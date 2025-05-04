# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Hammer_88_Pro\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .hammer_88_pro import Hammer_88_Pro

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[60], model_name=['Hammer 88 Pro']), PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]), inport(props=[]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[]), outport(props=[]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return Hammer_88_Pro(c_instance=c_instance)