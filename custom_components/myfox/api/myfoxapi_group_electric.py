import logging
import time

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_GROUP_ELECTRIC_LIST,
    MYFOX_GROUP_ELECTRIC_SET_ON,
    MYFOX_GROUP_ELECTRIC_SET_OFF
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiGroupElectricClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "group_electric"
        self.module = list()
        self.module_time = 0

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.module_time) :
                response = await self.callMyFoxApiGet(MYFOX_GROUP_ELECTRIC_LIST % (self.myfox_info.site.siteId))
                print(str(response))
                items = response["payload"]["items"]
                self.module = items
                self.module_time = time.time()
                #for item in items :
                #    group = MyFoxGroupElectric(item["groupId"],
                #                                item["label"],
                #                                item["type"],
                #                                [])
                #    for device in item["devices"] :
                #        group.devices.append(MyFoxSocket(device["deviceId"],
                #                                            device["label"],
                #                                            device["modelId"],
                #                                            device["modelLabel"]))
                #    self.module.append(group)
            else :
                _LOGGER.debug("MyFoxApiGroupElectricClient.getList -> Cache ")

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOn(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_ELECTRIC_SET_ON % (self.myfox_info.site.siteId, groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOff(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_ELECTRIC_SET_OFF % (self.myfox_info.site.siteId, groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
