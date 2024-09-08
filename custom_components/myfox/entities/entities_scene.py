import logging

from typing import Any

from homeassistant.components.scene import Scene
from ..entities import MyFoxAbstractSceneEntity
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)
from ..scenes import BaseScene

_LOGGER = logging.getLogger(__name__)
 
## ////////////////////////////////////////////////////////////////////////////
## SCENES
## ////////////////////////////////////////////////////////////////////////////

class BaseSceneEntity(Scene, MyFoxAbstractSceneEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseScene, title: str, key: str):
        super().__init__(coordinator, device, title, key)

    async def async_activate(self, **kwargs: Any) -> None:
        """Handle the button press."""
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.processScenario()

class OnDemandSceneEntity(BaseSceneEntity) :
    """ """

class ActivabledSceneEntity(BaseSceneEntity) :
    """ """