"""Provide oauth implementations for the MyFox integration."""
import logging

from homeassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from .const import (
   DEFAULT_MYFOX_URL_API, MYFOX_TOKEN_PATH, MYFOX_AUTORIZE_PATH
)
_LOGGER = logging.getLogger(__name__)

class MyFoxImplementation(AuthImplementation):
    """MyFox API user Oauth2 implementation."""

    def __init__(
        self, hass: HomeAssistant, auth_domain: str, credential: ClientCredential
    ) -> None:
        """Initialize user Oauth2 implementation."""

        url_autorize = f"{DEFAULT_MYFOX_URL_API}{MYFOX_AUTORIZE_PATH}"
        url_token = f"{DEFAULT_MYFOX_URL_API}{MYFOX_TOKEN_PATH}"
        
        super().__init__(
            hass,
            auth_domain,
            credential,
            AuthorizationServer(url_autorize, url_token),
        )

    async def async_refresh_token(self, token: dict) -> dict:
        """ Rafraichissement token"""
        _LOGGER.debug("Refresh Old Token %s", str(token) )
        new_token =  await super().async_refresh_token(token)
        _LOGGER.debug("New Token %s", str(new_token) )
        return new_token
