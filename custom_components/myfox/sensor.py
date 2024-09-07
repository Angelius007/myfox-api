import logging

from homeassistant.components.sensor import (SensorDeviceClass, SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (UnitOfTemperature, LIGHT_LUX)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (DOMAIN_MYFOX)
from .api.myfoxapi import (MyFoxApiClient)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .entities import BaseSensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des sensors """
    coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX][entry.entry_id]
    for (client_key,client_item) in coordinator.myfoxApiClient.items() :
        client: MyFoxApiClient = client_item

        for (deviceId, device) in client.devices.items():
            async_add_entities(device.sensors(coordinator))


class TempSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = -1


class LightSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = LIGHT_LUX
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = -1

