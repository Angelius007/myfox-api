import logging
import jwt
from dataclasses import field
from typing import  Any
import voluptuous as vol
from collections.abc import Mapping

from homeassistant.config_entries import ConfigFlow, ConfigEntry, OptionsFlow, SOURCE_REAUTH, ConfigFlowResult
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.core import callback
from homeassistant.helpers import config_entry_oauth2_flow

from . import (DOMAIN_MYFOX, 
                CONFIG_VERSION)
from .api.const import (
     KEY_CLIENT_ID, 
     KEY_CLIENT_SECRET, 
     KEY_MYFOX_USER, 
     KEY_MYFOX_PSWD,
     KEY_SITE_ID,
     KEY_TOKEN,
     KEY_ACCESS_TOKEN,
     KEY_REFRESH_TOKEN,
     KEY_EXPIRE_IN,
     KEY_EXPIRE_AT,
     KEY_EXPIRE_TIME,
     KEY_CACHE_EXPIRE_IN,
     CACHE_EXPIRE_IN,
     POOLING_INTERVAL_DEF,
     KEY_POOLING_INTERVAL,
     KEY_CACHE_CAMERA,
     CACHE_CAMERA,
     KEY_CACHE_SECURITY,
     CACHE_SECURITY
)

from .api.myfoxapi import (
    MyFoxEntryDataApi,
    MyFoxOptionsDataApi,
    MyFoxApiClient
)
from .devices.site import MyFoxSite
from .api.oauth import MyFoxSystemImplementation

_LOGGER = logging.getLogger(__name__)

