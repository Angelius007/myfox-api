import logging
import logging.config

from typing import Any
import asyncio
import json

from asyncio import AbstractEventLoop

from custom_components.myfox.api import (MyFoxEntryDataApi, MyFoxOptionsDataApi)
from custom_components.myfox.api.myfoxapi import (MyFoxPolicy, MyFoxApiClient)
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

from custom_components.myfox.devices.site import (MyFoxSite)


logging.config.fileConfig('logging.conf', None, True)
_LOGGER = logging.getLogger(__name__)


class MyFoxCache() :
    def readCache() :
        try :
            f = open("cache.txt", "r")
            data = f.read()
            _LOGGER.debug("Cache : " + data)
            f.close()
            return json.loads(data)
        except Exception :
            try:
                f = open("cache_save.txt", "r")
                data = f.read()
                _LOGGER.debug("Cache : " + data)
                f.close()
                return json.loads(data)
            except Exception :
                f = open("init_cache.txt", "r")
                data = f.read()
                _LOGGER.debug("Cache : " + data)
                f.close()
                return json.loads(data)

    def writeCache(myfox_info: MyFoxEntryDataApi) :
        f = open("cache.txt", "w")
        data = {
            "CLIENT_ID"      : myfox_info.client_id,
            "CLIENT_SECRET"  : myfox_info.client_secret,
            "MYFOX_USER"     : myfox_info.username,
            "MYFOX_PSWD"     : myfox_info.password,
            "access_token"   : myfox_info.access_token,
            "refresh_token"  : myfox_info.refresh_token,
            "expires_time"   : myfox_info.expires_time,
            "expires_in"     : myfox_info.expires_in,
            "site_id"        : myfox_info.site.siteId
        }
        f.write(json.dumps(data))
        f.close()

    def getMyFoxEntryDataFromCache() -> MyFoxEntryDataApi:
        data = MyFoxCache.readCache()
        if "CLIENT_ID" in data:
            client_id = data["CLIENT_ID"]
        if "CLIENT_SECRET" in data:
            client_secret = data["CLIENT_SECRET"]
        if "MYFOX_USER" in data:
            myxof_user = data["MYFOX_USER"]
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

        myfox_info = MyFoxEntryDataApi(client_id=client_id, client_secret=client_secret,
                                       username=myxof_user, password=myfox_pswd,
                                       access_token=access_token, refresh_token=refresh_token,
                                       expires_in=expires_in, expires_time=expires_time,
                                       site=MyFoxSite(site_id))
        options = MyFoxOptionsDataApi()
        myfox_info.options = options
        _LOGGER.info(str(myfox_info))
        return myfox_info


