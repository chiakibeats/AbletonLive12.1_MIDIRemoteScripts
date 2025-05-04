# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_5th_Gen\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .oxygen_5th_gen import Oxygen_5th_Gen

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[1, 2, 3], model_name=['Oxygen 25 MKV', 'Oxygen 49 MKV', 'Oxygen 61 MKV']), PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return Oxygen_5th_Gen(c_instance=c_instance)