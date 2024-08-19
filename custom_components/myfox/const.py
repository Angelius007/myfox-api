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
MYFOX_DEVICE_OTHER_LIST="v2/site/%i/device/data/other/items" # List all generic sensor featured devices
# device data state
MYFOX_DEVICE_STATE_LIST = "v2/site/%i/device/data/state/items" #List devices with state data
MYFOX_DEVICE_STATE_GET = "v2/site/%i/device/%i/data/state" #Get device state
# device data temperature
# get v2/site/%i/device/data/temperature/items #List all temperature sensor featured devices
# get v2/site/%i/device/{deviceId}/data/temperature #Get temperature measures
# device gate
# get v2/site/%i/device/gate/items #List gate devices
# post v2/site/%i/device/{deviceId}/gate/perform/one #Perform action #1
# post v2/site/%i/device/{deviceId}/gate/perform/two #Perform action #2
# device heater
# get v2/site/%i/device/heater/items #List heater devices
# get v2/site/%i/device/heater/items/withthermostat #List heater devices with virtuals thermostats
# post v2/site/%i/device/{deviceId}/heater/auto #Set a thermostat to 'auto' mode
# post v2/site/%i/device/{deviceId}/heater/away #Set a thermostat to 'away' mode
# post v2/site/%i/device/{deviceId}/heater/boost #Set a thermostat to 'boost' mode
# post v2/site/%i/device/{deviceId}/heater/eco #Set a heater to 'eco' mode
# post v2/site/%i/device/{deviceId}/heater/frost #Set a heater to 'frost' mode
# post v2/site/%i/device/{deviceId}/heater/off #Set a heater to 'off' mode
# post v2/site/%i/device/{deviceId}/heater/on #Set a heater to 'on' mode
# post v2/site/%i/device/{deviceId}/heater/thermostatoff #Set a thermostat to 'off' mode
# device module
# get v2/site/%i/device/module/items #List module devices
# post v2/site/%i/device/{deviceId}/module/perform/one #Perform action #1
# post v2/site/%i/device/{deviceId}/module/perform/two #Perform action #2
# device shutter
# get v2/site/%i/device/shutter/items #List shutter devices
# post v2/site/%i/device/{deviceId}/shutter/close #Close shutter
# post v2/site/%i/device/{deviceId}/shutter/my #Set shutter to favorite position
# post v2/site/%i/device/{deviceId}/shutter/open #Open shutter
# device socket
# get v2/site/%i/device/socket/items #List socket devices
# post v2/site/%i/device/{deviceId}/socket/off #Turn off a device
# post v2/site/%i/device/{deviceId}/socket/on #Turn on a device
# group electic
# get v2/site/%i/group/electric/items #List groups of type electric
# post v2/site/%i/group/{groupId}/electric/off #Turn off all electric devices from a group
# post v2/site/%i/group/{groupId}/electric/on #Turn on all electric devices from a group
# group shutter
# get v2/site/%i/group/shutter/itemsList groups of type shutter
# post v2/site/%i/group/{groupId}/shutter/close #Close all shutters from a group
# post v2/site/%i/group/{groupId}/shutter/open #Open all shutters from a group
# site library
# get v2/site/%i/library/image/items #Get all images taken from a site's cameras
# get v2/site/%i/library/video/items #Get all videos taken from a site's cameras
# get v2/site/%i/library/video/{videoId}/play #Get video informations for HLS playing


