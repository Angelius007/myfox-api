import dataclasses
import json
import logging
from abc import ABC, abstractmethod

from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

#from .data_holder import MyFoxDataHolder

_LOGGER = logging.getLogger(__name__)

@dataclasses.dataclass
class MyFoxDeviceInfo:
    deviceId: int
    label: str
    modelId: int
    modelLabel: str

class BaseDevice(ABC):

    #data: MyFoxDataHolder = None
    device_info: MyFoxDeviceInfo = None

    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__()
        self.device_info = device_info

    def configure(self, refresh_period: int, diag: bool = False):
        #self.data = MyFoxDataHolder(refresh_period, diag)
        """ """

    @abstractmethod
    def sensors(self, coordinator) -> list[SensorEntity]:
        pass

    @abstractmethod
    def numbers(self, coordinator) -> list[NumberEntity]:
        pass

    @abstractmethod
    def switches(self, coordinator) -> list[SwitchEntity]:
        pass

    @abstractmethod
    def selects(self, coordinator) -> list[SelectEntity]:
        pass

    @abstractmethod
    def buttons(self, coordinator) -> list[ButtonEntity]:
        pass

    @abstractmethod
    def texts(self, coordinator) -> list[ButtonEntity]:
        pass

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