import logging

from homeassistant.components.sensor import (SensorDeviceClass, SensorStateClass, SensorEntity)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (UnitOfTemperature)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (DOMAIN_MYFOX)
from .api.myfoxapi import (MyFoxApiClient)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .entities import BaseSensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des switchs """
    for (client_key,client_item) in hass.data[DOMAIN_MYFOX][entry.entry_id].items() :
        client: MyFoxApiClient = client_item
        _LOGGER.debug("client:"+str(client.__class__))

        coordinator = MyFoxCoordinator(hass, client)
        await coordinator.async_config_entry_first_refresh()

        for (deviceId, device) in client.devices.items():
            async_add_entities(device.sensors(client, coordinator))


class TempSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = -1

    def __init__(self, client, coordinator:MyFoxCoordinator, device, title: str, key: str):
        super().__init__(client, coordinator, device, title, key)
        if self.idx in self.coordinator.data:
            _LOGGER.debug("init value : %s, %s", self.idx, self.coordinator.data[self.idx])
            self._attr_native_value = self.coordinator.data[self.idx]
            self.async_write_ha_state()
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.idx in self.coordinator.data:
            _LOGGER.debug("_handle_coordinator_update : %s, %s", self.idx, self.coordinator.data[self.idx])
            self._attr_native_value = self.coordinator.data[self.idx]
            self.async_write_ha_state()

    
