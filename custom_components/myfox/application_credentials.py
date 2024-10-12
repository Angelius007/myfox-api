"""Application Credentials platform the MyFox integration."""
import logging

from homeassistant.components.application_credentials import ClientCredential
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .api.oauth import MyFoxImplementation

_LOGGER = logging.getLogger(__name__)

async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    _LOGGER.debug("Init MyFoxImplementation for credential %s", str(credential))
    return MyFoxImplementation(
        hass,
        auth_domain,
        credential,
    )

