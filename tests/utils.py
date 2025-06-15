# tests/utils.py
from aiohttp import hdrs
import base64
import json
import logging.config
from multidict import CIMultiDictProxy, CIMultiDict
import secrets
from unittest.mock import AsyncMock, MagicMock

from custom_components.myfox.api import (MyFoxEntryDataApi, MyFoxOptionsDataApi)
from custom_components.myfox.devices.site import (MyFoxSite)

logging.config.fileConfig('logging.conf', None, True)
_LOGGER = logging.getLogger(__name__)

class FakeResponse():
    """Objet qui imite aiohttp.ClientResponse pour async with."""
    def __init__(self, status: int, payload: dict):
        self.status = status
        self._payload = payload
        _h = CIMultiDict()
        _h[hdrs.CONTENT_TYPE] = "application/json"
        self.headers: CIMultiDictProxy[str] = CIMultiDictProxy(_h)
        self.reason = ""

    async def json(self):
        return self._payload

    # ---- async context manager ----
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


def fake_http_call(url: str, *args, **kwargs):
    """Route les URL vers des FakeResponse adaptées."""

    if "oauth2/token" in url:
        token1 = str(base64.b64encode(secrets.token_bytes(32))).replace("==","")
        token2 = str(base64.b64encode(secrets.token_bytes(32))).replace("==","")

        return FakeResponse(200, {"status": "OK", "access_token":token1, "refresh_token":token2, "expires_in":3600, "site_id": 1326})

    elif "v2/client/site/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload" :
                                      {"items": [
                                          {
                                              "siteId" : 1326,
                                              "label" : "Alarme Mock",
                                              "brand" : "Mock",
                                              "timezone" : "Europe/Paris",
                                              "AXA" : "Non",
                                              "cameraCount" : 1,
                                              "gateCount" : 1,
                                              "shutterCount" : 1,
                                              "socketCount" : 1,
                                              "moduleCount" : 1,
                                              "heaterCount" : 1,
                                              "scenarioCount" : 3,
                                              "deviceTemperatureCount" : 1,
                                              "deviceStateCount" : 1,
                                              "deviceLightCount" : 1,
                                              "deviceDetectorCount" : 1
                                          }
                                      ]}
                                  })

    elif "v2/site/1326/scenario/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload" :
                                      {"items": [
                                          {
                                              "scenarioId" : 123,
                                              "label" : "Scenario Mock 1",
                                              "typeLabel" : "onDemand",
                                              "enabled" : "None"
                                          },
                                          {
                                              "scenarioId" : 456,
                                              "label" : "Scenario Mock 2",
                                              "typeLabel" : "scheduled",
                                              "enabled" : "True"
                                          },
                                          {
                                              "scenarioId" : 789,
                                              "label" : "Scenario Mock 3",
                                              "typeLabel" : "simulation",
                                              "enabled" : "True"
                                          }
                                      ]}
                                  })
    elif "v2/site/1326/scenario/123/play" in url or  "v2/site/1326/scenario/456/play" in url or  "v2/site/1326/scenario/789/play" in url:
        return FakeResponse(200, {"status": "OK"})
    elif "v2/site/1326/scenario" in url and  "/play" in url:
        return FakeResponse(200, {"status": "KO", "error" : "404", "error_description" : "Unknown scenario ID"})
    elif "v2/site/1326/scenario/123/disable" in url or  "v2/site/1326/scenario/456/disable" in url or  "v2/site/1326/scenario/789/disable" in url:
        return FakeResponse(200, {"status": "OK"})
    elif "v2/site/1326/scenario/123/enable" in url or  "v2/site/1326/scenario/456/enable" in url or  "v2/site/1326/scenario/789/enable" in url:
        return FakeResponse(200, {"status": "OK"})
    elif "v2/site/1326/xxx" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                      ]}
                                  })

    return FakeResponse(404, {"status": "KO", "error": "Service not implemented", "error_description" : "No Mock found"})

class FakeClientSession:
    def __init__(self, *args, **kwargs):
        self.get  = MagicMock(side_effect=fake_http_call)
        self.post = MagicMock(side_effect=fake_http_call)
        print(f"⭐️ FakeClientSession constructed via {__name__}")


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None

class MyFoxMockCache :
    @staticmethod
    def readCache():
        try:
            f = open("cache_mock.txt", "r")
            data = f.read()
            _LOGGER.debug("Cache : " + data)
            f.close()
            return json.loads(data)
        except Exception:
            try:
                f = open("cache_save.txt", "r")
                data = f.read()
                _LOGGER.debug("Cache : " + data)
                f.close()
                return json.loads(data)
            except Exception:
                f = open("init_cache.txt", "r")
                data = f.read()
                _LOGGER.debug("Cache : " + data)
                f.close()
                return json.loads(data)

    @staticmethod
    def writeCache(myfox_info: MyFoxEntryDataApi):
        f = open("cache_mock.txt", "w")
        data = {
            "CLIENT_ID": myfox_info.client_id,
            "CLIENT_SECRET": myfox_info.client_secret,
            "MYFOX_USER": myfox_info.username,
            "MYFOX_PSWD": myfox_info.password,
            "access_token": myfox_info.access_token,
            "refresh_token": myfox_info.refresh_token,
            "expires_time": myfox_info.expires_time,
            "expires_in": myfox_info.expires_in,
            "site_id": myfox_info.site.siteId
        }
        f.write(json.dumps(data))
        f.close()

    @staticmethod
    def getMyFoxEntryDataFromCache() -> MyFoxEntryDataApi:
        data = MyFoxMockCache.readCache()
        client_id = ""
        client_secret = ""
        myfox_user = ""
        myfox_pswd = ""
        access_token = ""
        refresh_token = ""
        expires_in = 0
        expires_time = 0.0
        site_id = 0
        if "CLIENT_ID" in data:
            client_id = data["CLIENT_ID"]
        if "CLIENT_SECRET" in data:
            client_secret = data["CLIENT_SECRET"]
        if "MYFOX_USER" in data:
            myfox_user = data["MYFOX_USER"]
        if "MYFOX_PSWD" in data:
            myfox_pswd = data["MYFOX_PSWD"]
        if "access_token" in data:
            access_token = data["access_token"]
        if "refresh_token" in data:
            refresh_token = data["refresh_token"]
        if "expires_in" in data:
            expires_in = data["expires_in"]
        if "expires_time" in data:
            expires_time = data["expires_time"]
        if "site_id" in data:
            site_id = int(data["site_id"])

        myfox_info = MyFoxEntryDataApi(client_id=client_id, client_secret=client_secret, username=myfox_user,
                                       password=myfox_pswd,
                                       access_token=access_token, refresh_token=refresh_token, expires_in=expires_in,
                                       expires_time=expires_time, site=MyFoxSite(site_id))
        options = MyFoxOptionsDataApi()
        myfox_info.options = options
        _LOGGER.info(str(myfox_info))
        return myfox_info
