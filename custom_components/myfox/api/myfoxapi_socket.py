import logging
from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_DEVICE_SOCKET_LIST,
    MYFOX_DEVICE_SOCKET_ON,
    MYFOX_DEVICE_SOCKET_OFF
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiSocketClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "socket"
        self.module = list()
        self.module_time = 0

    def stop(self) -> bool:
        super().stop()
        self.module.clear()
        return True
    
    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.module_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_SOCKET_LIST % (self.myfox_info.site.siteId))
                items = response["payload"]["items"]
                _LOGGER.debug("getList : %s",str(items))
                self.module = items

                #for item in items :
                #    self.module.append(MyFoxSocket(item["deviceId"],
                #                                           item["label"],
                #                                           item["modelId"],
                #                                           item["modelLabel"]))

            else :
                _LOGGER.debug("MyFoxApiSocketClient.getList -> Cache ")
                
            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOn(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SOCKET_ON % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setOn : %s",str(response))

            return (response["status"] == "OK")
        
        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOff(self, deviceId:int) -> list:
        """ Get security site """
        try:
            _LOGGER.debug("Device : %s", str(deviceId))
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SOCKET_OFF % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setOff : %s",str(response))

            _LOGGER.debug("Response : %s", str(response))
            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            print("Error : " + str(exception))
            raise MyFoxException(exception)
