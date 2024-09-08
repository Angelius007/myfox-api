import logging

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity

from ..devices import  BaseDevice, MyFoxDeviceInfo
from ..entities.entities_sensor import AlerteSateSensorEntity

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
class MyFoxAlerteSensorDevice(BaseDevice) :
    """" """
    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        _LOGGER.debug("Ajout Sensors sur device %s", str(self.device_info.deviceId))
        return [AlerteSateSensorEntity(coordinator, self, f"Etat {self.device_info.label}", "state")]

