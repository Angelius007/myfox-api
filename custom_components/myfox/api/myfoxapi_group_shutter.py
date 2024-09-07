import logging
import time

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_GROUP_SHUTTER_LIST,
    MYFOX_GROUP_SHUTTER_SET_CLOSE,
    MYFOX_GROUP_SHUTTER_SET_OPEN
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiGroupShutterClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "group_shutter"
        self.module = list()
        self.module_time = 0

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.module_time) :
                response = await self.callMyFoxApiGet(MYFOX_GROUP_SHUTTER_LIST % (self.myfox_info.site.siteId))
                print(str(response))
                items = response["payload"]["items"]
                self.module = items
                self.module_time = time.time()
                #for item in items :
                #    group = MyFoxGroupShutter(item["groupId"],
                #                                item["label"],
                #                                item["type"],
                #                                [])
                #    for device in item["devices"] :
                #        group.devices.append(MyFoxShutter(device["deviceId"],
                #                                            device["label"],
                #                                            device["modelId"],
                #                                            device["modelLabel"]))
                #    self.module.append(group)
            else :
                _LOGGER.debug("MyFoxApiGroupShutterClient.getList -> Cache ")

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOpen(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_SHUTTER_SET_OPEN % (self.myfox_info.site.siteId, groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setClose(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_SHUTTER_SET_CLOSE % (self.myfox_info.site.siteId, groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
