import logging
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity

from ..devices import  BaseDevice, MyFoxDeviceInfo
from ..entities.entities_sensor import LightSensorEntity

_LOGGER = logging.getLogger(__name__)

#LightSensor  {
    # deviceId (integer): The device identifier,
    # label (string): The device label,
    # light (integer, null): Current light level,
    # modelId (string): The device model identifier,
    # modelLabel (string): The device model label
#}
@dataclass
class MyFoxLightSensor :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    light: int

    
@dataclass
class MyFoxLightDevice(BaseDevice) :
    """" """
    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        _LOGGER.debug("Ajout LightSensorEntity / light sur device %s", str(self.device_info.deviceId))
        return [LightSensorEntity(coordinator, self, f"Luminosité {self.device_info.label}", "light")]
