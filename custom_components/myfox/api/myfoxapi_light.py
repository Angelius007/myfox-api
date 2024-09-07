import logging

from typing import Type

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices import (BaseDevice)
from ..devices.light import (MyFoxLightDevice)

from .const import (
    MYFOX_LIGHT_LIST, MYFOX_LIGHT_HISTORY
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiLightClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.type :  Type[BaseDevice] | None = MyFoxLightDevice
        self.ligth = list()
        self.client_key = "light"

    def stop(self) -> bool:
        super().stop()
        self.ligth.clear()
        return True

    async def getList(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIGHT_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]
            _LOGGER.debug("getLightList : %s",str(items))
            self.ligth = items

            #for item in items :
            #    self.ligth.append(MyFoxLightSensor(item["deviceId"],
            #                    item["label"],
            #                    item["modelId"],
            #                    item["modelLabel"],
            #                    item["light"]))
            return self.ligth

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def getLightHistory(self, deviceId:int):
        """ Mise a jour security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIGHT_HISTORY % (self.myfox_info.site.siteId , deviceId))
            _LOGGER.debug("getLightHistory : %s",str(response))
            # {'status': 'OK', 'timestamp': 1723759985, 'payload': {'request': 'OK'}}
            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)