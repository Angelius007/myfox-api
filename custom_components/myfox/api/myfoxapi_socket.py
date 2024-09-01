import logging
from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices.socket import MyFoxSocket

from .const import (
    MYFOX_DEVICE_SOCKET_LIST,
    MYFOX_DEVICE_SOCKET_ON,
    MYFOX_DEVICE_SOCKET_OFF
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiSocketClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.module = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_SOCKET_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.module.append(MyFoxSocket(item["deviceId"],
                                                       item["label"],
                                                       item["modelId"],
                                                       item["modelLabel"]))

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOn(self, device:MyFoxSocket) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SOCKET_ON % (self.myfox_info.site.siteId, device.deviceId))

            return (response["status"] == "OK")
        
        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOff(self, device:MyFoxSocket) -> list:
        """ Get security site """
        try:
            _LOGGER.debug("Device : %s", str(device))
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SOCKET_OFF % (self.myfox_info.site.siteId, device.deviceId))

            _LOGGER.debug("Response : %s", str(response))
            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            print("Error : " + str(exception))
            raise MyFoxException(exception)
