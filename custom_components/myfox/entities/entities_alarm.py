import logging
from typing import Any

from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelState, AlarmControlPanelEntityFeature
from homeassistant.components.alarm_control_panel.const import CodeFormat

from ..coordinator.myfox_coordinator import (MyFoxCoordinator)
from ..devices import BaseDevice
from .entity import BaseWithValueEntity

_LOGGER = logging.getLogger(__name__)


class MyFoxAlarmEntity(AlarmControlPanelEntity, BaseWithValueEntity) :

    def __init__(self, coordinator: MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)
        self._attr_code_arm_required = coordinator.options.use_code_alarm
        if self._attr_code_arm_required:
            self._attr_code_format = CodeFormat.NUMBER
        else:
            self._attr_code_format = None
        self._attr_supported_features: AlarmControlPanelEntityFeature = (
            AlarmControlPanelEntityFeature.ARM_AWAY
            | AlarmControlPanelEntityFeature.ARM_HOME
        )

    def _update_value(self, val: Any) -> bool:
        # 1 : disarmed
        # 2 : partial
        # 4 : armed
        value = self.coordinator.data[self.idx]
        if type(value) is int :
            if int(value) == 1:
                self._attr_alarm_state = AlarmControlPanelState.DISARMED
            elif int(value) == 10:
                self._attr_alarm_state = AlarmControlPanelState.DISARMING
            elif int(value) == 2:
                self._attr_alarm_state = AlarmControlPanelState.ARMED_HOME
            elif int(value) == 20:
                self._attr_alarm_state = AlarmControlPanelState.ARMING
            elif int(value) == 4:
                self._attr_alarm_state = AlarmControlPanelState.ARMED_AWAY
            elif int(value) == 40:
                self._attr_alarm_state = AlarmControlPanelState.ARMING
            else:
                self._attr_alarm_state = AlarmControlPanelState.PENDING
        elif type(value) is str :
            self._attr_changed_by = value

        return True


    async def async_alarm_disarm(self, code=None) -> None:
        """Send disarm command."""
        coordinator: MyFoxCoordinator = self.coordinator
        await coordinator.setSecurity(self.idx, "disarmed", code)


    async def async_alarm_arm_away(self, code=None) -> None:
        """Send arm home command."""
        coordinator: MyFoxCoordinator = self.coordinator
        await coordinator.setSecurity(self.idx, "armed", code)


    async def async_alarm_arm_home(self, code=None) -> None:
        """Send arm home command."""
        coordinator: MyFoxCoordinator = self.coordinator
        await coordinator.setSecurity(self.idx, "partial", code)
