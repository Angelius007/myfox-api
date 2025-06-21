# tests/utils.py
from aiohttp import hdrs
from aiohttp.hdrs import CONTENT_DISPOSITION
from types import SimpleNamespace
import base64
import json
import logging.config
from multidict import CIMultiDictProxy, CIMultiDict
import secrets
from unittest.mock import MagicMock

from custom_components.myfox.api import (MyFoxEntryDataApi, MyFoxOptionsDataApi)
from custom_components.myfox.devices.site import (MyFoxSite)

logging.config.fileConfig('logging.conf', None, True)
_LOGGER = logging.getLogger(__name__)


class FakeResponse():
    """Objet qui imite aiohttp.ClientResponse pour async with."""
    def __init__(self, status: int, payload: dict, content_type: str = "application/json", filename: str = "Null", binary_data: bytes = None):
        self.status = status
        self._payload = payload
        self._binary_data = binary_data
        self._filename = filename

        _h = CIMultiDict()
        _h[hdrs.CONTENT_TYPE] = content_type

        # Header HTTP typique pour forcer un download de fichier
        if content_type == "binary" :
            self.headers = CIMultiDict({
                CONTENT_DISPOSITION: f'attachment; filename="{filename}"'
            })
            self.content_disposition = SimpleNamespace(filename=filename)
        else :
            self.headers: CIMultiDictProxy[str] = CIMultiDictProxy(_h)
        self.reason = ""

    async def json(self):
        return self._payload

    async def read(self):
        return self._binary_data

    # ---- async context manager ----
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


