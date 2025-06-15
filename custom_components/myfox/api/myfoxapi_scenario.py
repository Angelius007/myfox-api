import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_SCENARIO_ITEMS, MYFOX_SCENARIO_ENABLE, MYFOX_SCENARIO_DISABLE, MYFOX_SCENARIO_PLAY
)

_LOGGER = logging.getLogger(__name__)


class MyFoxApiSecenarioClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "scenario"
        self.scenarii = list()
        self.scenarii_time = 0

    def stop(self) -> bool:
        super().stop()
        self.scenarii.clear()
        return True

    async def getList(self):
        """ Recuperation scenarios """
        try:
            if self.isCacheExpire(self.scenarii_time) :
                response = await self.callMyFoxApiGet(MYFOX_SCENARIO_ITEMS % self.myfox_info.site.siteId)
                items = response["payload"]["items"]
                _LOGGER.debug("getScenarii : %s", str(items))
                self.scenarii = items
                self.scenarii_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiSecenarioClient.getList -> Cache ")

            return self.scenarii

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def enableScenario(self, scenarioId: int):
        """ Enable scenario """
        try:
            response = await self.callMyFoxApiPost(MYFOX_SCENARIO_ENABLE % (self.myfox_info.site.siteId , scenarioId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.scenarii_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def disableScenario(self, scenarioId: int):
        """ Disable scenario """
        try:
            response = await self.callMyFoxApiPost(MYFOX_SCENARIO_DISABLE % (self.myfox_info.site.siteId , scenarioId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.scenarii_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def playScenario(self, scenarioId: int):
        """ Play scenario """
        try:
            response = await self.callMyFoxApiPost(MYFOX_SCENARIO_PLAY % (self.myfox_info.site.siteId , scenarioId))
            _LOGGER.debug("Response : %s", str(response))

            statut_ok = ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.scenarii_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
