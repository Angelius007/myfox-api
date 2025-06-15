import logging.config

import asyncio
import pytest
import unittest
from unittest.mock import AsyncMock, patch, Mock, MagicMock


from custom_components.myfox.api.myfoxapi import (MyFoxPolicy, MyFoxApiClient)
from custom_components.myfox.api.myfoxapi_exception import MyFoxException
from custom_components.myfox.api.myfoxapi_camera import (MyFoxApiCameraClient)
from custom_components.myfox.api.myfoxapi_light import (MyFoxApiLightClient)
from custom_components.myfox.api.myfoxapi_security import (MyFoxApiSecurityClient)
from custom_components.myfox.api.myfoxapi_scenario import (MyFoxApiSecenarioClient)
from custom_components.myfox.api.myfoxapi_state import (MyFoxApiStateClient)
from custom_components.myfox.api.myfoxapi_state_alerte import (MyFoxApiAlerteStateClient)
from custom_components.myfox.api.myfoxapi_temperature import (MyFoxApiTemperatureClient)
from custom_components.myfox.api.myfoxapi_gate import (MyFoxApiGateClient)
from custom_components.myfox.api.myfoxapi_module import (MyFoxApiModuleClient)
from custom_components.myfox.api.myfoxapi_shutter import (MyFoxApiShutterClient)
from custom_components.myfox.api.myfoxapi_socket import (MyFoxApiSocketClient)
from custom_components.myfox.api.myfoxapi_library import (MyFoxApiLibraryClient)
from custom_components.myfox.api.myfoxapi_group_electric import (MyFoxApiGroupElectricClient)
from custom_components.myfox.api.myfoxapi_group_shutter import (MyFoxApiGroupShutterClient)
from custom_components.myfox.api.myfoxapi_heater import (MyFoxApiHeaterClient)
from custom_components.myfox.api.myfoxapi_thermo import (MyFoxApThermoClient)

from tests.utils import fake_http_call, MyFoxMockCache, FakeClientSession

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
    access_token_initial=myfox_info.access_token
    refresh_token_initial=myfox_info.refresh_token
    try:
        client = MyFoxApiClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        results = await client.login()
        _LOGGER.info("login(1):"+str(results))
        assert results == True
        assert access_token_initial != client.myfox_info.access_token
        assert refresh_token_initial != client.myfox_info.refresh_token
        myfox_info=client.myfox_info

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
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
        _LOGGER.info("getInfoSite(1):"+str(results))
        assert results.siteId == myfox_info.site.siteId

        results = await client.getInfoSites(True)
        _LOGGER.info("getInfoSites(2):"+str(results))
        assert results[0].siteId == myfox_info.site.siteId

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
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
    access_token_initial=myfox_info.access_token
    refresh_token_initial=myfox_info.refresh_token
    try:
        client = MyFoxApiClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1

        results = await client.refreshToken()
        _LOGGER.info("refreshToken(1):"+str(results))
        assert results == True
        assert access_token_initial != client.myfox_info.access_token
        assert refresh_token_initial != client.myfox_info.refresh_token

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")

@pytest.mark.asyncio
async def test_client_scenario():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiSecenarioClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.getList()
        _LOGGER.info("getList(1):"+str(results))
        assert results.__len__() == 3
        # play scenario
        results = await client.playScenario(123)
        _LOGGER.info("playScenario(123):"+str(results))
        assert results == True
        results = await client.playScenario(456)
        _LOGGER.info("playScenario(456):"+str(results))
        assert results == True
        results = await client.playScenario(789)
        _LOGGER.info("playScenario(789):"+str(results))
        assert results == True
        try:
            results = await client.playScenario(101112)
            _LOGGER.info("playScenario(101112):"+str(results))
        except MyFoxException as exception:
            assert exception.status == 999
            assert exception.message == "Error : 404 - Description: Unknown scenario ID"
        # disable
        results = await client.disableScenario(456)
        _LOGGER.info("disableScenario(456):"+str(results))
        assert results == True
        # enable
        results = await client.enableScenario(456)
        _LOGGER.info("enableScenario(456):"+str(results))
        assert results == True

    except MyFoxException as exception:
        _LOGGER.error("Exception: Un mock non implémenté à vérifier")
        assert False
    except Exception as exception:
        _LOGGER.error("Exception", exception)
        assert False
    finally :
        MyFoxMockCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")
