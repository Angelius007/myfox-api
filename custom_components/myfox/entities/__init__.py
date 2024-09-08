import logging

from homeassistant.helpers.entity import Entity, EntityCategory, DeviceInfo
from homeassistant.components.button import ButtonEntity
from homeassistant.components.light  import LightEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.core import callback

from ..api.myfoxapi import MyFoxApiClient
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)


from ..const import (DOMAIN_MYFOX)

_LOGGER = logging.getLogger(__name__)

class MyFoxAbstractEntity(CoordinatorEntity, Entity):

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, context=str(device.device_info.deviceId)+"|"+key)
        self.idx = str(device.device_info.deviceId)+"|"+key 
        self._client: MyFoxApiClient = coordinator.myfoxApiClient
        self._device: BaseDevice = device
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+self.idx

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers={(DOMAIN_MYFOX, f"{self._device.device_info.deviceId+"-"+self._device.device_info.modelLabel}")},
            manufacturer="MyFox",
            name=self._device.device_info.label,
            model=self._device.device_info.modelLabel,
            model_id=self._device.device_info.modelId,
            serial_number=str(self._device.device_info.deviceId),
        )

class BaseWithValueEntity(MyFoxAbstractEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)
        if self.idx in self.coordinator.data:
            _LOGGER.debug("init value : %s, %s", self.idx, self.coordinator.data[self.idx])
            self._attr_native_value = self.coordinator.data[self.idx]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.idx in self.coordinator.data:
            _LOGGER.debug("_handle_coordinator_update : %s, %s", self.idx, self.coordinator.data[self.idx])
            self._attr_native_value = self.coordinator.data[self.idx]
            self.async_write_ha_state()

class BaseSensorEntity(SensorEntity, BaseWithValueEntity):
    pass

class BaseNumberEntity(NumberEntity, BaseWithValueEntity):
    pass

class BaseSwitchEntity(SwitchEntity, MyFoxAbstractEntity):
    pass

class BaseSelectEntity(SelectEntity, MyFoxAbstractEntity):
    pass

class BaseButtonEntity(ButtonEntity, MyFoxAbstractEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)

    def press(self) -> None:
        """Handle the button press."""
        coordinator:MyFoxCoordinator = self.coordinator
        coordinator.deferredPressButton(self.idx)

    async def async_press(self) -> None:
        """Handle the button press."""
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.pressButton(self.idx)

class BaseLightEntity(LightEntity, MyFoxAbstractEntity):
    pass
