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
from .api.myfoxapi_temperature import (MyFoxApiTemperatureClient)
from .api.myfoxapi_gate import (MyFoxApiGateClient)
from .api.myfoxapi_module import (MyFoxApiModuleClient)
from .api.myfoxapi_shutter import (MyFoxApiShutterClient)
from .api.myfoxapi_socket import (MyFoxApiSocketClient)
from .api.myfoxapi_library import (MyFoxApiLibraryClient)
from .api.myfoxapi_group_electric import (MyFoxApiGroupElectricClient)
from .api.myfoxapi_group_shutter import (MyFoxApiGroupShutterClient)
from .api.myfoxapi_heater import (MyFoxApHeaterClient)
from .api.myfoxapi_thermo import (MyFoxApThermoClient)


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

from .const import (DOMAIN, CONFIG_VERSION)


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
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    
    myfox_info = MyFoxEntryDataApi(entry.data[KEY_CLIENT_ID],
                                   entry.data[KEY_CLIENT_SECRET],
                                   entry.data[KEY_MYFOX_USER],
                                   entry.data[KEY_MYFOX_PSWD],
                                   entry.data[KEY_ACCESS_TOKEN],
                                   entry.data[KEY_REFRESH_TOKEN],
                                   entry.data[KEY_EXPIRE_IN],
                                   entry.data[KEY_EXPIRE_TIME])
    myfox_client = MyFoxApiClient(myfox_info)
    
    info_site = await myfox_client.getInfoSite(entry.data[KEY_SITE_ID], True)
    _LOGGER.info("Chargement du site %s", str(info_site))
     
    if info_site :
        """Recherche des devices."""
        _LOGGER.info("Chargement du site")
        hass.data[DOMAIN][entry.entry_id] = {} 
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
    pass

async def addSocket(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Socket")
    pass

async def addModule(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Module")
    pass

async def addHeater(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Heater")
    pass

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
    pass

async def addDetectorDevice(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Detector Device")
    pass

async def addTemperatureDevice(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    _LOGGER.debug("Add Temperature Device")
    client_themperature = MyFoxApiTemperatureClient(myfox_info)
    liste_capteur = await client_themperature.getList()
    for capteur in liste_capteur :
        client_themperature.configure_device(capteur.deviceId, capteur.label, capteur.modelId, capteur.modelLabel)

    if liste_capteur.__len__() > 0 :
        hass.data[DOMAIN][entry.entry_id]["temperature"] = client_themperature


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    if not await hass.config_entries.async_unload_platforms(entry, _PLATFORMS):
        return False

    for (type,hassclient) in hass.data[DOMAIN].pop(entry.entry_id).items() :
        client: MyFoxApiClient = hassclient
        client.stop()
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
