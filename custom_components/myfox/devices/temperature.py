import logging

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from ..devices import  BaseDevice, MyFoxDeviceInfo
from ..sensor import TempSensorEntity

_LOGGER = logging.getLogger(__name__)

#TemperatureSensor {
#deviceId (integer): The device identifier,
#label (string): The device label,
#lastTemperature (float, null): Last temperature,
#lastTemperatureAt (string): Last temperature date,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label
#}

@dataclass
class MyFoxTemperatureSensor :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    lastTemperature: float = 0.0
    lastTemperatureAt: str = None

#TemperatureRecord {
#deviceId (integer): The temperature sensor device identifier,
#celsius (float): The temperature value is celsius degrees,
#recordedAt (string): The temperature value creation date
#}

@dataclass
class MyFoxTemperatureRecord :
    deviceId: int
    celsius: float
    recordedAt: str

@dataclass
class MyFoxTemperatureDevice(BaseDevice) :
    """ """

    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        _LOGGER.debug("Ajout TempSensorEntity / lastTemperature sur device %s", str(self.device_info.deviceId))
        return [TempSensorEntity(coordinator, self, "Temperature", "lastTemperature")]

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
