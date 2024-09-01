import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN
from api.myfoxapi import (MyFoxApiClient)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des switchs """
    for client_item in hass.data[DOMAIN][entry.entry_id].items() :
        client: MyFoxApiClient = client_item
        for (deviceId, device) in client.devices.items():
            async_add_entities(device.selects(client))
