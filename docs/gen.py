from typing import List
import json
import sys
from unittest.mock import Mock

from custom_components.myfox.scenes import BaseScene, MyFoxSceneInfo
from custom_components.myfox.devices import BaseDevice, MyFoxDeviceInfo
from custom_components.myfox.devices.registry import (
    device_by_client_key
)
from custom_components.myfox.scenes.registry import (
    scene_by_typeLabel_key
)

from custom_components.myfox.entities.entity import (
    MyFoxAbstractDeviceEntity
)

MARKER_VALUE = -66666

device_info = MyFoxDeviceInfo(
    deviceId = 1,
    label = "LABEL",
    modelId = 1,
    modelLabel = "MODEL_LABEL"
)

scene_info = MyFoxSceneInfo(
    scenarioId = 1,
    label = "LABEL",
    typeLabel = "TYPE_LABEL",
    enabled = "ENABLED"
)

def get_device_data(deviceType: str) -> List[MyFoxDeviceInfo]:
    return [MyFoxDeviceInfo(1, "LABEL", 1, "MODEL_LABEL")]

def get_scene_data(typeLabel: str) -> List[MyFoxDeviceInfo]:
    return [MyFoxSceneInfo(1, "LABEL", typeLabel, "ENABLED")]

def get_devices(deviceType: str, dev: type[BaseDevice]) -> List[BaseDevice]:
    real_devices = []
    for device_info in get_device_data(deviceType):
        device = dev(device_info)
        real_devices.append(device)
    return real_devices

def get_scenes(typeLabel: str, dev: type[BaseScene]) -> List[BaseScene]:
    real_devices = []
    for device_info in get_scene_data(typeLabel):
        device = dev(device_info)
        real_devices.append(device)
    return real_devices

def add_stats_(info_global:str, new_info:str) -> str: 
    """ update info avec , si besoin """
    if len(info_global) > 0:
        info_global+=", "
    info_global+=new_info
    return info_global 

def device_summary(base_devices: List[BaseDevice]) -> str:
    total_sensors = 0
    total_switches = 0
    total_selects = 0
    total_buttons = 0
    total_texts = 0
    total_cameras = 0
    total_medias = 0
    total_alarms = 0
    total_info = ""
    for device in base_devices:
        coordinator = Mock()
        coordinator.data = []
        total_sensors += len(device.sensors(coordinator))
        if total_sensors > 0:
            total_info=add_stats_(total_info, f"sensors: {total_sensors}")
        total_switches += len(device.switches(coordinator))
        if total_switches > 0:
             total_info=add_stats_(total_info, f"switches: {total_switches}")
        total_selects += len(device.selects(coordinator))
        if total_selects > 0:
             total_info=add_stats_(total_info, f"selects: {total_selects}")
        total_buttons += len(device.buttons(coordinator))
        if total_buttons > 0:
             total_info=add_stats_(total_info, f"buttons: {total_buttons}")
        total_texts += len(device.texts(coordinator))
        if total_texts > 0:
             total_info=add_stats_(total_info, f"texts: {total_texts}")
        total_cameras += len(device.cameras(coordinator))
        if total_cameras > 0:
             total_info=add_stats_(total_info, f"cameras: {total_cameras}")
        total_medias += len(device.medias(coordinator))
        if total_medias > 0:
             total_info=add_stats_(total_info, f"medias: {total_medias}")
        total_alarms += len(device.alarms(coordinator))
        if total_alarms > 0:
             total_info=add_stats_(total_info, f"alarms: {total_alarms}")
    return total_info

def scene_summary(base_scenes: List[BaseScene]) -> str:
    total_scenes = 0
    total_switches = 0
    for scene in base_scenes:
        coordinator = Mock()
        coordinator.data = []
        total_scenes += len(scene.scenes(coordinator))
        total_switches += len(scene.switches(coordinator))
    return f"scenes: {total_scenes}, switches: {total_switches}"

def render_generic(sw: MyFoxAbstractDeviceEntity) -> str:
    return "- %s (%s)" % (sw._attr_unique_id, sw.__class__.__name__)

