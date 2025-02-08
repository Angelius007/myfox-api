import logging

from dataclasses import dataclass

from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_alarm import MyFoxAlarmEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class MyFoxAlarmeDevice(BaseDevice) :
    """ """

    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def alarms(self, coordinator) -> list[AlarmControlPanelEntity]:
        _LOGGER.debug("Ajout AlarmControlPanelEntity sur device %s", str(self.device_info.deviceId))
        return [MyFoxAlarmEntity(coordinator, self, f"{self.device_info.label}", "status")]
