from homeassistant.config_entries import ConfigFlow, ConfigEntry, OptionsFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from dataclasses import field
from typing import Dict, Any
import voluptuous as vol
from . import (DOMAIN, 
                   CONFIG_VERSION)
from .api.const import (
     KEY_CLIENT_ID, 
     KEY_CLIENT_SECRET, 
     KEY_MYFOX_USER, 
     KEY_MYFOX_PSWD,
     KEY_SITE_ID
)
from .api.myfoxapi import (
    MyFoxEntryDataApi,
    MyFoxApiClient
)
from .devices.site import MyFoxSite

class MyFoxConfigFlow(ConfigFlow, domain=DOMAIN):
    """ Config """
    VERSION = CONFIG_VERSION

    # Init des variables locales
    def __init__(self) -> None:
        self.client_id = None
        self.client_secret = None
        self.username = None
        self.password = None
        self.site_id = None
        self.sites: list[MyFoxSite] = field(default_factory=list)

        self.config_entry: ConfigEntry | None = None

    # Step pour relancer la conf
    async def async_step_reconfigure_user(self, user_input: dict[str, Any] | None = None):
        if not user_input:
            return self.async_show_menu(
                step_id="user"
            )

    # 1er step
    async def async_step_user(self, info: dict[str, Any] | None = None):
        USER_STEP_SCHEMA = vol.Schema({
            vol.Required(KEY_CLIENT_ID): str,
            vol.Required(KEY_CLIENT_SECRET): str,
            vol.Required(KEY_MYFOX_USER): str,
            vol.Required(KEY_MYFOX_PSWD): str
        })
        if info is not None:
            self.client_id      = info.get(KEY_CLIENT_ID)
            self.client_secret  = info.get(KEY_CLIENT_SECRET)
            self.username       = info.get(KEY_MYFOX_USER)
            self.password       = info.get(KEY_MYFOX_PSWD)

            myfox_info = MyFoxEntryDataApi(self.client_id,
                                        self.client_secret,
                                        self.username,
                                        self.password)
            myfox_client = MyFoxApiClient(myfox_info)
            
            login_ok = await myfox_client.login()

            if login_ok :
                """Recherche des devices."""
                self.sites = myfox_client.myfox_info.sites

            return await self.async_step_select_site()

        return self.async_show_form(
            step_id="user", data_schema=USER_STEP_SCHEMA)
    
    # Step de selection du site
    async def async_step_select_site(self, info: dict[str, Any] | None = None) -> FlowResult:
        """ Selection du site"""
        if info is not None:
            """ sauvegarde du site et de l'entry """
            self.site_id       = info.get(KEY_SITE_ID)
            device_unique_id = "myfox-"+self.site_id
            
            await self.async_set_unique_id(device_unique_id)
            self._abort_if_unique_id_configured()
            
            options = {}
            data = {
                KEY_CLIENT_ID: self.client_id,
                KEY_CLIENT_SECRET: self.client_secret,
                KEY_MYFOX_USER: self.username,
                KEY_MYFOX_PSWD: self.password,

            }
            return self.async_create_entry(title=self.installation_site, data=data, options=options)

        
        site_list = list()
        for site in self.sites:
            site_list.append(site.key)

        SITE_STEP_SCHEMA = vol.Schema({
            vol.Required(KEY_SITE_ID): selector.SelectSelector(
                selector.SelectSelectorConfig(options=site_list,
                                                mode=selector.SelectSelectorMode.DROPDOWN))
        })
        
        return self.async_show_form(
            step_id="select_site", data_schema=SITE_STEP_SCHEMA)


