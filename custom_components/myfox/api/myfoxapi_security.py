from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_SECURITY_GET, MYFOX_SECURITY_SET
)

class MyFoxApiSecurityClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)

    async def getSecurity(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_SECURITY_GET % (self.myfox_info.site.siteId))
            statutSecurity = response["payload"]["statusLabel"]
            # {'status': 'OK', 'timestamp': 1723759973, 'payload': {'status': 1, 'statusLabel': 'disarmed'}
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
            # {'status': 'OK', 'timestamp': 1723759985, 'payload': {'request': 'OK'}}
            return (response["payload"]["statusLabel"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)