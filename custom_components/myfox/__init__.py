import logging

from homeassistant.const import (
    Platform,
)
_LOGGER = logging.getLogger(__name__)

DOMAIN = "ecoflow_cloud"
CONFIG_VERSION = 1

_PLATFORMS = {
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BUTTON
}
