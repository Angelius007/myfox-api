import logging

from homeassistant.components.switch import SwitchEntity

from entity import MyFoxAbstractDeviceEntity

_LOGGER = logging.getLogger(__name__)

## ////////////////////////////////////////////////////////////////////////////
## DEVICES
## ////////////////////////////////////////////////////////////////////////////

class BaseSwitchEntity(SwitchEntity, MyFoxAbstractDeviceEntity):
    pass
