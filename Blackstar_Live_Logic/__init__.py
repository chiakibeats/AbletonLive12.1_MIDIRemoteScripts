# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .blackstar_live_logic import Blackstar_Live_Logic

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=10196, product_ids=[4097], model_name=['Live Logic MIDI Controller']), PORTS_KEY: [inport(props=[SCRIPT, REMOTE, NOTES_CC]), outport(props=[SCRIPT, REMOTE, NOTES_CC])]}

def create_instance(c_instance):
    return Blackstar_Live_Logic(c_instance=c_instance)