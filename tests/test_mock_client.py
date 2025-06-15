import logging.config

import pytest


from custom_components.myfox.api.myfoxapi import MyFoxApiClient
from custom_components.myfox.api.myfoxapi_exception import MyFoxException

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
async def test_client_login():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    access_token_initial = myfox_info.access_token
    refresh_token_initial = myfox_info.refresh_token
    try:
        client = MyFoxApiClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        results = await client.login()
        _LOGGER.info("login(1):" + str(results))
        assert results is True
        assert access_token_initial != client.myfox_info.access_token
        assert refresh_token_initial != client.myfox_info.refresh_token
        myfox_info = client.myfox_info

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
async def test_client_site():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1

        results = await client.getInfoSite(myfox_info.site.siteId, True)
        _LOGGER.info("getInfoSite(1):" + str(results))
        assert results.siteId == myfox_info.site.siteId

        results = await client.getInfoSites(True)
        _LOGGER.info("getInfoSites(2):" + str(results))
        assert results[0].siteId == myfox_info.site.siteId

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
async def test_client_refresh_token():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    access_token_initial = myfox_info.access_token
    refresh_token_initial = myfox_info.refresh_token
    try:
        client = MyFoxApiClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1

        results = await client.refreshToken()
        _LOGGER.info("refreshToken(1):" + str(results))
        assert results is True
        assert access_token_initial != client.myfox_info.access_token
        assert refresh_token_initial != client.myfox_info.refresh_token

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
