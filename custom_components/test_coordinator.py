import logging
import logging.config

import pytest
import asyncio
import json

from asyncio import AbstractEventLoop

from myfox.api.myfoxapi import (MyFoxPolicy, MyFoxEntryDataApi, MyFoxApiClient)
from myfox.api.myfoxapi_camera import (MyFoxApiCameraClient)
from myfox.api.myfoxapi_light import (MyFoxApiLightClient)
from myfox.api.myfoxapi_security import (MyFoxApiSecurityClient)
from myfox.api.myfoxapi_scenario import (MyFoxApiSecenarioClient)
from myfox.api.myfoxapi_sensor import (MyFoxApiSensorClient)
from myfox.api.myfoxapi_sensor_generic import (MyFoxApiGenericSensorClient)
from myfox.api.myfoxapi_temperature import (MyFoxApiTemperatureClient)
from myfox.api.myfoxapi_gate import (MyFoxApiGateClient)
from myfox.api.myfoxapi_module import (MyFoxApiModuleClient)
from myfox.api.myfoxapi_shutter import (MyFoxApiShutterClient)
from myfox.api.myfoxapi_socket import (MyFoxApiSocketClient)
from myfox.api.myfoxapi_library import (MyFoxApiLibraryClient)
from myfox.api.myfoxapi_group_electric import (MyFoxApiGroupElectricClient)
from myfox.api.myfoxapi_group_shutter import (MyFoxApiGroupShutterClient)
from myfox.api.myfoxapi_heater import (MyFoxApHeaterClient)
from myfox.api.myfoxapi_thermo import (MyFoxApThermoClient)


from myfox.devices.camera import (MyFoxCamera)
from myfox.devices.gate import (MyFoxGate)
from myfox.devices.heater import (MyFoxHeater)
from myfox.devices.module import (MyFoxModule)
from myfox.devices.light import (MyFoxLightSensor)
from myfox.devices.sensor import (MyFoxGenerictSensor, MyFoxDeviceWithState)
from myfox.devices.temperature import (MyFoxTemperatureRecord, MyFoxTemperatureSensor)
from myfox.devices.shutter import MyFoxShutter
from myfox.devices.socket import MyFoxSocket
from myfox.devices.librairie import (MyFoxImage, MyFoxVideo)
from myfox.devices.group import (MyFoxGroupElectric, MyFoxGroupShutter)
from myfox.devices.site import (MyFoxSite)


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

    def writeCache(myfox_info:MyFoxEntryDataApi) :
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
                    
        myfox_info = MyFoxEntryDataApi(client_id, client_secret, myxof_user, myfox_pswd,
                        access_token, refresh_token, expires_in, expires_time, MyFoxSite(site_id))
        _LOGGER.info(str(myfox_info))
        return myfox_info

