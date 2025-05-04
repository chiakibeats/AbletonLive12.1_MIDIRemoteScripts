# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Faderport\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from MackieControl import MackieControl

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479, product_ids=[517], model_name=['PreSonus FP2']), PORTS_KEY: [inport(props=[SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}

def create_instance(c_instance):
    return MackieControl(c_instance)