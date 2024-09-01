from dataclasses import dataclass

#Site {
#siteId (integer): The site unique identifier,
#label (string): The site label,
#brand (string): The brand of the site,
#timezone (string): The timezone of the site location,
#AXA (string): AXA Assistance identifier,
#cameraCount (integer): Number of cameras on the site,
#gateCount (integer): Number of gates on the site,
#shutterCount (integer): Number of shutters on the site,
#socketCount (integer): Number of sockets on the site,
#moduleCount (integer): Number of modules on the site,
#heaterCount (integer): Number of heaters on the site,
#scenarioCount (integer): Number of scenarios on the site,
#deviceTemperatureCount (integer): Number of temperature sensors on the site,
#deviceStateCount (integer): Number of IntelliTag on the site,
#deviceLightCount (integer): Number of light sensors on the site,
#deviceDetectorCount (integer): Number of generic detectors on the site
#}

@dataclass
class MyFoxSite :
    siteId: int
    label: str = ""
    key: str = ""
    brand : str = ""
    timezone : str = ""
    axa : str = ""
    cameraCount: int = 0
    gateCount: int = 0
    shutterCount: int = 0
    socketCount: int = 0
    moduleCount: int = 0
    heaterCount: int = 0
    scenarioCount: int = 0
    deviceTemperatureCount: int = 0
    deviceStateCount: int = 0
    deviceLightCount: int = 0
    deviceDetectorCount: int = 0