class TestClients :

    def testClient(loop : AbstractEventLoop, client : MyFoxApiClient, forceInit : bool = True):
        # results = loop.run_until_complete(asyncio.gather(*[client.getInfoSites(forceInit)]))
        # _LOGGER.info("results:"+str(results))
        # site_list = list()
        # for site in results[0]:
        #     site_list.append(site.key)

        results = loop.run_until_complete(asyncio.gather(*[client.getInfoSite(1326, forceInit)]))
        _LOGGER.info("results:"+str(results))

        # results = loop.run_until_complete(asyncio.gather(*[client.refreshToken()]))
        #_LOGGER.info("results:"+str(results))
        
        #results = loop.run_until_complete(asyncio.gather(*[client.getHistory()]))
        #_LOGGER.info("results:"+str(results))
        

    def testScenario(loop : AbstractEventLoop, client : MyFoxApiSecenarioClient):

        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.disableScenario(219)]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.enableScenario(219)]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.playScenario(321)]))
        _LOGGER.info("results:"+str(results))

    def testSecurity(loop : AbstractEventLoop, client : MyFoxApiSecurityClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getSecurity()]))
        _LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("armed")]))
        #_LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("partial")]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("disarmed")]))
        _LOGGER.info("results:"+str(results))

    def testCamera(loop : AbstractEventLoop, client : MyFoxApiCameraClient):
        #results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        #_LOGGER.info("results:"+str(results))
        #camera = results[0][0]
        #camera.protocol = "rtmp"
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStart(1027535)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveExtend(1027535)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStop(1027535)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraPreviewTake(1027535)]))
        #_LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.cameraSnapshotTake(1027535)]))
        _LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraRecordingStart(1027535)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraRecordingStop(1027535)]))
        #_LOGGER.info("results:"+str(results))

    def testLightSensor(loop : AbstractEventLoop, client : MyFoxApiLightClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))
        #camera = results[0][0]
        #camera.protocol = "rtmp"
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStart(65714)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveExtend(65714)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStop(65714)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.cameraPreviewTake(65714)]))
        #_LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.getLightHistory(65714)]))
        _LOGGER.info("results:"+str(results))

    def testGenericSensor(loop : AbstractEventLoop, client : MyFoxApiGenericSensorClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))

    def testSensor(loop : AbstractEventLoop, client : MyFoxApiSensorClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.getDeviceWithState(123)]))
        # _LOGGER.info("results:"+str(results))

    def testTemperatureSensor(loop : AbstractEventLoop, client : MyFoxApiTemperatureClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results[0]))

        for capteur in results[0] :
            print(str(capteur))
            #capteur.
            client.configure_device(capteur["deviceId"],capteur["label"],capteur["modelId"],capteur["modelLabel"])
            #device = MyFoxTemperatureSensor(65714, "device", 0, "xx", "")
            results = loop.run_until_complete(asyncio.gather(*[client.getTemperature(capteur["deviceId"])]))
            _LOGGER.info("results:"+str(results))

    def testGate(loop : AbstractEventLoop, client : MyFoxApiGateClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.performeOne(65714)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.performeTwo(65714)]))
        #_LOGGER.info("results:"+str(results))

    def testModule(loop : AbstractEventLoop, client : MyFoxApiModuleClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))

    def testShutter(loop : AbstractEventLoop, client : MyFoxApiShutterClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setFavorite(947805)]))
        # _LOGGER.info("results:"+str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setOpen(947805)]))
        # _LOGGER.info("results:"+str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setClose(947805)]))
        # _LOGGER.info("results:"+str(results))

    def testSocket(loop : AbstractEventLoop, client : MyFoxApiSocketClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.setOff(2262)]))
        #_LOGGER.info("results:"+str(results))
        # results = loop.run_until_complete(asyncio.gather(*[client.setOn(2262)]))
        #_LOGGER.info("results:"+str(results))

    def testLibrairie(loop : AbstractEventLoop, client : MyFoxApiLibraryClient):
        #results = loop.run_until_complete(asyncio.gather(*[client.getImageList()]))
        #_LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.getVideoList()]))
        _LOGGER.info("results:"+str(results))
        #device = MyFoxVideo(2262, "A1 - Lampe séjour", 19, "Prise électrique commandée DIO First")

    def testGroupElectric(loop : AbstractEventLoop, client : MyFoxApiGroupElectricClient):
        #results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        #_LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOff(24467)]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOn(24467)]))
        _LOGGER.info("results:"+str(results))

    def testGroupShutter(loop : AbstractEventLoop, client : MyFoxApiGroupShutterClient):
        #results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        #_LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOpen(24389)]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setClose(24389)]))
        _LOGGER.info("results:"+str(results))

    def testHeater(loop : AbstractEventLoop, client : MyFoxApHeaterClient):
        #results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        #_LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setEco(66172)]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setFrost(66172)]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOn(66172)]))
        _LOGGER.info("results:"+str(results))
        results = loop.run_until_complete(asyncio.gather(*[client.setOff(66172)]))
        _LOGGER.info("results:"+str(results))

    def testThermo(loop : AbstractEventLoop, client : MyFoxApThermoClient):
        results = loop.run_until_complete(asyncio.gather(*[client.getList()]))
        _LOGGER.info("results:"+str(results))


        #results = loop.run_until_complete(asyncio.gather(*[client.setAuto(66172)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.setAway(66172)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.setBoost(66172)]))
        #_LOGGER.info("results:"+str(results))
        #results = loop.run_until_complete(asyncio.gather(*[client.setOff(66172)]))
        #_LOGGER.info("results:"+str(results))

if __name__ == "__main__" :
    _LOGGER.info("**** Debut ****")
    asyncio.set_event_loop_policy(MyFoxPolicy())
    loop = asyncio.get_event_loop()
    
    _LOGGER.info("-> Lecture du cache ")
    myfox_info = MyFoxCache.getMyFoxEntryDataFromCache()

    try :        
        #TestClients.testClient(loop, MyFoxApiClient(myfox_info), True) # , True
        # TestClients.testScenario(loop, MyFoxApiSecenarioClient(myfox_info))
        # TestClients.testSecurity(loop, MyFoxApiSecurityClient(myfox_info))
        # TestClients.testCamera(loop, MyFoxApiCameraClient(myfox_info))
        # TestClients.testLightSensor(loop, MyFoxApiLightClient(myfox_info))
        # TestClients.testGenericSensor(loop, MyFoxApiGenericSensorClient(myfox_info))
        # TestClients.testSensor(loop, MyFoxApiSensorClient(myfox_info))
        TestClients.testTemperatureSensor(loop, MyFoxApiTemperatureClient(myfox_info))
        # TestClients.testGate(loop, MyFoxApiGateClient(myfox_info))
        # TestClients.testModule(loop, MyFoxApiModuleClient(myfox_info))
        # TestClients.testShutter(loop, MyFoxApiShutterClient(myfox_info))
        # TestClients.testSocket(loop, MyFoxApiSocketClient(myfox_info))
        # TestClients.testLibrairie(loop, MyFoxApiLibraryClient(myfox_info))
        # TestClients.testGroupElectric(loop, MyFoxApiGroupElectricClient(myfox_info))
        # TestClients.testGroupShutter(loop, MyFoxApiGroupShutterClient(myfox_info))
        # TestClients.testHeater(loop, MyFoxApHeaterClient(myfox_info))
        #TestClients.testThermo(loop, MyFoxApThermoClient(myfox_info))

    finally :
        _LOGGER.info("-> Sauvegarde du cache ")
        MyFoxCache.writeCache(myfox_info)
        _LOGGER.info("**** Fin ****")

