import logging
import time

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_DEVICE_GATE_LIST,
    MYFOX_DEVICE_GATE_PERFORM_ONE,
    MYFOX_DEVICE_GATE_PERFORM_TWO
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiGateClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "gate"
        self.gate = list()
        self.gate_time = 0

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.gate_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_GATE_LIST % (self.myfox_info.site.siteId))
                items = response["payload"]["items"]
                self.gate = items
                self.gate_time = time.time()
                #for item in items :
                #    self.gate.append(MyFoxGate(item["deviceId"],
                #                                           item["label"],
                #                                           item["modelId"],
                #                                           item["modelLabel"]))
            else :
                _LOGGER.debug("MyFoxApiGateClient.getList -> Cache ")

            return self.gate

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def performeOne(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_GATE_PERFORM_ONE % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def performeTwo(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_GATE_PERFORM_TWO % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
