import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (DOMAIN_MYFOX)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .api.myfoxapi import (MyFoxApiClient)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des scenes """
    coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX][entry.entry_id]
    for (client_key,client_item) in coordinator.myfoxApiClients.items() :
        client: MyFoxApiClient = client_item

        for (scenarioId, scene) in client.scenes.items():
            async_add_entities(scene.scenes(coordinator))