class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN_MYFOX
):
    """Config flow to handle MyFox OAuth2 authentication."""
    DOMAIN = DOMAIN_MYFOX

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return _LOGGER
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow start."""
        self.async_register_implementation(
            self.hass,
            MyFoxSystemImplementation(self.hass),
        )

        return await super().async_step_user()

    async def async_oauth_create_entry(
        self,
        data: dict[str, Any],
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        token = jwt.decode(
            data["token"]["access_token"], options={"verify_signature": False}
        )
        uid = token["sub"]

        await self.async_set_unique_id(uid)
        if self.source == SOURCE_REAUTH:
            self._abort_if_unique_id_mismatch(reason="reauth_account_mismatch")
            return self.async_update_reload_and_abort(
                self._get_reauth_entry(), data=data
            )
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=uid, data=data)

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauth dialog."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                description_placeholders={"name": "MyFox"},
            )
        return await self.async_step_user()
    
class MyFoxConfigFlow(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN_MYFOX):
    """ Config """
    DOMAIN = DOMAIN_MYFOX
    VERSION = CONFIG_VERSION
    PREFIX_ENTRY = "myfox-"

    # Init des variables locales
    def __init__(self) -> None:
        self.myfox_client:MyFoxApiClient = None
        self.siteId = None
        self.site: MyFoxSite = None
        self.sites: list[MyFoxSite] = field(default_factory=list[MyFoxSite])

        self.client_id = None
        self.client_secret = None
        self.username = None
        self.password = None

        self.access_token = None
        self.refresh_token = None

        self.config_entry: ConfigEntry | None = None
        self.data: dict[str, Any] | None = None

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return _LOGGER
    
    # Step pour relancer la conf
    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None): 
        if "entry_id" in self.context and self.context["entry_id"] :
            unique_id = self.context["entry_id"] #.replace(self.PREFIX_ENTRY, "")
            _LOGGER.debug("Entry trouvee : %s",unique_id)
            existing_entry = self.hass.config_entries.async_get_entry(unique_id)
            if existing_entry:
                self.data = existing_entry.data.copy()
                if KEY_CLIENT_ID in self.data:
                    self.client_id = self.data[KEY_CLIENT_ID]
                if KEY_CLIENT_SECRET in self.data:
                    self.client_secret = self.data[KEY_CLIENT_SECRET]
                if KEY_MYFOX_USER in self.data:
                    self.username = self.data[KEY_MYFOX_USER]
                if KEY_MYFOX_PSWD in self.data:
                    self.password = self.data[KEY_MYFOX_PSWD]
                if KEY_TOKEN in self.data:
                    if KEY_ACCESS_TOKEN in self.data[KEY_TOKEN]:
                        self.access_token = self.data[KEY_TOKEN][KEY_ACCESS_TOKEN]
                    if KEY_REFRESH_TOKEN in self.data[KEY_TOKEN]:
                        self.refresh_token = self.data[KEY_TOKEN][KEY_REFRESH_TOKEN]
                if KEY_SITE_ID in self.data:
                    self.siteId = self.data[KEY_SITE_ID]
            if self.data is None:
                self.data = dict[str, Any]()
            if user_input is not None:
                self.data.update(user_input)
        else :
            _LOGGER.debug("Entry non trouvee dans le context [%s]",str(self.context))
        return await self.async_step_user()


    # 1er step authent
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow start."""
        """Handle a flow start."""
        #self.async_register_implementation(
        #    self.hass,
        #    MyFoxSystemImplementation(self.hass),
        #)
        
        if self.data is None:
            self.data = dict[str, Any]()
        if user_input is not None:
            self.data.update(user_input)

        return await super().async_step_user()

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauth dialog."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                description_placeholders={"name": "MyFox"},
            )
        return await self.async_step_user()

    # 1er step config
    async def async_oauth_create_entry(self, info: dict[str, Any] | None = None):
        _LOGGER.info("async_oauth_create_entry :  %s", str(info))

        if self.source == SOURCE_REAUTH:
            self._abort_if_unique_id_mismatch(reason="reauth_account_mismatch")
            return self.async_update_reload_and_abort(
                self._get_reauth_entry(), data=info
            )
        
        USER_STEP_SCHEMA = vol.Schema({
            vol.Required(KEY_CLIENT_ID, default=self.client_id): str,
            vol.Required(KEY_CLIENT_SECRET, default=self.client_secret): str,
            vol.Optional(KEY_MYFOX_USER, default=self.username): str,
            vol.Optional(KEY_MYFOX_PSWD, default=self.password): str
        })
        if info is not None:
            myfox_info = MyFoxEntryDataApi(info.get(KEY_CLIENT_ID),
                                        info.get(KEY_CLIENT_SECRET),
                                        info.get(KEY_MYFOX_USER),
                                        info.get(KEY_MYFOX_PSWD))
            # anciens tokens
            if self.access_token :
                myfox_info.access_token = self.access_token
            if self.refresh_token :
                myfox_info.refresh_token = self.refresh_token
            # nouveaux token
            if KEY_TOKEN in info:
                if KEY_ACCESS_TOKEN in  info[KEY_TOKEN] :
                    myfox_info.access_token =  info[KEY_TOKEN][KEY_ACCESS_TOKEN]
                if KEY_REFRESH_TOKEN in  info[KEY_TOKEN] :
                    myfox_info.refresh_token =  info[KEY_TOKEN][KEY_REFRESH_TOKEN]
                if KEY_EXPIRE_IN in  info[KEY_TOKEN] :
                    myfox_info.expires_in =  info[KEY_TOKEN][KEY_EXPIRE_IN]
                if KEY_EXPIRE_AT in  info[KEY_TOKEN] :
                    myfox_info.expires_time =  info[KEY_TOKEN][KEY_EXPIRE_AT]
            
            options = MyFoxOptionsDataApi()
            options.cache_time = CACHE_EXPIRE_IN
            myfox_info.options = options
            self.myfox_client = MyFoxApiClient(myfox_info)
            if self.myfox_client.getExpireDelay() > 0 :
                await self.myfox_client.getInfoSites()
                """Recherche des devices."""
                self.sites = self.myfox_client.myfox_info.sites
            else :
                login_ok = await self.myfox_client.login()
                if login_ok :
                    """Recherche des devices."""
                    self.sites = self.myfox_client.myfox_info.sites
            self.data.update(info)
            return await self.async_step_select_site()

        return self.async_show_form(
            step_id="oauth_create_entry", data_schema=USER_STEP_SCHEMA)
    
    # Step de selection du site
    async def async_step_select_site(self, info: dict[str, Any] | None = None) -> FlowResult:
        """ Selection du site"""
        _LOGGER.info("async_step_select_site :  %s", str(info))
        if info is not None:
            """ sauvegarde du site et de l'entry """
            for site in self.sites:
                if site.key == info.get(KEY_SITE_ID) :
                    self.site = site
            device_unique_id = self.PREFIX_ENTRY+str(self.site.siteId)
            
            existing_entry = await self.async_set_unique_id(device_unique_id)
            
            new_data = {
                KEY_CLIENT_ID: self.myfox_client.myfox_info.client_id,
                KEY_CLIENT_SECRET: self.myfox_client.myfox_info.client_secret,
                KEY_MYFOX_USER: self.myfox_client.myfox_info.username,
                KEY_MYFOX_PSWD: self.myfox_client.myfox_info.password,

                KEY_SITE_ID: str(self.site.siteId),
            }
            if existing_entry:
                options = existing_entry.options.copy()
                #data = existing_entry.data.copy()
                self.data.update(info)
                self.data.update(new_data)

                if self.hass.config_entries.async_update_entry(existing_entry, data=self.data, options=options):
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                return self.async_abort(reason="updated_successfully")
            else :
                options = {
                    KEY_CACHE_EXPIRE_IN : CACHE_EXPIRE_IN
                }
                self.data.update(info)
                self.data.update(new_data)
                return self.async_create_entry(title=device_unique_id, data=self.data, options=options)
        
        site_list = list()
        default_site = None
        for site in self.sites:
            site_list.append(site.key)
            if self.siteId and int(self.siteId) == int(site.siteId) :
                default_site = site 

        SITE_STEP_SCHEMA = vol.Schema({
            vol.Required(KEY_SITE_ID, default=default_site): selector.SelectSelector(
                selector.SelectSelectorConfig(options=site_list,
                                                mode=selector.SelectSelectorMode.DROPDOWN))
        })
        
        return self.async_show_form(
            step_id="select_site", data_schema=SITE_STEP_SCHEMA)
    
    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """ Create the options flow. """
        return MyFoxOptionsFlowHandler(config_entry)

class MyFoxOptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        """ Initialize options flow. """
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """ Manage the options. """
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        cache_expire_in_param = CACHE_EXPIRE_IN
        if KEY_CACHE_EXPIRE_IN in self.config_entry.options:
            cache_expire_in_param = int(self.config_entry.options.get(KEY_CACHE_EXPIRE_IN))
        pooling_interval = POOLING_INTERVAL_DEF
        if KEY_POOLING_INTERVAL in self.config_entry.options:
            pooling_interval = int(self.config_entry.options.get(KEY_POOLING_INTERVAL))
        cache_camera = CACHE_CAMERA
        if KEY_CACHE_CAMERA in self.config_entry.options:
            cache_camera = int(self.config_entry.options.get(KEY_CACHE_CAMERA))
        cache_security = CACHE_SECURITY
        if KEY_CACHE_SECURITY in self.config_entry.options:
            cache_security = int(self.config_entry.options.get(KEY_CACHE_SECURITY))
     
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        KEY_POOLING_INTERVAL,
                        default=pooling_interval,
                    ): int,
                    vol.Required(
                        KEY_CACHE_EXPIRE_IN,
                        default=cache_expire_in_param,
                    ): int,
                    vol.Required(
                        KEY_CACHE_SECURITY,
                        default=cache_security,
                    ): int,
                    vol.Required(
                        KEY_CACHE_CAMERA,
                        default=cache_camera,
                    ): int
                }
            ),
        )