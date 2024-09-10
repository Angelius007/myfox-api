import logging

from dataclasses import dataclass

from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_select import HeaterSelectEntity
_LOGGER = logging.getLogger(__name__)

#Heater {
#deviceId (integer): The device identifier,
#label (string): The device label,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label,
#modeLabel (string) = ['boiler' or 'wired']: The heater heating mode,
#stateLabel (string) = ['on' or 'off' or 'eco' or 'frost' or 'boost' or 'away' or 'auto']: The heater state,
#lastTemperature (float, null, optional): Last temperature
#}

@dataclass
class MyFoxHeater :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    modeLabel: str
    stateLabel: str
    lastTemperature: float | None = None

@dataclass
class MyFoxHeaterDevice(BaseDevice) :

    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        return []

    def selects(self, coordinator) -> list[SelectEntity]:
        _LOGGER.debug("Ajout HeaterSelectEntity sur device %s", str(self.device_info.deviceId))
        return [HeaterSelectEntity(coordinator, self, f"Consigne {self.device_info.label}", "stateLabel")]
