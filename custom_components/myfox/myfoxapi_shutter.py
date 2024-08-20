from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from .devices.shutter import MyFoxShutter

from .const import (
    MYFOX_DEVICE_SHUTTER_LIST,
    MYFOX_DEVICE_SHUTTER_MY,
    MYFOX_DEVICE_SHUTTER_OPEN,
    MYFOX_DEVICE_SHUTTER_CLOSE
)

class MyFoxApiShutterClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.module = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_SHUTTER_LIST % (self.myfox_info.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.module.append(MyFoxShutter(item["deviceId"],
                                                       item["label"],
                                                       item["modelId"],
                                                       item["modelLabel"]))

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setFavorite(self, device:MyFoxShutter) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SHUTTER_MY % (self.myfox_info.siteId, device.deviceId))

            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOpen(self, device:MyFoxShutter) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SHUTTER_OPEN % (self.myfox_info.siteId, device.deviceId))

            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setClose(self, device:MyFoxShutter) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_SHUTTER_CLOSE % (self.myfox_info.siteId, device.deviceId))

            return (response["status"] == "OK")

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)