import logging

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..button import SocketButtonEntity

_LOGGER = logging.getLogger(__name__)

#Socket {
#deviceId (integer): The device identifier,
#label (string): The device label,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label
#}

@dataclass
class MyFoxSocket :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str


@dataclass
class MyFoxSocketDevice(BaseDevice) :
    """ """

    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        return []

    def numbers(self, coordinator) -> list[NumberEntity]:
        return []

    def switches(self, coordinator) -> list[SwitchEntity]:
        return []

    def buttons(self, coordinator) -> list[ButtonEntity]:
        _LOGGER.debug("Ajout buttons sur device %s", str(self.device_info.deviceId))
        return [SocketButtonEntity(coordinator, self,f"On {self.device_info.label}", "on"),
                SocketButtonEntity(coordinator, self, f"Off {self.device_info.label}", "off")]

    def selects(self, coordinator) -> list[SelectEntity]:
        return []
    
    def texts(self, coordinator) -> list[ButtonEntity]:
        return []
