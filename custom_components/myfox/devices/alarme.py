import logging

from dataclasses import dataclass

from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity
from homeassistant.components.select import SelectEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_select import SecuritySelectEntity
from ..entities.entities_alarm import MyFoxAlarmEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class MyFoxAlarmeDevice(BaseDevice) :
    """ """

    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    #def selects(self, coordinator) -> list[SelectEntity]:
    #    _LOGGER.debug("Ajout SecuritySelectEntity sur device %s", str(self.device_info.deviceId))
    #    # TODO : https://developers.home-assistant.io/docs/core/entity/alarm-control-panel
    #    return [SecuritySelectEntity(coordinator, self, f"{self.device_info.label}", "status")]

    def alarms(self, coordinator) -> list[AlarmControlPanelEntity]:
        _LOGGER.debug("Ajout AlarmControlPanelEntity sur device %s", str(self.device_info.deviceId))
        return [MyFoxAlarmEntity(coordinator, self, f"{self.device_info.label}", "status")]