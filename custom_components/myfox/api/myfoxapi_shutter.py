import logging

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_DEVICE_SHUTTER_LIST,
    MYFOX_DEVICE_SHUTTER_MY,
    MYFOX_DEVICE_SHUTTER_OPEN,
    MYFOX_DEVICE_SHUTTER_CLOSE
)

_LOGGER = logging.getLogger(__name__)

class MyFoxApiShutterClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.module = list()
        self.client_key = "shutter"

    def stop(self) -> bool:
        super().stop()
        self.module.clear()
        return True

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_SHUTTER_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]
            _LOGGER.debug("getList : %s",str(items))
            self.module = items
            #for item in items :
            #    self.module.append(MyFoxShutter(item["deviceId"],
            #                                           item["label"],
            #                                           item["modelId"],
            #                                           item["modelLabel"]))

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setFavorite(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SHUTTER_MY % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setFavorite : %s",str(response))

            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOpen(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SHUTTER_OPEN % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setOpen : %s",str(response))

            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setClose(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SHUTTER_CLOSE % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setClose : %s",str(response))

            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)