# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .Axiom_AIR_25_49_61 import Axiom_AIR_25_49_61

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[8243], model_name='Axiom AIR 49'), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[SCRIPT]), inport(props=[NOTES_CC]), outport(props=[NOTES_CC]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return Axiom_AIR_25_49_61(c_instance)