import logging.config

import pytest

from custom_components.myfox.api.myfoxapi_exception import MyFoxException
from custom_components.myfox.api.myfoxapi_camera import (MyFoxApiCameraClient)

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
async def test_client_list():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.getList()
        _LOGGER.info("getList(1):" + str(results))
        assert results.__len__() == 2

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
async def test_client_camera_live_start():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.cameraLiveStart(123456789, "hls")
        _LOGGER.info("cameraLiveStart(1):" + str(results))
        assert "GUID" in results

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
async def test_client_camera_live_extend():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.cameraLiveExtend(123456789)
        _LOGGER.info("cameraLiveExtend(1):" + str(results))
        assert "status" in results and results["status"] == "OK"

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
async def test_client_camera_live_stop():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.cameraLiveStop(123456789)
        _LOGGER.info("cameraLiveStop(1):" + str(results))
        assert "status" in results and results["status"] == "OK"

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
async def test_client_camera_preview_take():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.cameraPreviewTake(123456789)
        _LOGGER.info("cameraPreviewTake(1):" + str(results))
        assert isinstance(results, (bytes, bytearray))

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
async def test_client_camera_snapshot_take():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.cameraSnapshotTake(123456789)
        _LOGGER.info("cameraSnapshotTake(1):" + str(results))
        assert "status" in results and results["status"] == "OK"

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
async def test_client_camera_recording_start():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.cameraRecordingStart(123456789)
        _LOGGER.info("cameraRecordingStart(1):" + str(results))
        assert "status" in results and results["status"] == "OK"

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
async def test_client_camera_recording_stop():
    _LOGGER.info("**** Debut ****")
    myfox_info = MyFoxMockCache.getMyFoxEntryDataFromCache()
    try:
        client = MyFoxApiCameraClient(myfox_info)
        client.nb_retry = 1
        client.delay_between_retry = 1
        # get list
        results = await client.cameraRecordingStop(123456789)
        _LOGGER.info("cameraRecordingStop(1):" + str(results))
        assert "status" in results and results["status"] == "OK"

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
