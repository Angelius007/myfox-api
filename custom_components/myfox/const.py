from typing import Final

DOMAIN_MYFOX  : Final = "myfox"
CONFIG_VERSION: int = 2
PREFIX_ENTRY  : Final = "myfox-"

ONLINE_OPTIONS = {
    "Online": 0,
    "Offline": 1,
}

STATE_OPTIONS = {
    "Ouvert": "opened",
    "Fermé": "closed",
}

ALERTE_OPTIONS = {
    "OK": 0,
    "ALERTE": 1,
}

LIGHT_OPTIONS = {
    "Inconnu (0)": 0,
    "Pleine lumière": 1,
    "Lumière du jour": 2,
    "Inconnu (3)": 3,
    "Lumière basse": 4,
    "Pénombre": 5,
    "Obscurité": 6,
}

HEATER_OPTIONS = {
    "ON": "on",
    "OFF": "off",
    "Mode ECO": "eco",
    "Hors GEL": "frost",
    # "Absent": "away",
    # "Auto": "auto",
    # "Boost": "boost",
    # "Thermostat OFF": "thermostatoff",
}
HEATER_EXTENDED_OPTIONS = {
    "ON": "on",
    "OFF": "off",
    "Mode ECO": "eco",
    "Hors GEL": "frost",
    "Absent": "away",
    "Auto": "auto",
    "Boost": "boost",
    "Thermostat OFF": "thermostatoff",
}

SECURITY_OPTIONS = {
    "Disarmed": 1,
    "Partial": 2,
    "Armed": 4
}
