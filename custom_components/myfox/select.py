import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .api.myfoxapi import (MyFoxApiClient)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des switchs """
    for (client_key,client_item) in hass.data[DOMAIN][entry.entry_id].items() :
        client: MyFoxApiClient = client_item
        _LOGGER.debug("client:"+str(client.__class__))

        coordinator = MyFoxCoordinator(hass, client)
        await coordinator.async_config_entry_first_refresh()

        for (deviceId, device) in client.devices.items():
            async_add_entities(device.selects(client, coordinator))
