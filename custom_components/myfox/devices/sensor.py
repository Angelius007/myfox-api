import logging

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from ..devices import  BaseDevice, MyFoxDeviceInfo
from ..sensor import TempSensorEntity
from ..sensor import LightSensorEntity

_LOGGER = logging.getLogger(__name__)

# GenericSensor {
# deviceId (integer): The device identifier,
# label (string): The device label,
# state (integer, null): Current device state,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }

@dataclass
class MyFoxGenerictSensor :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    state: int

# DeviceWithState {
# deviceId (integer): The device identifier,
# label (string): The device label,
# stateLabel (string, null) = ['opened' or 'closed']: Current state,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }
@dataclass
class MyFoxDeviceWithState :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    stateLabel : str

@dataclass
class MyFoxDeviceWithStateState :
    deviceId: int
    stateLabel : str


@dataclass
class MyFoxSensorDevice(BaseDevice) :
    """" """
    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        _LOGGER.debug("Ajout Sensors sur device %s", str(self.device_info.deviceId))
        return [TempSensorEntity(coordinator, self, f"Temperature {self.device_info.label}", "lastTemperature"),
                LightSensorEntity(coordinator, self, f"Luminosité {self.device_info.label}", "light")]

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