def fake_http_call(url: str, *args, **kwargs):
    """Route les URL vers des FakeResponse adaptées."""

    print(f"⭐️ fake_http_call for {url}")
    if "oauth2/token" in url:
        token1 = str(base64.b64encode(secrets.token_bytes(32))).replace("==", "")
        token2 = str(base64.b64encode(secrets.token_bytes(32))).replace("==", "")

        return FakeResponse(200, {"status": "OK", "access_token": token1, "refresh_token": token2, "expires_in": 3600, "site_id": 1234})

    elif "v2/site/1234/device/2468/socket/on" in url \
            or "v2/site/1234/device/2468/socket/off" in url \
            or "v2/site/1234/device/2468/gate/perform/one" in url \
            or "v2/site/1234/device/2468/gate/perform/two" in url \
            or "v2/site/1234/device/2468/module/perform/one" in url \
            or "v2/site/1234/device/2468/module/perform/two" in url \
            or "v2/site/1234/device/2468/shutter/my" in url \
            or "v2/site/1234/device/2468/shutter/open" in url \
            or "v2/site/1234/device/2468/shutter/close" in url \
            or "v2/site/1234/security/set/armed" in url \
            or "v2/site/1234/security/set/partial" in url \
            or "v2/site/1234/security/set/disarmed" in url \
            or "v2/site/1234/device/123456789/camera/live/extend" in url \
            or "v2/site/1234/device/123456789/camera/live/stop" in url \
            or "v2/site/1234/device/123456789/camera/recording/start" in url \
            or "v2/site/1234/device/123456789/camera/recording/stop" in url \
            or "v2/site/1234/device/123456789/camera/snapshot/take" in url \
            or "v2/site/1234/device/123456789/camera/shutter/close" in url \
            or "v2/site/1234/device/123456789/camera/shutter/open" in url \
            or "v2/site/1234/scenario/123/play" in url or "v2/site/1234/scenario/456/play" in url or "v2/site/1234/scenario/789/play" in url \
            or "v2/site/1234/scenario/123/disable" in url or "v2/site/1234/scenario/456/disable" in url or "v2/site/1234/scenario/789/disable" in url \
            or "v2/site/1234/scenario/123/enable" in url or "v2/site/1234/scenario/456/enable" in url or "v2/site/1234/scenario/789/enable" in url \
            or "v2/site/1234/group/2468/electric/on" in url or "v2/site/1234/group/2468/electric/off" in url \
            or "v2/site/1234/group/2468/shutter/close" in url or "v2/site/1234/group/2468/shutter/open" in url \
            or "v2/site/1234/device/2468/heater/eco" in url or "v2/site/1234/device/2468/heater/frost" in url  \
            or "v2/site/1234/device/2468/heater/on" in url or "v2/site/1234/device/2468/heater/off" in url  \
            or "v2/site/1234/device/2468/heater/auto" in url or "v2/site/1234/device/2468/heater/away" in url  \
            or "v2/site/1234/device/2468/heater/boost" in url or "v2/site/1234/device/2468/heater/thermostatoff" in url :
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"request": "OK"}
                                  })

    elif "v2/client/site/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload" :
                                      {"items": [
                                          {
                                              "siteId" : 1234,
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

    elif "v2/site/1234/scenario/items" in url:
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
    elif "v2/site/1234/scenario" in url and "/play" in url:
        return FakeResponse(200, {"status": "KO", "error" : "404", "error_description" : "Unknown scenario ID"})
    elif "v2/site/1234/security" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload": {
                                      "status": 1,
                                      "statusLabel": "disarmed"
                                  }
                                  })
    elif "v2/site/1234/device/camera/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId" : 123456789,
                                              "label" : "camera mock",
                                              "resolutionHeight": 800,
                                              "resolutionWidth": 600,
                                              "modelId" : 5,
                                              "modelLabel" : "Panasonic BL-C131"
                                          },
                                          {
                                              "deviceId" : 123456788,
                                              "label" : "camera mock 2",
                                              "resolutionHeight": 800,
                                              "resolutionWidth": 600,
                                              "modelId" : 5,
                                              "modelLabel" : "Panasonic BL-C131"
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/123456789/camera/live/start" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {
                                          "GUID": "2468",
                                          "location": "here",
                                          "protocol": "hls"
                                      }
                                  })
    elif "v2/site/1234/device/123456789/camera/preview/take" in url:
        return FakeResponse(200, {"status": "OK",
                                  "binary": "xxx",
                                  "filename": "mock.jpg"
                                  }, "binary", "fichier_mock.jpg", b"abcd")
    elif "v2/site/1234/device/data/light/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId" : 123456789,
                                              "label" : "Capteur mock 1",
                                              "modelId" : 29,
                                              "light" : 2,
                                              "modelLabel" : "Capteur température & luminosité"
                                          },
                                          {
                                              "deviceId" : 123456788,
                                              "label" : "Capteur mock 2",
                                              "modelId" : 29,
                                              "light" : 5,
                                              "modelLabel" : "Capteur température & luminosité"
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/123456789/data/light" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 123456789,
                                              "level": 4,
                                              "recordedAt": 111
                                          },
                                          {
                                              "deviceId": 123456789,
                                              "level": 3,
                                              "recordedAt": 112
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/data/other/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId" : 12356,
                                              "label": "label mock 1",
                                              "state" : 1,
                                              "modelId": 99,
                                              "modelLabel": "model mock"
                                          },
                                          {
                                              "deviceId" : 12357,
                                              "label": "label mock 2",
                                              "state" : 1,
                                              "modelId": 99,
                                              "modelLabel": "model mock"
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/data/state/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 24689,
                                              "label": "state",
                                              "stateLabel": "opened",
                                              "modelId": 99,
                                              "modelLabel": "item"
                                          },
                                          {
                                              "deviceId": 24688,
                                              "label": "state",
                                              "stateLabel": "closed",
                                              "modelId": 99,
                                              "modelLabel": "item"
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/24689/data/state" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {
                                          "deviceId": 24689,
                                          "stateLabel": "opened"
                                      }
                                  })
    elif "v2/site/1234/device/data/temperature/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 123456,
                                              "label": "Capteur Salon",
                                              "modelId": 29,
                                              "modelLabel": "Capteur température & luminosité",
                                              "lastTemperature": 24,
                                              "lastTemperatureAt": '2024-08-20T17:43:46Z'
                                          },
                                          {
                                              "deviceId": 67891,
                                              "label": "Capteur Sejour",
                                              "modelId": 29,
                                              "modelLabel": "Capteur température & luminosité",
                                              "lastTemperature": 25,
                                              "lastTemperatureAt": '2024-08-20T17:43:46Z'
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/123456/data/temperature" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 123456,
                                              "celsius": 24,
                                              "recordedAt": '2024-08-20T17:43:46Z'
                                          },
                                          {
                                              "deviceId": 123456,
                                              "celsius": 25,
                                              "recordedAt": '2024-08-20T17:45:46Z'
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/gate/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 2468,
                                              "label": "Gate 1",
                                              "modelId": 31,
                                              "modelLabel": "gate",
                                          },
                                          {
                                              "deviceId": 2469,
                                              "label": "Gate 2",
                                              "modelId": 31,
                                              "modelLabel": "gate",
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/module/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 2468,
                                              "label": "Module 1",
                                              "modelId": 32,
                                              "modelLabel": "module",
                                          },
                                          {
                                              "deviceId": 2469,
                                              "label": "Module 2",
                                              "modelId": 32,
                                              "modelLabel": "module",
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/shutter/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 2468,
                                              "label": "Volet 1",
                                              "modelId": 14,
                                              "modelLabel": "Module DIO pour volet",
                                          },
                                          {
                                              "deviceId": 2469,
                                              "label": "Volet 2",
                                              "modelId": 14,
                                              "modelLabel": "Module DIO pour volet",
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/socket/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 2468,
                                              "label": "A2",
                                              "modelId": 18,
                                              "modelLabel": "Prise électrique commandée",
                                          },
                                          {
                                              "deviceId": 2469,
                                              "label": "A1",
                                              "modelId": 19,
                                              "modelLabel": "Prise électrique commandée DIO First",
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/library/image/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "imageId" : 2468,
                                              "cameraId" : 0,
                                              "cameraLabel" : "camera",
                                              "height" : 800,
                                              "width": 600,
                                              "createdAt": '2024-08-20T17:45:46Z',
                                              "fileURL": "https://fakeurl.com/toto"
                                          },
                                          {
                                              "imageId" : 2469,
                                              "cameraId" : 0,
                                              "cameraLabel" : "camera",
                                              "height" : 800,
                                              "width": 600,
                                              "createdAt": '2024-08-20T17:45:46Z',
                                              "fileURL": "https://fakeurl.com/toto"
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/library/video/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "videoId" : 2468,
                                              "cameraId" : 0,
                                              "cameraLabel" : "camera",
                                              "duration": 30,
                                              "height" : 800,
                                              "width": 600,
                                              "isRecording": False,
                                              "createdAt": '2024-08-20T17:45:46Z',
                                              "fileURL": "https://fakeurl.com/toto",
                                              "playURL": "https://fakeurl.com/toto",
                                              "previewURL": "https://fakeurl.com/toto"
                                          },
                                          {
                                              "videoId" : 2469,
                                              "cameraId" : 0,
                                              "cameraLabel" : "camera",
                                              "duration": 30,
                                              "height" : 800,
                                              "width": 600,
                                              "isRecording": False,
                                              "createdAt": '2024-08-20T17:45:46Z',
                                              "fileURL": "https://fakeurl.com/toto",
                                              "playURL": "https://fakeurl.com/toto",
                                              "previewURL": "https://fakeurl.com/toto"
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/library/video/2468/play" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {
                                          "videoId" : 2468,
                                          "location" : "https://fakeurl.com/toto",
                                          "protocol" : "hls",
                                      }
                                  })
    elif "v2/site/1234/group/electric/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "groupId": 2468,
                                              "label": "Lampes",
                                              "type": "Electrical devices",
                                              "modelLabel": "Prise électrique commandée",
                                              "devices" : [
                                                  {
                                                      "deviceId": 2468,
                                                      "label": "Lampe1",
                                                      "modelId": 18,
                                                      "modelLabel": "Prise électrique commandée"
                                                  },
                                                  {
                                                      "deviceId": 2469,
                                                      "label": "Lampe2",
                                                      "modelId": 18,
                                                      "modelLabel": "Prise électrique commandée"
                                                  }
                                              ]
                                          },
                                          {
                                              "groupId": 2469,
                                              "label": "Lampes 2",
                                              "type": "Electrical devices",
                                              "modelLabel": "Prise électrique commandée",
                                              "devices" : [
                                                  {
                                                      "deviceId": 2468,
                                                      "label": "Lampe1",
                                                      "modelId": 18,
                                                      "modelLabel": "Prise électrique commandée"
                                                  },
                                                  {
                                                      "deviceId": 2469,
                                                      "label": "Lampe2",
                                                      "modelId": 18,
                                                      "modelLabel": "Prise électrique commandée"
                                                  }
                                              ]
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/group/shutter/items" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "groupId": 2468,
                                              "label": "Volets 1",
                                              "type": "Shutters",
                                              "devices" : [
                                                  {
                                                      "deviceId": 2468,
                                                      "label": "Volet1",
                                                      "modelId": 14,
                                                      "modelLabel": "DIO module for shutter"
                                                  },
                                                  {
                                                      "deviceId": 2469,
                                                      "label": "Volet2",
                                                      "modelId": 14,
                                                      "modelLabel": "DIO module for shutter"
                                                  }
                                              ]
                                          },
                                          {
                                              "groupId": 2469,
                                              "label": "Volets 2",
                                              "type": "Shutters",
                                              "devices" : [
                                                  {
                                                      "deviceId": 2468,
                                                      "label": "Volet1",
                                                      "modelId": 14,
                                                      "modelLabel": "DIO module for shutter"
                                                  },
                                                  {
                                                      "deviceId": 2469,
                                                      "label": "Volet2",
                                                      "modelId": 14,
                                                      "modelLabel": "DIO module for shutter"
                                                  }
                                              ]
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/device/heater/items" in url or "v2/site/1234/device/heater/items/withthermostat" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "deviceId": 2468,
                                              "label": "Radiateur 1",
                                              "modelId": 44,
                                              "modelLabel": "Module chauffage",
                                              "modeLabel": "wired",
                                              "stateLabel": "on",
                                              "lastTemperature": 25
                                          },
                                          {
                                              "deviceId": 2469,
                                              "label": "Radiateur 2",
                                              "modelId": 44,
                                              "modelLabel": "Module chauffage",
                                              "modeLabel": "wired",
                                              "stateLabel": "on",
                                              "lastTemperature": 25
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/history" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                          {
                                              "logId": 2468,
                                              "label": "log1",
                                              "type": "security",
                                              "createdAt": '2024-08-20T17:45:46Z'
                                          },
                                          {
                                              "logId": 2469,
                                              "label": "log2",
                                              "type": "scenario",
                                              "createdAt": '2024-08-20T17:45:46Z'
                                          }
                                      ]}
                                  })
    elif "v2/site/1234/xxx" in url:
        return FakeResponse(200, {"status": "OK",
                                  "payload":
                                      {"items": [
                                      ]}
                                  })

    print(f"⭐️ fake_http_call : No mock founded for {url}")
    return FakeResponse(404, {"status": "KO", "error": "Service not implemented", "error_description" : "No Mock found"})


class FakeClientSession:
    def __init__(self, *args, **kwargs):
        self.get = MagicMock(side_effect=fake_http_call)
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
            f = open("init_cache.txt", "r")
            data = f.read()
            _LOGGER.debug("Cache : " + data)
            f.close()
            return json.loads(data)
        except Exception:
            try:
                f = open("tests/init_cache.txt", "r")
                data = f.read()
                _LOGGER.debug("Cache : " + data)
                f.close()
                return json.loads(data)
            except Exception as exception:
                _LOGGER.error("Erreur chargement du cache", exception)

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
        site_id = 1234
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
                                       expires_time=expires_time, site=MyFoxSite(siteId=site_id))
        options = MyFoxOptionsDataApi()
        myfox_info.options = options
        print(f"⭐️ getMyFoxEntryDataFromCache.myfox_info: {data} -> {myfox_info}")
        _LOGGER.info(str(myfox_info))
        return myfox_info
