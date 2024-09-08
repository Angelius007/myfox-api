import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from homeassistant.const import (
    Platform,
)

from .api.const import (
    KEY_CLIENT_ID,
    KEY_CLIENT_SECRET,
    KEY_MYFOX_USER,
    KEY_MYFOX_PSWD,
    KEY_ACCESS_TOKEN,
    KEY_REFRESH_TOKEN,
    KEY_EXPIRE_IN,
    KEY_EXPIRE_TIME,
    KEY_SITE_ID
)
from .api.myfoxapi import (
    MyFoxEntryDataApi,
    MyFoxApiClient
)

from .api.myfoxapi_camera import (MyFoxApiCameraClient)
from .api.myfoxapi_light import (MyFoxApiLightClient)
from .api.myfoxapi_security import (MyFoxApiSecurityClient)
from .api.myfoxapi_scenario import (MyFoxApiSecenarioClient)
from .api.myfoxapi_sensor import (MyFoxApiSensorClient)
from .api.myfoxapi_sensor_alerte import (MyFoxApiAlerteSensorClient)
from .api.myfoxapi_temperature import (MyFoxApiTemperatureClient)
from .api.myfoxapi_gate import (MyFoxApiGateClient)
from .api.myfoxapi_module import (MyFoxApiModuleClient)
from .api.myfoxapi_shutter import (MyFoxApiShutterClient)
from .api.myfoxapi_socket import (MyFoxApiSocketClient)
from .api.myfoxapi_library import (MyFoxApiLibraryClient)
from .api.myfoxapi_group_electric import (MyFoxApiGroupElectricClient)
from .api.myfoxapi_group_shutter import (MyFoxApiGroupShutterClient)
from .api.myfoxapi_heater import (MyFoxApiHeaterClient)
from .api.myfoxapi_thermo import (MyFoxApThermoClient)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)


from .devices import (BaseDevice)
from .devices.camera import (MyFoxCamera)
from .devices.gate import (MyFoxGate)
from .devices.heater import (MyFoxHeater)
from .devices.module import (MyFoxModule)
from .devices.light import (MyFoxLightSensor)
from .devices.sensor import (MyFoxGenerictSensor, MyFoxDeviceWithState)
from .devices.temperature import (MyFoxTemperatureRecord, MyFoxTemperatureSensor)
from .devices.shutter import MyFoxShutter
from .devices.socket import MyFoxSocket
from .devices.librairie import (MyFoxImage, MyFoxVideo)
from .devices.group import (MyFoxGroupElectric, MyFoxGroupShutter)

from .const import (DOMAIN_MYFOX, CONFIG_VERSION)


_LOGGER = logging.getLogger(__name__)

_PLATFORMS = {
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BUTTON
}

