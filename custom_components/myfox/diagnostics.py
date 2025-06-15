import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util.hass_dict import HassEntryKey

from .coordinator.myfox_coordinator import (MyFoxCoordinator)

from . import DOMAIN_MYFOX

_LOGGER = logging.getLogger(__name__)
MYFOX_KEY: HassEntryKey["MyFoxCoordinator"] = HassEntryKey(DOMAIN_MYFOX)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    values = {"MyFox": []}
    # Coordinator
    coordinator: MyFoxCoordinator = hass.data.setdefault(MYFOX_KEY, {})[entry.entry_id]
    value_myfox = {
        "coordinator" : coordinator.name,
        "info_site" : [],
        "clients" : [],
        "last_params" : [dict(sorted(coordinator.last_params.items()))],
    }
    value_site = None
    for (client_key, myfoxApiClient) in coordinator.myfoxApiClients.items() :
        """ Clients """
        if value_site is None:
            value_site = {
                "site" : str(myfoxApiClient.myfox_info.site),
                "access_token" : myfoxApiClient.myfox_info.access_token,
                "refresh_token" : myfoxApiClient.myfox_info.refresh_token,
            }
            value_myfox["info_site"].append(value_site)
        value_client = {
            "client_key": myfoxApiClient.client_key,
            "devices": [],
            "scenes": []
        }
        for (sn, device) in myfoxApiClient.devices.items():
            """ Devices """
            value_device = {
                'label': device.device_info.label,
                'deviceId': device.device_info.deviceId,
                'modelId': device.device_info.modelId,
                'modelLabel': device.device_info.modelLabel,
            }
            value_client["devices"].append(value_device)
        for (sn, scene) in myfoxApiClient.scenes.items():
            """ Scenes """
            value_scene = {
                'label': scene.scene_info.label,
                'scenarioId': scene.scene_info.scenarioId,
                'typeLabel': scene.scene_info.typeLabel,
                'enabled': scene.scene_info.enabled,
            }
            value_client["scenes"].append(value_scene)
        value_myfox["clients"].append(value_client)
    values["MyFox"].append(value_myfox)

    return values
