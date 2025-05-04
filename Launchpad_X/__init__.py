# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from .launchpad_x import Launchpad_X

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[259], model_name=['Launchpad X']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), inport(props=[NOTES_CC, REMOTE]), outport(props=[NOTES_CC, SYNC, SCRIPT]), outport(props=[REMOTE])]}

def create_instance(c_instance):
    return Launchpad_X(c_instance=c_instance)