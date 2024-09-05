from typing import Final

DOMAIN_MYFOX: Final = "myfox"

DEFAULT_MYFOX_URL_API = "https://api.myfox.me/"

KEY_CLIENT_ID     = "client_id"
KEY_CLIENT_SECRET = "client_secret"
KEY_MYFOX_USER    = "username"
KEY_MYFOX_PSWD    = "password"
KEY_SITE_ID       = "site_id"
KEY_ACCESS_TOKEN  = "access_token"
KEY_REFRESH_TOKEN = "refresh_token"
KEY_EXPIRE_IN     = "expires_in"
KEY_EXPIRE_TIME   = "expires_time"
KEY_GRANT_TYPE    = "grant_type"

GRANT_TYPE_PASSWORD = "password"
GRANT_REFRESH_TOKEN = "refresh_token"

# SEUILS
SEUIL_EXPIRE_MIN = (5*60) # 5 min
CACHE_EXPIRE_IN = (10*60) #10 min

# token
MYFOX_TOKEN_PATH = "oauth2/token"
# sites
MYFOX_INFO_SITE_PATH = "v2/client/site/items" #List available sites for the current user
MYFOX_HISTORY_GET    = "v2/site/%i/history" #Get site history
# scenarios
MYFOX_SCENARIO_ITEMS   = "v2/site/%i/scenario/items"
MYFOX_SCENARIO_PLAY    = "v2/site/%i/scenario/%i/play"
MYFOX_SCENARIO_ENABLE  = "v2/site/%i/scenario/%i/enable"
MYFOX_SCENARIO_DISABLE = "v2/site/%i/scenario/%i/disable"
# security
MYFOX_SECURITY_GET = "v2/site/%i/security"
MYFOX_SECURITY_SET = "v2/site/%i/security/set/%s"
# camera
MYFOX_CAMERA_LIST          = "v2/site/%i/device/camera/items" #List camera devices
MYFOX_CAMERA_LIVE_EXTEND   = "v2/site/%i/device/%i/camera/live/extend" #Add 30 seconds to live streaming
MYFOX_CAMERA_LIVE_START    = "v2/site/%i/device/%i/camera/live/start/%s" #Start live streaming from a camera (hls / rtmp  )
MYFOX_CAMERA_LIVE_STOP     = "v2/site/%i/device/%i/camera/live/stop" #Stop live streaming from a camera
MYFOX_CAMERA_PREV_TAKE     = "v2/site/%i/device/%i/camera/preview/take" #Get a volatile preview from a camera
MYFOX_CAMERA_REC_START     = "v2/site/%i/device/%i/camera/recording/start" #Start recording from a camera
MYFOX_CAMERA_REC_STOP      = "v2/site/%i/device/%i/camera/recording/stop" #Stop recording from a camera
MYFOX_CAMERA_SHUTTER_CLOSE = "v2/site/%i/device/%i/camera/shutter/close" #Open shutter for Myfox Security Camera
MYFOX_CAMERA_SHUTTER_OPEN  = "v2/site/%i/device/%i/camera/shutter/open" #Open shutter for Myfox Security Camera
MYFOX_CAMERA_SNAP_TAKE     = "v2/site/%i/device/%i/camera/snapshot/take" #Take a snapshot from a camera and save it in the library
# device data light
MYFOX_LIGHT_LIST    = "v2/site/%i/device/data/light/items" #List all light sensor featured devices
MYFOX_LIGHT_HISTORY = "v2/site/%i/device/%i/data/light" #Get light measures
# device data other
MYFOX_DEVICE_OTHER_LIST = "v2/site/%i/device/data/other/items" # List all generic sensor featured devices
# device data state
MYFOX_DEVICE_STATE_LIST = "v2/site/%i/device/data/state/items" #List devices with state data
MYFOX_DEVICE_STATE_GET  = "v2/site/%i/device/%i/data/state" #Get device state
# device data temperature
MYFOX_DEVICE_TEMPERATURE_LIST = "v2/site/%i/device/data/temperature/items" #List all temperature sensor featured devices
MYFOX_DEVICE_TEMPERATURE_GET  = "v2/site/%i/device/%i/data/temperature" #Get temperature measures
# device gate 
MYFOX_DEVICE_GATE_LIST        = "v2/site/%i/device/gate/items" #List gate devices
MYFOX_DEVICE_GATE_PERFORM_ONE = "v2/site/%i/device/%i/gate/perform/one" #Perform action #1 post
MYFOX_DEVICE_GATE_PERFORM_TWO = "v2/site/%i/device/%i/gate/perform/two" #Perform action #2 post
# device heater
MYFOX_DEVICE_HEATER_LIST             = "v2/site/%i/device/heater/items" #List heater devices
MYFOX_DEVICE_HEATER_SET_ECO          = "v2/site/%i/device/%i/heater/eco" #Set a heater to 'eco' mode post
MYFOX_DEVICE_HEATER_SET_FROST        = "v2/site/%i/device/%i/heater/frost" #Set a heater to 'frost' mode post
MYFOX_DEVICE_HEATER_SET_ON           = "v2/site/%i/device/%i/heater/on" #Set a heater to 'on' mode post
MYFOX_DEVICE_HEATER_SET_OFF          = "v2/site/%i/device/%i/heater/off" #Set a heater to 'off' mode post
# device heater
MYFOX_DEVICE_HEATER_THERMO_LIST = "v2/site/%i/device/heater/items/withthermostat" #List heater devices with virtuals thermostats
MYFOX_DEVICE_HEATER_THERMO_SET_AUTO  = "v2/site/%i/device/%i/heater/auto" #Set a thermostat to 'auto' mode post
MYFOX_DEVICE_HEATER_THERMO_SET_AWAY  = "v2/site/%i/device/%i/heater/away" #Set a thermostat to 'away' mode post
MYFOX_DEVICE_HEATER_THERMO_SET_BOOST = "v2/site/%i/device/%i/heater/boost" #Set a thermostat to 'boost' mode post
MYFOX_DEVICE_HEATER_THERMO_SET_OFF   = "v2/site/%i/device/%i/heater/thermostatoff" #Set a thermostat to 'off' mode post
# device module
MYFOX_DEVICE_MODULE_LIST        = "v2/site/%i/device/module/items" #List module devices
MYFOX_DEVICE_MODULE_PERFORM_ONE = "v2/site/%i/device/%i/module/perform/one" #Perform action #1 post
MYFOX_DEVICE_MODULE_PERFORM_TWO = "v2/site/%i/device/%i/module/perform/two" #Perform action #2 post
# device shutter
MYFOX_DEVICE_SHUTTER_LIST  = "v2/site/%i/device/shutter/items" #List shutter devices
MYFOX_DEVICE_SHUTTER_MY    = "v2/site/%i/device/%i/shutter/my" #Set shutter to favorite position post
MYFOX_DEVICE_SHUTTER_OPEN  = "v2/site/%i/device/%i/shutter/open" #Open shutter post
MYFOX_DEVICE_SHUTTER_CLOSE = "v2/site/%i/device/%i/shutter/close" #Close shutter post
# device socket
MYFOX_DEVICE_SOCKET_LIST = "v2/site/%i/device/socket/items" #List socket devices
MYFOX_DEVICE_SOCKET_ON   = "v2/site/%i/device/%i/socket/on" #Turn on a device post
MYFOX_DEVICE_SOCKET_OFF  = "v2/site/%i/device/%i/socket/off" #Turn off a device post
# group electic
MYFOX_GROUP_ELECTRIC_LIST    = "v2/site/%i/group/electric/items" #List groups of type electric
MYFOX_GROUP_ELECTRIC_SET_ON  = "v2/site/%i/group/%i/electric/on" #Turn on all electric devices from a group post
MYFOX_GROUP_ELECTRIC_SET_OFF = "v2/site/%i/group/%i/electric/off" #Turn off all electric devices from a group post
# group shutter
MYFOX_GROUP_SHUTTER_LIST      = "v2/site/%i/group/shutter/items" #List groups of type shutter
MYFOX_GROUP_SHUTTER_SET_CLOSE = "v2/site/%i/group/%i/shutter/close" #Close all shutters from a group post
MYFOX_GROUP_SHUTTER_SET_OPEN  = "v2/site/%i/group/%i/shutter/open" #Open all shutters from a group post
# site library
MYFOX_LIBRARY_IMAGE_LIST = "v2/site/%i/library/image/items" #Get all images taken from a site's cameras
MYFOX_LIBRARY_VIDEO_LIST = "v2/site/%i/library/video/items" #Get all videos taken from a site's cameras
MYFOX_LIBRARY_VIDEO_PLAY = "v2/site/%i/library/video/%i/play" #Get video informations for HLS playing
