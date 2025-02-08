import logging
from typing import Any

from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelState

from ..coordinator.myfox_coordinator import (MyFoxCoordinator)
from ..devices import BaseDevice
from .entity import BaseWithValueEntity

_LOGGER = logging.getLogger(__name__)

class MyFoxAlarmEntity(AlarmControlPanelEntity, BaseWithValueEntity) :

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)

    def _update_value(self, val: Any) -> bool:
        # 1 : disarmed
        # 2 : partial
        # 4 : armed
        value = self.coordinator.data[self.idx]
        if int(value) == 1:
            self._attr_alarm_state = AlarmControlPanelState.DISARMED
        elif int(value) == 2:
            self._attr_alarm_state = AlarmControlPanelState.ARMED_HOME
        elif int(value) == 4:
            self._attr_alarm_state = AlarmControlPanelState.ARMED_AWAY
        else:
            self._attr_alarm_state = AlarmControlPanelState.PENDING
        
        return True


    async def async_alarm_disarm(self, code=None) -> None:
        """Send disarm command."""
        self._attr_alarm_state = AlarmControlPanelState.DISARMING
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.setSecurity("disarmed")

    async def async_alarm_arm_away(self, code=None) -> None:
        """Send arm home command."""
        self._attr_alarm_state = AlarmControlPanelState.ARMING
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.setSecurity("armed")
        
    async def async_alarm_arm_home(self, code=None) -> None:
        """Send arm home command."""
        self._attr_alarm_state = AlarmControlPanelState.ARMING
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.setSecurity("partial")
    
    async def async_alarm_arm_night(self, code=None) -> None:
        """Send arm night command."""
        self._attr_alarm_state = AlarmControlPanelState.ARMING
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.setSecurity("partial")
