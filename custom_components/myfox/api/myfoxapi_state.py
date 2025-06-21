import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_DEVICE_STATE_LIST,
    MYFOX_DEVICE_STATE_GET
)

_LOGGER = logging.getLogger(__name__)


class MyFoxApiStateClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "state"
        self.sensor = list()
        self.sensor_time = 0
        self.sensorState = list()
        self.sensorState_time = 0

    def stop(self) -> bool:
        super().stop()
        self.sensor.clear()
        self.sensorState.clear()
        return True

    async def getList(self):
        """ Get security site """
        try:
            if self.isCacheExpire(self.sensor_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_STATE_LIST % self.myfox_info.site.siteId)
                items = response["payload"]["items"]
                _LOGGER.debug("getDeviceWithStateList : %s", str(items))
                self.sensor = items
                self.sensor_time = time.time()
            else :
                _LOGGER.debug("MyFoxApiSensorClient.getList -> Cache ")

            return self.sensor

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def getDeviceWithState(self, deviceId: int):
        """ Get security site """
        try:
            if self.isCacheExpire(self.sensorState_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_STATE_GET % (self.myfox_info.site.siteId, deviceId))
                items = response["payload"]
                _LOGGER.debug("getDeviceWithState : %s", str(items))
                self.sensorState = items
                self.sensorState_time = time.time()
            else :
                _LOGGER.debug("MyFoxApiSensorClient.getDeviceWithState -> Cache ")

            return self.sensorState

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
