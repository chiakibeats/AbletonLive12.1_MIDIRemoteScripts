# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_Mini32\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .AxiomAirMini32 import AxiomAirMini32

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[8247], model_name='Axiom A.I.R. Mini32'), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT])]}

def create_instance(c_instance):
    return AxiomAirMini32(c_instance)