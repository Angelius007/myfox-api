"""Provide oauth implementations for the MyFox integration."""
import logging
import base64
import hashlib
import secrets
from typing import Any

from homeassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow
from .const import (
    KEY_GRANT_TYPE, GRANT_TYPE_PASSWORD, GRANT_TYPE_AUTHORIZATION_CODE,
    KEY_MYFOX_USER, KEY_MYFOX_PSWD,
     
      DEFAULT_MYFOX_URL_API, MYFOX_TOKEN_PATH, MYFOX_AUTORIZE_PATH
)
from ..const import (
    DOMAIN_MYFOX
)
_LOGGER = logging.getLogger(__name__)

class MyFoxSystemImplementation(config_entry_oauth2_flow.LocalOAuth2Implementation):
    """Tesla Fleet API open source Oauth2 implementation."""

    code_verifier: str
    code_challenge: str

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize open source Oauth2 implementation."""

        # Setup PKCE
        self.code_verifier = secrets.token_urlsafe(32)
        hashed_verifier = hashlib.sha256(self.code_verifier.encode()).digest()
        self.code_challenge = (
            base64.urlsafe_b64encode(hashed_verifier).decode().replace("=", "")
        )
        url_autorize = f"{DEFAULT_MYFOX_URL_API}{MYFOX_AUTORIZE_PATH}"
        url_token = f"{DEFAULT_MYFOX_URL_API}{MYFOX_TOKEN_PATH}"
        super().__init__(
            hass,
            DOMAIN_MYFOX,
            "CLIENT_ID",
            "",
            url_autorize,
            url_token,
        )

    @property
    def name(self) -> str:
        """Name of the implementation."""
        return "Built-in open source client ID"

    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra data that needs to be appended to the authorize url."""
        return {
    #        "code_challenge": self.code_challenge,  # PKCE
        }

    async def async_resolve_external_data(self, external_data: Any) -> dict:
        """Resolve the authorization code to tokens."""
        return await self._token_request(
            {
                "grant_type": GRANT_TYPE_PASSWORD,
                "code": external_data["code"],
                KEY_MYFOX_USER: external_data[KEY_MYFOX_USER],
                KEY_MYFOX_PSWD: external_data[KEY_MYFOX_PSWD],
                "redirect_uri": external_data["state"]["redirect_uri"]
            }
        )


class MyFoxImplementation(AuthImplementation):
    """Tesla Fleet API user Oauth2 implementation."""

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
#    @property
#    def extra_authorize_data(self) -> dict[str, Any]:
#        """Extra data that needs to be appended to the authorize url."""
#        return {KEY_GRANT_TYPE: GRANT_TYPE_AUTHORIZATION_CODE}