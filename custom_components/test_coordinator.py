import asyncio
import json

from myfox.myfoxapi import (MyFoxPolicy, MyFoxEntryDataApi, MyFoxApiClient)
from myfox.myfoxapi_camera import (MyFoxApiCameraClient)
from myfox.devices.camera import (MyFoxCamera)
from myfox.myfoxapi_light import (MyFoxApiLightClient)
from myfox.devices.light import (MyFoxLightSensor)
from myfox.myfoxapi_security import (MyFoxApiSecurityClient)
from myfox.myfoxapi_scenario import (MyFoxApiSecenarioClient)

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
        "siteId"         : myfox_info.siteId
    }
    f.write(json.dumps(data))
    f.close()

def readCache() :
    try :
        f = open("cache.txt", "r")
        data = f.read()
        print("Cache : " + data)
        f.close()
        return json.loads(data)
    except Exception :
        try:
            f = open("cache_save.txt", "r")
            data = f.read()
            print("Cache : " + data)
            f.close()
            return json.loads(data)
        except Exception : 
            f = open("init_cache.txt", "r")
            data = f.read()
            print("Cache : " + data)
            f.close()
            return json.loads(data)

def getMyFoxEntryDataFromCache() -> MyFoxEntryDataApi:
    data = readCache()
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
    if "siteId" in data:
        siteId = data["siteId"]
    
    myfox_info = MyFoxEntryDataApi(client_id, client_secret, myxof_user, myfox_pswd,
                      access_token, refresh_token, expires_in, expires_time, siteId)
    return myfox_info

def getClient(loop = None, myfox_info:MyFoxEntryDataApi = None) -> MyFoxApiClient :

    client = MyFoxApiClient(myfox_info)

    if not loop :
        loop = asyncio.get_event_loop()

    writeCache(client.myfox_info)

    return client

def getClientCamera(loop = None, myfox_info:MyFoxEntryDataApi = None) -> MyFoxApiCameraClient :

    client = MyFoxApiCameraClient(myfox_info)

    if not loop :
        loop = asyncio.get_event_loop()

    writeCache(client.myfox_info)

    return client

def getClientLight(loop = None, myfox_info:MyFoxEntryDataApi = None) -> MyFoxApiLightClient :

    client = MyFoxApiLightClient(myfox_info)

    if not loop :
        loop = asyncio.get_event_loop()

    writeCache(client.myfox_info)

    return client

def getClientSecurity(loop = None, myfox_info:MyFoxEntryDataApi = None) -> MyFoxApiSecurityClient :

    client = MyFoxApiSecurityClient(myfox_info)

    if not loop :
        loop = asyncio.get_event_loop()

    writeCache(client.myfox_info)

    return client

def getClientScenario(loop = None, myfox_info:MyFoxEntryDataApi = None) -> MyFoxApiSecenarioClient :

    client = MyFoxApiSecenarioClient(myfox_info)

    if not loop :
        loop = asyncio.get_event_loop()

    writeCache(client.myfox_info)

    return client

def testClient(loop, client):
    results = loop.run_until_complete(asyncio.gather(*[client.getInfoSite()]))
    print("results:"+str(results))

    # results = loop.run_until_complete(asyncio.gather(*[client.refreshToken()]))
    #print("results:"+str(results))
    
    #results = loop.run_until_complete(asyncio.gather(*[client.getHistory()]))
    #print("results:"+str(results))
    

def testScenario(loop, client):
    results = loop.run_until_complete(asyncio.gather(*[client.disableScenario(219)]))
    print("results:"+str(results))
    results = loop.run_until_complete(asyncio.gather(*[client.enableScenario(219)]))
    print("results:"+str(results))
    results = loop.run_until_complete(asyncio.gather(*[client.playScenario(321)]))
    print("results:"+str(results))

def testSecurity(loop, client):
    results = loop.run_until_complete(asyncio.gather(*[client.getSecurity()]))
    print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("armed")]))
    #print("results:"+str(results))
    results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("partial")]))
    print("results:"+str(results))
    results = loop.run_until_complete(asyncio.gather(*[client.setSecurity("disarmed")]))
    print("results:"+str(results))

def testCamera(loop, client):
    #results = loop.run_until_complete(asyncio.gather(*[client.getCamera()]))
    #print("results:"+str(results))
    #camera = results[0][0]
    #camera.protocol = "rtmp"
    camera = MyFoxCamera(1027535, "camera", 0, "xx", False)
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStart(camera)]))
    #print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveExtend(camera)]))
    #print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStop(camera)]))
    #print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraPreviewTake(camera)]))
    #print("results:"+str(results))
    results = loop.run_until_complete(asyncio.gather(*[client.cameraSnapshotTake(camera)]))
    print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraRecordingStart(camera)]))
    #print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraRecordingStop(camera)]))
    #print("results:"+str(results))

def testLightSensor(loop, client):
    results = loop.run_until_complete(asyncio.gather(*[client.getLightList()]))
    print("results:"+str(results))
    #camera = results[0][0]
    #camera.protocol = "rtmp"
    light = MyFoxLightSensor(65714, "capteur", 0, "xx", 2)
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStart(camera)]))
    #print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveExtend(camera)]))
    #print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraLiveStop(camera)]))
    #print("results:"+str(results))
    #results = loop.run_until_complete(asyncio.gather(*[client.cameraPreviewTake(camera)]))
    #print("results:"+str(results))
    results = loop.run_until_complete(asyncio.gather(*[client.getLightHistory(light)]))
    print("results:"+str(results))

if __name__ == "__main__" :
    print("**** Debut ****")
    asyncio.set_event_loop_policy(MyFoxPolicy())
    loop = asyncio.get_event_loop()
    
    myfox_info = getMyFoxEntryDataFromCache()

    try :
        client = getClient(loop, myfox_info)
        clientScenario = getClientScenario(loop, myfox_info)
        clientSecurity = getClientSecurity(loop, myfox_info)
        clientCamera = getClientCamera(loop, myfox_info)
        clientLight = getClientLight(loop, myfox_info)
        testClient(loop, clientScenario)
        # testScenario(loop, clientScenario)
        # testSecurity(loop, clientSecurity)
        # testCamera(loop, clientCamera)
        # testLightSensor(loop, clientLight)

    finally :
        writeCache(client.myfox_info)
        print("**** Fin ****")


