import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_DEVICE_OTHER_LIST
)

_LOGGER = logging.getLogger(__name__)


class MyFoxApiAlerteStateClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "alerte_state_sensor"
        self.sensor = list()
        self.sensor_time = 0

    def stop(self) -> bool:
        super().stop()
        self.sensor.clear()
        return True

    async def getList(self):
        """ Get security site """
        try:
            if self.isCacheExpire(self.sensor_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_OTHER_LIST % self.myfox_info.site.siteId)
                items = response["payload"]["items"]
                _LOGGER.debug("getSensorList : %s", str(items))
                self.sensor = items
                self.sensor_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiAlerteStateClient.getList -> Cache ")

            return self.sensor

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
