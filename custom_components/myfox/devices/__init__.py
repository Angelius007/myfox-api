import dataclasses
import json
import logging
from abc import ABC, abstractmethod

from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from .data_holder import MyFoxDataHolder
#from ..api.myfoxapi import MyFoxApiClient 

_LOGGER = logging.getLogger(__name__)

@dataclasses.dataclass
class MyFoxDeviceInfo:
    deviceId: int
    label: str
    modelId: int
    modelLabel: str

class BaseDevice(ABC):

    data: MyFoxDataHolder = None
    device_info: MyFoxDeviceInfo = None

    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__()

    def configure(self, refresh_period: int, diag: bool = False):
        self.data = MyFoxDataHolder(refresh_period, diag)

    @abstractmethod
    def sensors(self, client) -> list[SensorEntity]: # : MyFoxApiClient
        pass

    @abstractmethod
    def numbers(self, client) -> list[NumberEntity]:
        pass

    @abstractmethod
    def switches(self, client) -> list[SwitchEntity]:
        pass

    @abstractmethod
    def selects(self, client) -> list[SelectEntity]:
        pass

    @abstractmethod
    def buttons(self, client) -> list[ButtonEntity]:
        pass

class DiagnosticDevice(BaseDevice):

    def sensors(self, client) -> list[SensorEntity]:
        return []

    def numbers(self, client) -> list[NumberEntity]:
        return []

    def switches(self, client) -> list[SwitchEntity]:
        return []

    def buttons(self, client) -> list[ButtonEntity]:
        return []

    def selects(self, client) -> list[SelectEntity]:
        return []