def render_device_summary(device: BaseDevice, brief: bool = False) -> str:
    coordinator = Mock()
    coordinator.data = []
    res = ""
    if device.sensors(coordinator).__len__() > 0 :
        res += "\n*Sensors*\n"
        for sw in device.sensors(coordinator):
            res += render_generic(sw) + "\n"

    if device.switches(coordinator).__len__() > 0 :
        res += "\n*Switches*\n"
        for sw in device.switches(coordinator):
            res += render_generic(sw) + "\n"

    if device.selects(coordinator).__len__() > 0 :
        res += "\n*Selects*\n"
        for sw in device.selects(coordinator):
            res += render_generic(sw) + "\n"

    if device.buttons(coordinator).__len__() > 0 :
        res += "\n*Buttons*\n"
        for sw in device.buttons(coordinator):
            res += render_generic(sw) + "\n"

    if device.texts(coordinator).__len__() > 0 :
        res += "\n*Texts*\n"
        for sw in device.texts(coordinator):
            res += render_generic(sw) + "\n"

    if device.cameras(coordinator).__len__() > 0 :
        res += "\n*Cameras*\n"
        for sw in device.cameras(coordinator):
            res += render_generic(sw) + "\n"

    if device.medias(coordinator).__len__() > 0 :
        res += "\n*Medias*\n"
        for sw in device.medias(coordinator):
            res += render_generic(sw) + "\n"

    if device.alarms(coordinator).__len__() > 0 :
        res += "\n*Alarms*\n"
        for sw in device.alarms(coordinator):
            res += render_generic(sw) + "\n"

    return res

def render_scene_summary(scene: BaseScene, brief: bool = False) -> str:
    coordinator = Mock()
    coordinator.data = []
    res = ""
    if scene.scenes(coordinator).__len__() > 0 :
        res += "\n*Scenes*\n"
        for sw in scene.scenes(coordinator):
            res += render_generic(sw) + "\n"

    if scene.switches(coordinator).__len__() > 0 :
        res += "\n*Switches*\n"
        for sw in scene.switches(coordinator):
            res += render_generic(sw) + "\n"

    return res

def render_brief_summary():
    content_summary = "Liste des integrations :\n\n"
    for dt, dev in device_by_client_key.items():
        if dt != "generic":
            content = ""
            real_devices = get_devices(dt, dev)
            for device in real_devices:
                if len(real_devices) > 1:
                    content = content + f"\n### {device.device_info.modelLabel}\n"
                content = content + render_device_summary(device, True)
            content_summary+="<details><summary> %s <i>(%s)</i> </summary>\n" % (dev.__name__, device_summary(real_devices))
            content_summary+="<p>\n"
            content_summary+="%s\n" % content
            content_summary+="</p></details>\n"
            content_summary+="\n"

    for dt, dev in scene_by_typeLabel_key.items():
        if dt != "generic":
            content = ""
            real_scenes = get_scenes(dt, dev)
            for scene in real_scenes:
                if len(real_scenes) > 1:
                    content = content + f"\n### {scene.scene_info.typeLabel}\n"
                content = content + render_scene_summary(scene, True)
            content_summary+="<details><summary> %s <i>(%s)</i> </summary>" % (dev.__name__, scene_summary(real_scenes))
            content_summary+="<p>\n"
            content_summary+="%s\n" % content
            content_summary+="</p></details>\n"
            content_summary+="\n"
    print(content_summary)
    with open("summary.md" , "w+") as f_summary:
        f_summary.write(content_summary)
        f_summary.write("\n")

def update_full_summary():
    content_integration = "Liste des integrations\n\n"
    content_integration+="Liste des devices : \n"
    for dt, dev in device_by_client_key.items():
        if dt != "generic":
            content = ""
            real_devices = get_devices(dt, dev)
            for device in real_devices:
                if len(real_devices) > 1:
                    content+= f"\n### {device.device_info.modelLabel}\n"
                content+= render_device_summary(device)
            with open("devices/%s.md" % dev.__name__, "w+") as f:
                f.write("## %s\n" % dev.__name__)
                f.write(content)
                f.write("\n\n")
                f.write("[Retour liste des integrations](../integration.md)\n")

            content_integration+="- [%s](devices/%s.md)\n" % (dev.__name__, dev.__name__)
    content_integration+="\n"
    content_integration+="Liste des scenes : \n"
    for dt, dev in scene_by_typeLabel_key.items():
        if dt != "generic":
            content = ""
            real_scenes = get_scenes(dt, dev)
            for scene in real_scenes:
                if len(real_scenes) > 1:
                    content = content + f"\n### {scene.scene_info.typeLabel}\n"
                content = content + render_scene_summary(scene)
            with open("scenes/%s.md" % dev.__name__, "w+") as f:
                f.write("## %s\n" % dev.__name__)
                f.write(content)
                f.write("\n\n")
                f.write("[Retour liste des integrations](../integration.md)\n")

            #print("- [%s](scenes/%s.md)" % (dt, dt))
            content_integration+="- [%s](scenes/%s.md)\n" % (dev.__name__, dev.__name__)
    print(content_integration)
    with open("integration.md" , "w+") as f_integration:
        f_integration.write(content_integration)
        f_integration.write("\n")

if __name__ == "__main__":
    print("path : %s" % sys.path)
    update_full_summary()
    render_brief_summary()