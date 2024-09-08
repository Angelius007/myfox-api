import logging

from homeassistant.components.button import (ButtonDeviceClass, ButtonEntity)
from homeassistant.helpers.entity import EntityCategory

from . import MyFoxAbstractDeviceEntity
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
 
class BaseButtonEntity(ButtonEntity, MyFoxAbstractDeviceEntity):
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


class ShutterButtonEntity(BaseButtonEntity):
    """ """
    _attr_device_class = ButtonDeviceClass.IDENTIFY
    _attr_entity_category = EntityCategory.CONFIG

    @property
    def icon(self) -> str | None:
        if self.idx.endswith("open"):
            return "mdi:window-shutter-open"
        elif self.idx.endswith("close"):
            return "mdi:window-shutter"
        elif self.idx.endswith("my"):
            return "mdi:window-shutter-auto"
        else :
            return "mdi:eye"


class SocketButtonEntity(BaseButtonEntity):
    """ """
    _attr_device_class = ButtonDeviceClass.IDENTIFY
    _attr_entity_category = EntityCategory.CONFIG

    @property
    def icon(self) -> str | None:
        if self.idx.endswith("on"):
            return "mdi:toggle-switch-variant"
        elif self.idx.endswith("off"):
            return "mdi:toggle-switch-variant-off"
        else :
            return "mdi:eye"
    