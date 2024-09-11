from homeassistant.config_entries import ConfigFlow, ConfigEntry, OptionsFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from dataclasses import field
from typing import Dict, Any
import voluptuous as vol
from . import (DOMAIN_MYFOX, 
                CONFIG_VERSION)
from .api.const import (
     KEY_CLIENT_ID, 
     KEY_CLIENT_SECRET, 
     KEY_MYFOX_USER, 
     KEY_MYFOX_PSWD,
     KEY_SITE_ID,
     KEY_ACCESS_TOKEN,
     KEY_REFRESH_TOKEN,
     KEY_EXPIRE_IN,
     KEY_EXPIRE_TIME
)

from .api.myfoxapi import (
    MyFoxEntryDataApi,
    MyFoxApiClient
)
from .devices.site import MyFoxSite

class MyFoxConfigFlow(ConfigFlow, domain=DOMAIN_MYFOX):
    """ Config """
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

    # Step pour relancer la conf
    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None): 
        if "entry_id" in self.context and self.context["entry_id"] :
            unique_id = self.context["entry_id"] #.replace(self.PREFIX_ENTRY, "")
            existing_entry = await self.async_set_unique_id(unique_id, raise_on_progress=False)
            if existing_entry:
                data = existing_entry.data.copy()
                if KEY_CLIENT_ID in data:
                    self.client_id = data[KEY_CLIENT_ID]
                if KEY_CLIENT_SECRET in data:
                    self.client_secret = data[KEY_CLIENT_SECRET]
                if KEY_MYFOX_USER in data:
                    self.username = data[KEY_MYFOX_USER]
                if KEY_MYFOX_PSWD in data:
                    self.password = data[KEY_MYFOX_PSWD]
                if KEY_ACCESS_TOKEN in data:
                    self.access_token = data[KEY_ACCESS_TOKEN]
                if KEY_REFRESH_TOKEN in data:
                    self.refresh_token = data[KEY_REFRESH_TOKEN]
                if KEY_SITE_ID in data:
                    self.siteId = data[KEY_SITE_ID]

        return await self.async_step_user()

    # 1er step
    async def async_step_user(self, info: dict[str, Any] | None = None):
        USER_STEP_SCHEMA = vol.Schema({
            vol.Required(KEY_CLIENT_ID, default=self.client_id): str,
            vol.Required(KEY_CLIENT_SECRET, default=self.client_secret): str,
            vol.Required(KEY_MYFOX_USER, default=self.username): str,
            vol.Required(KEY_MYFOX_PSWD, default=self.password): str,
            vol.Optional(KEY_ACCESS_TOKEN, default=self.access_token): str,
            vol.Optional(KEY_REFRESH_TOKEN, default=self.refresh_token): str,
        })
        if info is not None:
            myfox_info = MyFoxEntryDataApi(info.get(KEY_CLIENT_ID),
                                        info.get(KEY_CLIENT_SECRET),
                                        info.get(KEY_MYFOX_USER),
                                        info.get(KEY_MYFOX_PSWD))
            if KEY_ACCESS_TOKEN in info :
                myfox_info.access_token = info.get(KEY_ACCESS_TOKEN)
            if KEY_REFRESH_TOKEN in info :
                myfox_info.refresh_token = info.get(KEY_REFRESH_TOKEN)
            
            self.myfox_client = MyFoxApiClient(myfox_info)
            
            login_ok = await self.myfox_client.login()
            if login_ok :
                """Recherche des devices."""
                self.sites = self.myfox_client.myfox_info.sites

            return await self.async_step_select_site()

        return self.async_show_form(
            step_id="user", data_schema=USER_STEP_SCHEMA)
    
    # Step de selection du site
    async def async_step_select_site(self, info: dict[str, Any] | None = None) -> FlowResult:
        """ Selection du site"""
        if info is not None:
            """ sauvegarde du site et de l'entry """
            for site in self.sites:
                if site.key == info.get(KEY_SITE_ID) :
                    self.site = site
            device_unique_id = self.PREFIX_ENTRY+str(self.site.siteId)
            
            existing_entry = await self.async_set_unique_id(device_unique_id)
            
            options = {}
            if existing_entry:
                data = existing_entry.data.copy()
                data[KEY_CLIENT_ID] = self.myfox_client.myfox_info.client_id
                data[KEY_CLIENT_SECRET] = self.myfox_client.myfox_info.client_secret
                data[KEY_MYFOX_USER] = self.myfox_client.myfox_info.username
                data[KEY_MYFOX_PSWD] = self.myfox_client.myfox_info.password
                data[KEY_ACCESS_TOKEN] = self.myfox_client.myfox_info.access_token
                data[KEY_REFRESH_TOKEN] = self.myfox_client.myfox_info.refresh_token
                data[KEY_EXPIRE_IN] = self.myfox_client.myfox_info.expires_in
                data[KEY_EXPIRE_TIME] = self.myfox_client.myfox_info.expires_time
                data[KEY_SITE_ID] = str(self.site.siteId)
                if self.hass.config_entries.async_update_entry(existing_entry, data=data):
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                return self.async_abort(reason="updated_successfully")
            else :
                data = {
                    KEY_CLIENT_ID: self.myfox_client.myfox_info.client_id,
                    KEY_CLIENT_SECRET: self.myfox_client.myfox_info.client_secret,
                    KEY_MYFOX_USER: self.myfox_client.myfox_info.username,
                    KEY_MYFOX_PSWD: self.myfox_client.myfox_info.password,
                    KEY_ACCESS_TOKEN: self.myfox_client.myfox_info.access_token,
                    KEY_REFRESH_TOKEN: self.myfox_client.myfox_info.refresh_token,
                    KEY_EXPIRE_IN: self.myfox_client.myfox_info.expires_in,
                    KEY_EXPIRE_TIME: self.myfox_client.myfox_info.expires_time,
                    KEY_SITE_ID: str(self.site.siteId),
                }
                return self.async_create_entry(title=device_unique_id, data=data, options=options)

        
        site_list = list()
        for site in self.sites:
            site_list.append(site.key)

        SITE_STEP_SCHEMA = vol.Schema({
            vol.Required(KEY_SITE_ID, default=self.siteId): selector.SelectSelector(
                selector.SelectSelectorConfig(options=site_list,
                                                mode=selector.SelectSelectorMode.DROPDOWN))
        })
        
        return self.async_show_form(
            step_id="select_site", data_schema=SITE_STEP_SCHEMA)


