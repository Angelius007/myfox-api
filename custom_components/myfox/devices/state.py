import logging

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity

from . import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_sensor import AlerteStateSensorEntity, StateSensorEntity

_LOGGER = logging.getLogger(__name__)

# GenericSensor {
# deviceId (integer): The device identifier,
# label (string): The device label,
# state (integer, null): Current device state,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }

# DeviceWithState {
# deviceId (integer): The device identifier,
# label (string): The device label,
# stateLabel (string, null) = ['opened' or 'closed']: Current state,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }


@dataclass
class MyFoxAlerteStateDevice(BaseDevice) :
    """" """
    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        _LOGGER.debug("Ajout AlerteStateSensorEntity sur device %s", str(self.device_info.deviceId))
        return [AlerteStateSensorEntity(coordinator, self, f"Etat {self.device_info.label}", "state")]


@dataclass
class MyFoxStateDevice(BaseDevice) :
    """" """
    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        _LOGGER.debug("Ajout StateSensorEntity sur device %s", str(self.device_info.deviceId))
        return [StateSensorEntity(coordinator, self, f"Etat {self.device_info.label}", "stateLabel")]
