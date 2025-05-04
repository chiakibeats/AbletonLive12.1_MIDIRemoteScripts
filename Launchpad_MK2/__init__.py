# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from .Launchpad_MK2 import Launchpad_MK2

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120], model_name=['Launchpad MK2', 'Launchpad MK2 2', 'Launchpad MK2 3', 'Launchpad MK2 4', 'Launchpad MK2 5', 'Launchpad MK2 6', 'Launchpad MK2 7', 'Launchpad MK2 8', 'Launchpad MK2 9', 'Launchpad MK2 10', 'Launchpad MK2 11', 'Launchpad MK2 12', 'Launchpad MK2 13', 'Launchpad MK2 14', 'Launchpad MK2 15', 'Launchpad MK2 16']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[NOTES_CC, SCRIPT, SYNC, REMOTE])]}

def create_instance(c_instance):
    return Launchpad_MK2(c_instance)