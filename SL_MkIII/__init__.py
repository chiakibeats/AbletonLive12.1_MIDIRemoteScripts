# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .sl_mkiii import SLMkIII

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[257], model_name=['Novation SL MkIII']), PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]), inport(props=[NOTES_CC, SCRIPT, REMOTE]), inport(props=[NOTES_CC, REMOTE]), outport(props=[]), outport(props=[NOTES_CC, SCRIPT]), outport(props=[]), outport(props=[])]}

def create_instance(c_instance):
    return SLMkIII(c_instance=c_instance)