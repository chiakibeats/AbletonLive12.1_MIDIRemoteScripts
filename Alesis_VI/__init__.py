# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Alesis_VI\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .Alesis_VI import Alesis_VI

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=5042, product_ids=[131, 132, 133], model_name=['VI25', 'VI49', 'VI61']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return Alesis_VI(c_instance)