class TestClients :

    def testClient(self, loop : AbstractEventLoop, client : MyFoxApiClient, forceInit : bool = True):
        # results = loop.run_until_complete(asyncio.gather(*[client.getInfoSites(forceInit)]))
        # _LOGGER.info("results:" + str(results))
        # site_list = list()
        # for site in results[0]:
        #     site_list.append(site.key)
        results = loop.run_until_complete(asyncio.gather(*[client.login()]))[0]
        _LOGGER.info("results:" + str(results))

        results = loop.run_until_complete(asyncio.gather(*[client.getInfoSite(1326, forceInit)]))[0]
        _LOGGER.info("results:" + str(results))

        # results = loop.run_until_complete(asyncio.gather(*[client.refreshToken()]))[0]
        # _LOGGER.info("results:" + str(results))

        # results = loop.run_until_complete(asyncio.gather(*[client.getHistory()]))[0]
        # _LOGGER.info("results:" + str(results))

    def testScenario(self, loop : AbstractEventLoop, client : MyFoxApiSecenarioClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.disableScenario(219)]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.enableScenario(219)]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.playScenario(321)]))[0]
        _LOGGER.info("results:" + str(results))

    def testSecurity(self, loop : AbstractEventLoop, client : MyFoxApiSecurityClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getSecurity()]))[0]
        _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("armed")]))[0]
        # _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("partial")]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("disarmed")]))[0]
        _LOGGER.info("results:" + str(results))

    def testCamera(self, loop : AbstractEventLoop, client : MyFoxApiCameraClient):
        # results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        # _LOGGER.info("results:" + str(results))
        # camera = results[0][0]
        # camera.protocol = "rtmp"
        # results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStart(1027535)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveExtend(1027535)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStop(1027535)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.cameraPreviewTake(1027535)]))[0]
        # _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.cameraSnapshotTake(1027535)]))[0]
        _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.cameraRecordingStart(1027535)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.cameraRecordingStop(1027535)]))[0]
        # _LOGGER.info("results:" + str(results))

    def testLightSensor(self, loop : AbstractEventLoop, client : MyFoxApiLightClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.getLightHistory(65714)]))[0]
        _LOGGER.info("results:" + str(results))

    def testGenericSensor(self, loop : AbstractEventLoop, client : MyFoxApiAlerteStateClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))

    def testSensor(self, loop : AbstractEventLoop, client : MyFoxApiStateClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.getDeviceWithState(123)]))[0]
        # _LOGGER.info("results:" + str(results))

    def testTemperatureSensor(self, loop : AbstractEventLoop, client : MyFoxApiTemperatureClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results[0]))

        for capteur in results :
            _LOGGER.debug(str(capteur))
            # capteur.
            client.configure_device(capteur["deviceId"], capteur["label"], capteur["modelId"], capteur["modelLabel"])
            # device = MyFoxTemperatureSensor(65714, "device", 0, "xx", "")
            # results = loop.run_until_complete(asyncio.gather(*[client.getTemperature(capteur["deviceId"])]))[0]
            # _LOGGER.info("results:" + str(results))

    def testGate(self, loop : AbstractEventLoop, client : MyFoxApiGateClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.performeOne(65714)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.performeTwo(65714)]))[0]
        # _LOGGER.info("results:" + str(results))

    def testModule(self, loop : AbstractEventLoop, client : MyFoxApiModuleClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))

    def testShutter(self, loop : AbstractEventLoop, client : MyFoxApiShutterClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setFavorite(947805)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setOpen(947805)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setClose(947805)]))[0]
        # _LOGGER.info("results:" + str(results))

    def testSocket(self, loop : AbstractEventLoop, client : MyFoxApiSocketClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setOff(2262)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setOn(2262)]))[0]
        # _LOGGER.info("results:" + str(results))

    def testLibrairie(self, loop : AbstractEventLoop, client : MyFoxApiLibraryClient):
        # results = loop.run_until_complete(asyncio.gather(*[client.getImageList()]))[0]
        # _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.getVideoList()]))[0]
        _LOGGER.info("results:" + str(results))

    def testGroupElectric(self, loop : AbstractEventLoop, client : MyFoxApiGroupElectricClient):
        # results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        # _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOff(24467)]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOn(24467)]))[0]
        _LOGGER.info("results:" + str(results))

    def testGroupShutter(self, loop : AbstractEventLoop, client : MyFoxApiGroupShutterClient):
        # results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        # _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOpen(24389)]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setClose(24389)]))[0]
        _LOGGER.info("results:" + str(results))

    def testHeater(self, loop : AbstractEventLoop, client : MyFoxApiHeaterClient):
        # results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        # _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setEco(66172)]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setFrost(66172)]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOn(66172)]))[0]
        _LOGGER.info("results:" + str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOff(66172)]))[0]
        _LOGGER.info("results:" + str(results))

    def testThermo(self, loop : AbstractEventLoop, client : MyFoxApThermoClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))[0]
        _LOGGER.info("results:" + str(results))

        # results = loop.run_until_complete(asyncio.gather(*[client.setAuto(66172)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setAway(66172)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setBoost(66172)]))[0]
        # _LOGGER.info("results:" + str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setOff(66172)]))[0]
        # _LOGGER.info("results:" + str(results))

    def testHistory(self, loop : AbstractEventLoop, client : MyFoxApiClient):
        results = loop.run_until_complete((asyncio.gather(*[client.getHistory(type="security")])))[0]
        _LOGGER.info("results:" + str(results))
        for temp in results:
            _LOGGER.info("temp:" + str(temp))

    def testSetUpdate(self) :
        params = dict[str, Any]()
        listening_idx = set()
        listening_idx.add("72625|lastTemperature")
        listening_idx.add("65714|lastTemperature")
        temp = dict[str, Any]()
        temp["deviceId"] = 72625
        temp["lastTemperature"] = 15.2
        temp["lastTimeTemperature"] = 125252

        TestClients.addToParams(params, listening_idx, temp)

    def addToParams(self, params: dict[str, Any], listening_idx: set, temp: Any):
        """ Ajout des parames de la liste si correspond aux attentes """
        device_id = temp["deviceId"]
        for key, val in temp.items() :
            control_key = str(device_id) + "|" + str(key)
            if control_key in listening_idx:
                params[control_key] = val
                _LOGGER.info("addToParams -> deviceId(%s) : %s [%s]", str(device_id), control_key, str(val))


if __name__ == "__main__" :
    _LOGGER.info("**** Debut ****")
    asyncio.set_event_loop_policy(MyFoxPolicy())
    loop = asyncio.get_event_loop()
    _LOGGER.info("-> Lecture du cache ")
    myfox_info = MyFoxCache.getMyFoxEntryDataFromCache()

    try :
        """ """
        # TestClients.testSetUpdate()
        # TestClients.testClient(loop, MyFoxApiClient(myfox_info), True) # , True
        # TestClients.testScenario(loop, MyFoxApiSecenarioClient(myfox_info))
        # TestClients.testSecurity(loop, MyFoxApiSecurityClient(myfox_info))
        # TestClients.testCamera(loop, MyFoxApiCameraClient(myfox_info))
        # TestClients.testLightSensor(loop, MyFoxApiLightClient(myfox_info))
        # TestClients.testGenericSensor(loop, MyFoxApiAlerteStateClient(myfox_info))
        # TestClients.testSensor(loop, MyFoxApiSensorClient(myfox_info))
        # TestClients.testTemperatureSensor(loop, MyFoxApiTemperatureClient(myfox_info))
        # TestClients.testGate(loop, MyFoxApiGateClient(myfox_info))
        # TestClients.testModule(loop, MyFoxApiModuleClient(myfox_info))
        # TestClients.testShutter(loop, MyFoxApiShutterClient(myfox_info))
        # TestClients.testSocket(loop, MyFoxApiSocketClient(myfox_info))
        # TestClients.testLibrairie(loop, MyFoxApiLibraryClient(myfox_info))
        # TestClients.testGroupElectric(loop, MyFoxApiGroupElectricClient(myfox_info))
        # TestClients.testGroupShutter(loop, MyFoxApiGroupShutterClient(myfox_info))
        # TestClients.testHeater(loop, MyFoxApiHeaterClient(myfox_info))
        # TestClients.testThermo(loop, MyFoxApThermoClient(myfox_info))
        TestClients.testHistory(loop, MyFoxApiClient(myfox_info))
        # TestClients.testEncryptDecrypt(loop)

    finally :
        _LOGGER.info("-> Sauvegarde du cache ")
        MyFoxCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")
