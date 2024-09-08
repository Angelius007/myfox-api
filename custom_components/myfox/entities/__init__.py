import logging
from typing import Any

from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.components.number import NumberEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.core import callback

from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)


from ..const import (DOMAIN_MYFOX)

_LOGGER = logging.getLogger(__name__)

## ////////////////////////////////////////////////////////////////////////////
## DEVICES
## ////////////////////////////////////////////////////////////////////////////

class MyFoxAbstractDeviceEntity(CoordinatorEntity, Entity):

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, context=str(device.device_info.deviceId)+"|"+key)
        self.idx = str(device.device_info.deviceId)+"|"+key 
        self._device: BaseDevice = device
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+self.idx

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers={(DOMAIN_MYFOX, f"{self._device.device_info.deviceId}-{self._device.device_info.modelLabel}")},
            manufacturer="MyFox",
            name=self._device.device_info.label,
            model=self._device.device_info.modelLabel,
            model_id=self._device.device_info.modelId,
            serial_number=str(self._device.device_info.deviceId),
        )

class BaseWithValueEntity(MyFoxAbstractDeviceEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)
        if self.idx in self.coordinator.data:
            statutok=self._update_value(coordinator.data[self.idx])
            _LOGGER.debug("init value : %s, %s : %s", self.idx, self.coordinator.data[self.idx], str(statutok))
            
    def _update_value(self, val: Any) -> bool:
        self._attr_native_value = self.coordinator.data[self.idx]
        return True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.idx in self.coordinator.data:
            _LOGGER.debug("_handle_coordinator_update : %s, %s", self.idx, self.coordinator.data[self.idx])
            if self._update_value(self.coordinator.data[self.idx]) :
                self.async_write_ha_state()


class BaseNumberEntity(NumberEntity, BaseWithValueEntity):
    pass

class BaseSwitchEntity(SwitchEntity, MyFoxAbstractDeviceEntity):
    pass
