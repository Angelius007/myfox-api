import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_DEVICE_HEATER_THERMO_LIST,
    MYFOX_DEVICE_HEATER_THERMO_SET_AUTO,
    MYFOX_DEVICE_HEATER_THERMO_SET_AWAY,
    MYFOX_DEVICE_HEATER_THERMO_SET_BOOST,
    MYFOX_DEVICE_HEATER_THERMO_SET_OFF
)
_LOGGER = logging.getLogger(__name__)


class MyFoxApThermoClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "thermo"
        self.heater = list()
        self.heater_time = 0

    def stop(self) -> bool:
        super().stop()
        self.heater.clear()
        return True

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.heater_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_HEATER_THERMO_LIST % (self.myfox_info.site.siteId))
                _LOGGER.debug(str(response))
                items = response["payload"]["items"]
                _LOGGER.debug("getList : %s", str(items))
                self.heater = items
                self.heater_time = time.time()

            else :
                _LOGGER.debug("MyFoxApThermoClient.getList -> Cache ")

            return self.heater

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def setAuto(self, deviceId: int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_AUTO % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.heater_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def setAway(self, deviceId: int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_AWAY % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.heater_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def setBoost(self, deviceId: int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_BOOST % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.heater_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def setOff(self, deviceId: int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_OFF % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.heater_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
