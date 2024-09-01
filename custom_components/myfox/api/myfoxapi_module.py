import logging

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices.module import MyFoxModule

from .const import (
    MYFOX_DEVICE_MODULE_LIST,
    MYFOX_DEVICE_MODULE_PERFORM_ONE,
    MYFOX_DEVICE_MODULE_PERFORM_TWO
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiModuleClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.module = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_MODULE_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]
            _LOGGER.debug("getList : %s",str(items))

            for item in items :
                self.module.append(MyFoxModule(item["deviceId"],
                                                       item["label"],
                                                       item["modelId"],
                                                       item["modelLabel"]))

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def performeOne(self, device:MyFoxModule) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_MODULE_PERFORM_ONE % (self.myfox_info.site.siteId, device.deviceId))
            _LOGGER.debug("performeOne : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def performeTwo(self, device:MyFoxModule) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_MODULE_PERFORM_TWO % (self.myfox_info.site.siteId, device.deviceId))
            _LOGGER.debug("performeTwo : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
