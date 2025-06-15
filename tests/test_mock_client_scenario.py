import logging.config

import pytest


from custom_components.myfox.api.myfoxapi_exception import MyFoxException
from custom_components.myfox.api.myfoxapi_scenario import (MyFoxApiSecenarioClient)

from tests.utils import MyFoxMockCache, FakeClientSession

logging.config.fileConfig('logging.conf', None, True)
_LOGGER = logging.getLogger(__name__)

PATCHES = [
    "custom_components.myfox.api.myfoxapi.aiohttp.ClientSession",
]


@pytest.fixture(autouse=True)
def patch_aiohttp(monkeypatch):
    for target in PATCHES:
        monkeypatch.setattr(target, FakeClientSession, raising=True)


@pytest.mark.asyncio
async def test_client_scenario_list():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecenarioClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.getList()
        _LOGGER.info("getList(1):" + str(results))
        assert results.__len__() == 3

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        _LOGGER.debug(exception)
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")


@pytest.mark.asyncio
async def test_client_scenario_play():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecenarioClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # play scenario
        results = await client.playScenario(123)
        _LOGGER.info("playScenario(123):" + str(results))
        assert results is True
        results = await client.playScenario(456)
        _LOGGER.info("playScenario(456):" + str(results))
        assert results is True
        results = await client.playScenario(789)
        _LOGGER.info("playScenario(789):" + str(results))
        assert results is True
        try:
            results = await client.playScenario(101112)
            _LOGGER.info("playScenario(101112):" + str(results))
        except MyFoxException as exception:
            assert exception.status == 999
            assert exception.message == "Error : 404 - Description: Unknown scenario ID"
        # disable
        results = await client.disableScenario(456)
        _LOGGER.info("disableScenario(456):" + str(results))
        assert results is True
        # enable
        results = await client.enableScenario(456)
        _LOGGER.info("enableScenario(456):" + str(results))
        assert results is True

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        _LOGGER.debug(exception)
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")


@pytest.mark.asyncio
async def test_client_scenario_enable():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecenarioClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # enable
        results = await client.enableScenario(456)
        _LOGGER.info("enableScenario(456):" + str(results))
        assert results is True

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        _LOGGER.debug(exception)
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")


@pytest.mark.asyncio
async def test_client_scenario_disable():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecenarioClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # disable
        results = await client.disableScenario(456)
        _LOGGER.info("disableScenario(456):" + str(results))
        assert results is True

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        _LOGGER.debug(exception)
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")
