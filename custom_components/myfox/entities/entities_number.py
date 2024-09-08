import logging

from homeassistant.components.number import NumberEntity

from ..entities import BaseWithValueEntity

_LOGGER = logging.getLogger(__name__)

## ////////////////////////////////////////////////////////////////////////////
## DEVICES
## ////////////////////////////////////////////////////////////////////////////

class BaseNumberEntity(NumberEntity, BaseWithValueEntity):
    pass

