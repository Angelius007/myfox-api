from typing import Final

DOMAIN: Final = "myfox"

DEFAULT_MYFOX_URL_API = "https://api.myfox.me/"

KEY_CLIENT_ID = "client_id"
KEY_CLIENT_SECRET = "client_secret"
KEY_MYFOX_USER = "username"
KEY_MYFOX_PSWD = "password"
KEY_ACCESS_TOKEN = "access_token"
KEY_REFRESH_TOKEN = "refresh_token"
KEY_EXPIRE_IN = "expires_in"
KEY_GRANT_TYPE = "grant_type"

GRANT_TYPE_PASSWORD="password"
GRANT_REFRESH_TOKEN="refresh_token"

# token
MYFOX_TOKEN_PATH = "oauth2/token"
# sites
MYFOX_INFO_SITE_PATH = "v2/client/site/items" #List available sites for the current user
MYFOX_HISTORY_GET= "v2/site/%i/history" #Get site history
# scenarios
MYFOX_SCENARIO_ITEMS = "v2/site/%i/scenario/items"
MYFOX_SCENARIO_PLAY = "v2/site/%i/scenario/%i/play"
MYFOX_SCENARIO_ENABLE = "v2/site/%i/scenario/%i/enable"
MYFOX_SCENARIO_DISABLE = "v2/site/%i/scenario/%i/disable"
# security
MYFOX_SECURITY_GET = "v2/site/%i/security"
MYFOX_SECURITY_SET = "v2/site/%i/security/set/%s"
# camera
MYFOX_CAMERA_LIST = "v2/site/%i/device/camera/items" #List camera devices
MYFOX_CAMERA_LIVE_EXTEND="v2/site/%i/device/%i/camera/live/extend" #Add 30 seconds to live streaming
MYFOX_CAMERA_LIVE_START="v2/site/%i/device/%i/camera/live/start/%s" #Start live streaming from a camera (hls / rtmp  )
MYFOX_CAMERA_LIVE_STOP="v2/site/%i/device/%i/camera/live/stop" #Stop live streaming from a camera
MYFOX_CAMERA_PREV_TAKE="v2/site/%i/device/%i/camera/preview/take" #Get a volatile preview from a camera
MYFOX_CAMERA_REC_START="v2/site/%i/device/%i/camera/recording/start" #Start recording from a camera
MYFOX_CAMERA_REC_STOP="v2/site/%i/device/%i/camera/recording/stop" #Stop recording from a camera
MYFOX_CAMERA_SHUTTER_CLOSE="v2/site/%i/device/%i/camera/shutter/close" #Open shutter for Myfox Security Camera
MYFOX_CAMERA_SHUTTER_OPEN="v2/site/%i/device/%i/camera/shutter/open" #Open shutter for Myfox Security Camera
MYFOX_CAMERA_SNAP_TAKE="v2/site/%i/device/%i/camera/snapshot/take" #Take a snapshot from a camera and save it in the library
# device data light
MYFOX_LIGHT_LIST = "v2/site/%i/device/data/light/items" #List all light sensor featured devices
MYFOX_LIGHT_HISTORY = "v2/site/%i/device/%i/data/light" #Get light measures
# device data other
# get /site/{siteId}/device/data/other/itemsList all generic sensor featured devices
# device data state
# get /site/{siteId}/device/data/state/itemsList devices with state data
# get /site/{siteId}/device/{deviceId}/data/stateGet device state
# device data temperature
# get /site/{siteId}/device/data/temperature/itemsList all temperature sensor featured devices
# get /site/{siteId}/device/{deviceId}/data/temperatureGet temperature measures
# device gate
# get /site/{siteId}/device/gate/itemsList gate devices
# post /site/{siteId}/device/{deviceId}/gate/perform/onePerform action #1
# post /site/{siteId}/device/{deviceId}/gate/perform/twoPerform action #2
# device heater
# get /site/{siteId}/device/heater/itemsList heater devices
# get /site/{siteId}/device/heater/items/withthermostatList heater devices with virtuals thermostats
# post /site/{siteId}/device/{deviceId}/heater/autoSet a thermostat to 'auto' mode
# post /site/{siteId}/device/{deviceId}/heater/awaySet a thermostat to 'away' mode
# post /site/{siteId}/device/{deviceId}/heater/boostSet a thermostat to 'boost' mode
# post /site/{siteId}/device/{deviceId}/heater/ecoSet a heater to 'eco' mode
# post /site/{siteId}/device/{deviceId}/heater/frostSet a heater to 'frost' mode
# post /site/{siteId}/device/{deviceId}/heater/offSet a heater to 'off' mode
# post /site/{siteId}/device/{deviceId}/heater/onSet a heater to 'on' mode
# post /site/{siteId}/device/{deviceId}/heater/thermostatoffSet a thermostat to 'off' mode
# device module
# get /site/{siteId}/device/module/itemsList module devices
# post /site/{siteId}/device/{deviceId}/module/perform/onePerform action #1
# post /site/{siteId}/device/{deviceId}/module/perform/twoPerform action #2
# device shutter
# get /site/{siteId}/device/shutter/itemsList shutter devices
# post /site/{siteId}/device/{deviceId}/shutter/closeClose shutter
# post /site/{siteId}/device/{deviceId}/shutter/mySet shutter to favorite position
# post /site/{siteId}/device/{deviceId}/shutter/openOpen shutter
# device socket
# get /site/{siteId}/device/socket/itemsList socket devices
# post /site/{siteId}/device/{deviceId}/socket/offTurn off a device
# post /site/{siteId}/device/{deviceId}/socket/onTurn on a device
# group electic
# get /site/{siteId}/group/electric/itemsList groups of type electric
# post /site/{siteId}/group/{groupId}/electric/offTurn off all electric devices from a group
# post /site/{siteId}/group/{groupId}/electric/onTurn on all electric devices from a group
# group shutter
# get /site/{siteId}/group/shutter/itemsList groups of type shutter
# post /site/{siteId}/group/{groupId}/shutter/closeClose all shutters from a group
# post /site/{siteId}/group/{groupId}/shutter/openOpen all shutters from a group
# site library
# get /site/{siteId}/library/image/itemsGet all images taken from a site's cameras
# get /site/{siteId}/library/video/itemsGet all videos taken from a site's cameras
# get /site/{siteId}/library/video/{videoId}/playGet video informations for HLS playing


