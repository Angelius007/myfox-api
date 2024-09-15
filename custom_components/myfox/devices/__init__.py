import dataclasses
import logging
from abc import ABC

from homeassistant.components.camera import Camera
from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

_LOGGER = logging.getLogger(__name__)

@dataclasses.dataclass
class MyFoxDeviceInfo:
    deviceId: int
    label: str
    modelId: int
    modelLabel: str

class BaseDevice(ABC):

    device_info: MyFoxDeviceInfo = None

    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__()
        self.device_info = device_info

    def sensors(self, coordinator) -> list[SensorEntity]:
        return []

    def numbers(self, coordinator) -> list[NumberEntity]:
        return []

    def switches(self, coordinator) -> list[SwitchEntity]:
        return []

    def selects(self, coordinator) -> list[SelectEntity]:
        return []

    def buttons(self, coordinator) -> list[ButtonEntity]:
        return []

    def texts(self, coordinator) -> list[ButtonEntity]:
        return []

    def cameras(self, coordinator) -> list[Camera]:
        return []
    
class DiagnosticDevice(BaseDevice):

    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__()
