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
    def sensors(self, client, coordinator) -> list[SensorEntity]:
        pass

    @abstractmethod
    def numbers(self, client, coordinator) -> list[NumberEntity]:
        pass

    @abstractmethod
    def switches(self, client, coordinator) -> list[SwitchEntity]:
        pass

    @abstractmethod
    def selects(self, client, coordinator) -> list[SelectEntity]:
        pass

    @abstractmethod
    def buttons(self, client, coordinator) -> list[ButtonEntity]:
        pass

    @abstractmethod
    def texts(self, client, coordinator) -> list[ButtonEntity]:
        pass

class DiagnosticDevice(BaseDevice):

    def sensors(self, client, coordinator) -> list[SensorEntity]:
        return []

    def numbers(self, client, coordinator) -> list[NumberEntity]:
        return []

    def switches(self, client, coordinator) -> list[SwitchEntity]:
        return []

    def buttons(self, client, coordinator) -> list[ButtonEntity]:
        return []

    def selects(self, client, coordinator) -> list[SelectEntity]:
        return []
    
    def texts(self, client, coordinator) -> list[ButtonEntity]:
        return []