import logging.config

import pytest

from custom_components.myfox.api.myfoxapi_exception import MyFoxException
from custom_components.myfox.api.myfoxapi_security import (MyFoxApiSecurityClient)

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
async def test_client_security_list():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecurityClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.getList
        _LOGGER.info("getList(1):" + str(results))
        assert results.__len__() == 1

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
async def test_client_security_get():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecurityClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.getSecurity()
        _LOGGER.info("getSecurity(1):" + str(results))
        assert "statusLabel" in results and results['statusLabel'] == "disarmed"

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
async def test_client_security_armed():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecurityClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # play scenario
        results = await client.setSecurity("armed")
        _LOGGER.info("setSecurity(armed):" + str(results))
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
async def test_client_security_partial():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecurityClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # play scenario
        results = await client.setSecurity("partial")
        _LOGGER.info("setSecurity(partial):" + str(results))
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
async def test_client_security_disarmed():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecurityClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # play scenario
        results = await client.setSecurity("disarmed")
        _LOGGER.info("setSecurity(disarmed):" + str(results))
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
