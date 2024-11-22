import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.hass_dict import HassEntryKey

from .const import (DOMAIN_MYFOX)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .api.myfoxapi import (MyFoxApiClient)

_LOGGER = logging.getLogger(__name__)
MYFOX_KEY: HassEntryKey["MyFoxCoordinator"] = HassEntryKey(DOMAIN_MYFOX)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des scenes """
    coordinator:MyFoxCoordinator = hass.data.setdefault(MYFOX_KEY, {})[entry.entry_id]
    known_scenes: set[str] = set()
    
    def _check_scene() -> None:
        for (client_key,client_item) in coordinator.myfoxApiClients.items() :
            client: MyFoxApiClient = client_item

            for (scenarioId, scene) in client.scenes.items():
                # ajout uniquement des nouveaux devices
                scene_unique = client.client_key + scenarioId
                if scene_unique not in known_scenes :
                    known_scenes.add(scene_unique)
                    async_add_entities(scene.scenes(coordinator))

    _check_scene()
    entry.async_on_unload(
        coordinator.async_add_listener(_check_scene)
    )
