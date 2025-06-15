import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.hass_dict import HassEntryKey

from .const import (DOMAIN_MYFOX)
from .api.myfoxapi import (MyFoxApiClient)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
MYFOX_KEY: HassEntryKey["MyFoxCoordinator"] = HassEntryKey(DOMAIN_MYFOX)

PARALLEL_UPDATES = 1


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des sensors """
    coordinator: MyFoxCoordinator = hass.data.setdefault(MYFOX_KEY, {})[entry.entry_id]
    known_devices: set[str] = set()

    def _check_device() -> None:
        for (client_key, client_item) in coordinator.myfoxApiClients.items() :
            client: MyFoxApiClient = client_item

            for (deviceId, device) in client.devices.items():
                # ajout uniquement des nouveaux devices
                device_unique = client.client_key + deviceId
                if device_unique not in known_devices :
                    known_devices.add(device_unique)
                    async_add_entities(device.cameras(coordinator))

    _check_device()
    entry.async_on_unload(
        coordinator.async_add_listener(_check_device)
    )
