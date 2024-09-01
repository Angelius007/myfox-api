import logging

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices.scenario import MyFoxScenario

from .const import (
    MYFOX_SCENARIO_ITEMS, MYFOX_SCENARIO_ENABLE, MYFOX_SCENARIO_DISABLE, MYFOX_SCENARIO_PLAY
)

_LOGGER = logging.getLogger(__name__)

class MyFoxApiSecenarioClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.scenarii = list()


    async def getScenarii(self):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiGet(MYFOX_SCENARIO_ITEMS % self.myfox_info.site.siteId)
            items = response["payload"]["items"]
            _LOGGER.debug("getScenarii : %s",str(items))

            for item in items :
                self.scenarii.append(MyFoxScenario(item["scenarioId"],
                                item["label"],
                                item["typeLabel"],
                                item["enabled"]))

            return self.scenarii

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def enableScenario(self, scenarioId: int):
        """ Enable scenario """
        try:
            response = await self.callMyFoxApiPost(MYFOX_SCENARIO_ENABLE % (self.myfox_info.site.siteId , scenarioId))
            _LOGGER.debug("enableScenario : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def disableScenario(self, scenarioId: int):
        """ Disable scenario """
        try:
            response = await self.callMyFoxApiPost(MYFOX_SCENARIO_DISABLE % (self.myfox_info.site.siteId , scenarioId))
            _LOGGER.debug("disableScenario : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def playScenario(self, scenarioId: int):
        """ Play scenario """
        try:
            response = await self.callMyFoxApiPost(MYFOX_SCENARIO_PLAY % (self.myfox_info.site.siteId , scenarioId))
            _LOGGER.debug("playScenario : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