async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrate old entry."""


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if DOMAIN_MYFOX not in hass.data:
        hass.data[DOMAIN_MYFOX] = {}
    
    myfox_info = MyFoxEntryDataApi(entry.data[KEY_CLIENT_ID],
                                   entry.data[KEY_CLIENT_SECRET],
                                   entry.data[KEY_MYFOX_USER],
                                   entry.data[KEY_MYFOX_PSWD],
                                   entry.data[KEY_ACCESS_TOKEN],
                                   entry.data[KEY_REFRESH_TOKEN],
                                   entry.data[KEY_EXPIRE_IN],
                                   entry.data[KEY_EXPIRE_TIME])
    myfox_client = MyFoxApiClient(myfox_info)
    
    info_site = await myfox_client.getInfoSite(entry.data[KEY_SITE_ID])
    _LOGGER.info("Chargement du site %s", str(info_site))
     
    if info_site :
        """Recherche des devices."""
        _LOGGER.info("Chargement du site")

        coordinator = MyFoxCoordinator(hass)
        hass.data[DOMAIN_MYFOX][entry.entry_id] = coordinator
        # cameraCount: int = 0
        if myfox_client.myfox_info.site.cameraCount > 0 :
            await addCamera(hass, entry, myfox_info)
        # gateCount: int = 0
        if myfox_client.myfox_info.site.gateCount > 0 :
            await addGate(hass, entry, myfox_info)
        # shutterCount: int = 0
        if myfox_client.myfox_info.site.shutterCount > 0 :
            await addShutter(hass, entry, myfox_info)
        # socketCount: int = 0
        if myfox_client.myfox_info.site.socketCount > 0 :
            await addSocket(hass, entry, myfox_info)
        # moduleCount: int = 0
        if myfox_client.myfox_info.site.moduleCount > 0 :
            await addModule(hass, entry, myfox_info)
        # heaterCount: int = 0
        if myfox_client.myfox_info.site.heaterCount > 0 :
            await addHeater(hass, entry, myfox_info)
        # scenarioCount: int = 0
        if myfox_client.myfox_info.site.scenarioCount > 0 :
            await addScenario(hass, entry, myfox_info)
        # deviceStateCount: int = 0
        if myfox_client.myfox_info.site.deviceStateCount > 0 :
            await addDeviceState(hass, entry, myfox_info)
        # deviceLightCount: int = 0
        if myfox_client.myfox_info.site.deviceLightCount > 0 :
            await addDeviceLight(hass, entry, myfox_info)
        # deviceDetectorCount: int = 0
        if myfox_client.myfox_info.site.deviceDetectorCount > 0 :
            await addDetectorDevice(hass, entry, myfox_info)
        # Sondes de temperature
        if myfox_client.myfox_info.site.deviceTemperatureCount > 0 :
            await addTemperatureDevice(hass, entry, myfox_info)

        # prepa coordinator
        await coordinator.async_config_entry_first_refresh()

        new_data = {**entry.data}
        # mise a jour du token
        new_data[KEY_ACCESS_TOKEN]  = myfox_info.access_token
        new_data[KEY_REFRESH_TOKEN] = myfox_info.refresh_token
        new_data[KEY_EXPIRE_IN]     = myfox_info.expires_in
        new_data[KEY_EXPIRE_TIME]   = myfox_info.expires_time
        
        hass.config_entries.async_update_entry(entry, data=new_data, options=entry.options)
        await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)
        entry.async_on_unload(entry.add_update_listener(update_listener))
        return True
    else :
        _LOGGER.warn("Pas de site trouve pour l'identifiant %s",entry.data[KEY_SITE_ID])
        return False

async def addCamera(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Camera")
    pass

async def addGate(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Gate")
    pass

async def addShutter(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Shutter")
    await addClientToCoordinator(hass, entry, MyFoxApiShutterClient(myfox_info))
    _LOGGER.debug("Add Group Shutter")
    await addClientToCoordinator(hass, entry, MyFoxApiGroupShutterClient(myfox_info))
    
async def addSocket(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Socket")
    await addClientToCoordinator(hass, entry, MyFoxApiSocketClient(myfox_info))
    _LOGGER.debug("Add Group Socket")
    await addClientToCoordinator(hass, entry, MyFoxApiGroupElectricClient(myfox_info))

async def addModule(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Module")
    pass

async def addHeater(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Heater")
    await addClientToCoordinator(hass, entry, MyFoxApiHeaterClient(myfox_info))

async def addScenario(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Scenario")
    pass

async def addDeviceState(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add State Device")
    pass

async def addDeviceLight(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Light Device")
    await addClientToCoordinator(hass, entry, MyFoxApiLightClient(myfox_info))

async def addDetectorDevice(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Detector Device")
    await addClientToCoordinator(hass, entry, MyFoxApiAlerteSensorClient(myfox_info))

async def addTemperatureDevice(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    _LOGGER.debug("Add Temperature Device")
    await addClientToCoordinator(hass, entry, MyFoxApiTemperatureClient(myfox_info))

async def addClientToCoordinator(hass: HomeAssistant, entry: ConfigEntry, client:MyFoxApiClient) :
    """" """
    _LOGGER.debug("-> Get devices")
    liste_capteurs = await client.getList()
    for capteur in liste_capteurs :
        _LOGGER.debug("Configuration device " + str(capteur))
        deviceId = 0
        label = ""
        modelId = 0
        modelLabel = ""
        if "deviceId" in capteur :
            deviceId = capteur["deviceId"]
        elif "groupId" in capteur :
            deviceId = capteur["groupId"]
        if "label" in capteur :
            label = capteur["label"]
        if "modelId" in capteur :
            modelId = capteur["modelId"]
        if "modelLabel" in capteur :
            modelLabel = capteur["modelLabel"]
        elif "type" in capteur :
            modelLabel = capteur["type"]

        client.configure_device(deviceId, label, modelId, modelLabel)

    if liste_capteurs.__len__() > 0 :
        coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX][entry.entry_id]
        coordinator.add_client(client)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    if not await hass.config_entries.async_unload_platforms(entry, _PLATFORMS):
        return False

    coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX].pop(entry.entry_id)
    for (type,hassclient) in coordinator.myfoxApiClient.items() :
        client: MyFoxApiClient = hassclient
        client.stop()
    coordinator.stop()
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
