import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_DEVICE_MODULE_LIST,
    MYFOX_DEVICE_MODULE_PERFORM_ONE,
    MYFOX_DEVICE_MODULE_PERFORM_TWO
)
_LOGGER = logging.getLogger(__name__)


class MyFoxApiModuleClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "module"
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
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_MODULE_LIST % (self.myfox_info.site.siteId))
                items = response["payload"]["items"]
                _LOGGER.debug("getList : %s", str(items))
                self.module = items
                self.module_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiModuleClient.getList -> Cache ")

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def performeOne(self, deviceId: int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_MODULE_PERFORM_ONE % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.module_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def performeTwo(self, deviceId: int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_MODULE_PERFORM_TWO % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.module_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
