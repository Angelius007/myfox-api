import logging.config

import pytest

from custom_components.myfox.api.myfoxapi_exception import MyFoxException
from custom_components.myfox.api.myfoxapi_state import (MyFoxApiStateClient)

from tests.utils import MyFoxMockCache, FakeClientSession
from custom_components.myfox.crypto.secure import encode

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
async def test_client_state_list():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiStateClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.getList()
        _LOGGER.info("getList(1):" + str(results))
        assert results.__len__() == 2

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        _LOGGER.error(exception)
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")


@pytest.mark.asyncio
async def test_client_state():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiStateClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.getDeviceWithState(24689)
        _LOGGER.info("getDeviceWithState(1):" + str(results))
        assert results is not None and results["stateLabel"] == "opened"

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        _LOGGER.error(exception)
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")
