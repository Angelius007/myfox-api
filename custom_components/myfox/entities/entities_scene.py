import logging

from typing import Any

from homeassistant.components.scene import Scene
from homeassistant.components.switch import SwitchEntity
from .entity import MyFoxAbstractSceneEntity, BaseSceneWithValueEntity
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)
from ..scenes import BaseScene

_LOGGER = logging.getLogger(__name__)

# # ////////////////////////////////////////////////////////////////////////////
# # SCENES
# # ////////////////////////////////////////////////////////////////////////////


class BaseSceneEntity(Scene, MyFoxAbstractSceneEntity):
    def __init__(self, coordinator: MyFoxCoordinator, device: BaseScene, title: str, key: str):
        super().__init__(coordinator, device, title, key)

    async def async_activate(self, **kwargs: Any) -> None:
        """Handle the button press."""
        coordinator: MyFoxCoordinator = self.coordinator
        await coordinator.playScenario(self.idx)


class BaseSwitchEntity(SwitchEntity, BaseSceneWithValueEntity):
    def __init__(self, coordinator: MyFoxCoordinator, device: BaseScene, title: str, key: str):
        super().__init__(coordinator, device, title, key)

    def _update_value(self, val: Any) -> bool:
        self._attr_is_on = bool(self.coordinator.data[self.idx])
        return True

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        coordinator: MyFoxCoordinator = self.coordinator
        await coordinator.enableScenario(self.idx)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        coordinator: MyFoxCoordinator = self.coordinator
        await coordinator.disableScenario(self.idx)


class OnDemandSceneEntity(BaseSceneEntity) :
    """ """


class ActivabledSceneEntity(BaseSwitchEntity) :
    """ """
