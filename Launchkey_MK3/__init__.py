# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from .launchkey_mk3 import Launchkey_MK3

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[308, 309, 310, 311, 320], model_name=['Launchkey MK3 25', 'Launchkey MK3 37', 'Launchkey MK3 49', 'Launchkey MK3 61', 'Launchkey MK3 88']), PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[SYNC, REMOTE]), outport(props=[NOTES_CC, SCRIPT])]}

def create_instance(c_instance):
    return Launchkey_MK3(c_instance=c_instance)