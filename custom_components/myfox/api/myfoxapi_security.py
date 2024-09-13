import logging

import time
from .myfoxapi_exception import (MyFoxException)
from .myfoxapi import (MyFoxApiClient, MyFoxEntryDataApi )

from .const import (
    MYFOX_SECURITY_GET, MYFOX_SECURITY_SET
)

_LOGGER = logging.getLogger(__name__)

class MyFoxApiSecurityClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "security"
        self.security = list()
        self.security_time = 0

    def stop(self) -> bool:
        super().stop()
        return True

    async def getList(self) -> list:
        """ Generation d'une entite fictive pour l'alarme """
        if self.isCacheExpire(self.security_time) :
            statutSecurity = await self.getSecurity()
            self.security.clear()
            if "status" in statutSecurity and "statusLabel" in statutSecurity :
                self.security.append({'deviceId': self.myfox_info.site.siteId,
                                    'label': 'Alarme MyFox', 
                                    'modelId': 99, 
                                    'modelLabel': 'Alarme MyFox',
                                    "status" : statutSecurity["status"],
                                    "statusLabel" : statutSecurity["statusLabel"]
                                    })
                self.security_time = time.time()
        else :
            _LOGGER.debug("MyFoxApiSecurityClient.getList -> Cache ")
        return self.security

    async def getSecurity(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_SECURITY_GET % (self.myfox_info.site.siteId))
            statutSecurity = response["payload"]
            _LOGGER.debug("getSecurity : %s",str(statutSecurity))
            # {'status': 'OK', 'timestamp': 1723759973, 'payload': {'status': 1, 'statusLabel': 'disarmed'}
            # 1 : disarmed
            # 2 : partial
            # 4 : armed
            return statutSecurity

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setSecurity(self, securityLevel: str):
        """ Mise a jour security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_SECURITY_SET % (self.myfox_info.site.siteId , securityLevel))
            _LOGGER.debug("setSecurity : %s",str(response))
            # {'status': 'OK', 'timestamp': 1723759985, 'payload': {'request': 'OK'}}
            return (response["payload"]["request"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)