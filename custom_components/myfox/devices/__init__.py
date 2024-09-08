import dataclasses
import logging
from abc import ABC

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

    def configure(self, refresh_period: int, diag: bool = False):
        #self.data = MyFoxDataHolder(refresh_period, diag)
        """ """

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
    
class DiagnosticDevice(BaseDevice):

    def sensors(self, coordinator) -> list[SensorEntity]:
        return []

    def numbers(self, coordinator) -> list[NumberEntity]:
        return []

    def switches(self, coordinator) -> list[SwitchEntity]:
        return []

    def buttons(self, coordinator) -> list[ButtonEntity]:
        return []

    def selects(self, coordinator) -> list[SelectEntity]:
        return []
    
    def texts(self, coordinator) -> list[ButtonEntity]:
        return []
