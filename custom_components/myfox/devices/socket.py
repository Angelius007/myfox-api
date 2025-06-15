import logging

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_button import SocketButtonEntity

_LOGGER = logging.getLogger(__name__)

# Socket {
# deviceId (integer): The device identifier,
# label (string): The device label,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }


@dataclass
class MyFoxSocketDevice(BaseDevice) :
    """ """

    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__(device_info)

    def buttons(self, coordinator) -> list[ButtonEntity]:
        _LOGGER.debug("Ajout SocketButtonEntity sur device %s", str(self.device_info.deviceId))
        return [SocketButtonEntity(coordinator, self, f"On {self.device_info.label}", "on"),
                SocketButtonEntity(coordinator, self, f"Off {self.device_info.label}", "off")]


@dataclass
class MyFoxGroupSocketDevice(MyFoxSocketDevice) :
    """ """

    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__(device_info)
