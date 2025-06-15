import logging

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_sensor import TempSensorEntity

_LOGGER = logging.getLogger(__name__)

# TemperatureSensor {
# deviceId (integer): The device identifier,
# label (string): The device label,
# lastTemperature (float, null): Last temperature,
# lastTemperatureAt (string): Last temperature date,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }

# TemperatureRecord {
# deviceId (integer): The temperature sensor device identifier,
# celsius (float): The temperature value is celsius degrees,
# recordedAt (string): The temperature value creation date
# }


@dataclass
class MyFoxTemperatureDevice(BaseDevice) :
    """ """

    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__(device_info)

    def sensors(self, coordinator) -> list[SensorEntity]:
        _LOGGER.debug("Ajout TempSensorEntity / lastTemperature sur device %s", str(self.device_info.deviceId))
        return [TempSensorEntity(coordinator, self, f"Temperature {self.device_info.label}", "lastTemperature")]
