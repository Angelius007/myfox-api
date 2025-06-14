import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_LIGHT_LIST, MYFOX_LIGHT_HISTORY
)
_LOGGER = logging.getLogger(__name__)


class MyFoxApiLightClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "light"
        self.ligth = list()
        self.light_time = 0

    def stop(self) -> bool:
        super().stop()
        self.ligth.clear()
        return True

    async def getList(self):
        """ Get security site """
        try:
            if self.isCacheExpire(self.light_time) :
                response = await self.callMyFoxApiGet(MYFOX_LIGHT_LIST % (self.myfox_info.site.siteId))
                items = response["payload"]["items"]
                _LOGGER.debug("getLightList : %s", str(items))
                self.ligth = items
                self.light_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiLightClient.getList -> Cache ")

            return self.ligth

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def getLightHistory(self, deviceId: int):
        """ Mise a jour security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIGHT_HISTORY % (self.myfox_info.site.siteId , deviceId))
            _LOGGER.debug("getLightHistory : %s", str(response))
            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
