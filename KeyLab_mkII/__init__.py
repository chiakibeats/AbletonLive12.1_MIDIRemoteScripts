# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .keylab_mkii import KeyLabMkII

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=7285, product_ids=[587, 651, 715], model_name=['KeyLab mkII 49', 'KeyLab mkII 61', 'KeyLab mkII 88']), PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]), inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return KeyLabMkII(c_instance=c_instance)