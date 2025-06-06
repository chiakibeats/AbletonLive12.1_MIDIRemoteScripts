# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .oxygen_pro import Oxygen_Pro

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[56, 57, 58], model_name=['Oxygen Pro 25', 'Oxygen Pro 49', 'Oxygen Pro 61']), PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]), inport(props=[]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[]), outport(props=[]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return Oxygen_Pro(c_instance=c_instance)