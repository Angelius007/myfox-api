import logging

import time
from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)
from ..crypto.secure import decode

from .const import (
    MYFOX_SECURITY_GET, MYFOX_SECURITY_SET
)

_LOGGER = logging.getLogger(__name__)


class MyFoxApiSecurityClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "security"
        self.security = list()
        self.security_time = 0

    def saveMyFoxInfo(self, myfox_info: MyFoxEntryDataApi) :
        super().saveMyFoxInfo(myfox_info)
        self.security_cache_expire_in = myfox_info.options.cache_security_time

    def stop(self) -> bool:
        super().stop()
        return True

    async def getList(self) -> list:
        """ Generation d'une entite fictive pour l'alarme """
        if self.isCacheExpireWithParam(self.security_time, self.security_cache_expire_in) :
            statutSecurity = await self.getSecurity()
            self.security.clear()
            if "status" in statutSecurity and "statusLabel" in statutSecurity:
                self.security.append({'deviceId': self.myfox_info.site.siteId,
                                      'label': 'Alarme MyFox',
                                      'modelId': 99,
                                      'modelLabel': 'Alarme MyFox',
                                      "status": statutSecurity["status"],
                                      "statusLabel": statutSecurity["statusLabel"]
                                      })
                self.security_time = time.time()
        else:
            _LOGGER.debug("MyFoxApiSecurityClient.getList -> Cache ")
        return self.security

    async def getSecurity(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_SECURITY_GET % self.myfox_info.site.siteId)
            statutSecurity = response["payload"]
            _LOGGER.debug("getSecurity : %s", str(statutSecurity))

            return statutSecurity

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def setSecurity(self, securityLevel: str, code: str = None):
        """ Mise a jour security site """
        try:
            if self.myfox_info.options.use_code_alarm:
                codes = decode(self.myfox_info.options.secure_codes, str(self.myfox_info.site.siteId))
                code_trouve = False
                for local_code in codes.split(" ") :
                    if str(code) == str(local_code) :
                        code_trouve = True
                        _LOGGER.debug("Code OK")
                        break
                if not code_trouve :
                    _LOGGER.warning("Code inconnu %s", str(code))
                    raise MyFoxException(401, "Code incorrect")
            response = await self.callMyFoxApiPost(MYFOX_SECURITY_SET % (self.myfox_info.site.siteId , securityLevel))
            _LOGGER.debug("setSecurity : %s", str(response))
            statut_ok = (response["payload"]["request"] == "OK")
            if statut_ok :
                # Force expire cache
                self.security_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
