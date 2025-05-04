# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .AxiomPro import AxiomPro

def create_instance(c_instance):
    return AxiomPro(c_instance)
from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[8227], model_name='Axiom Pro 49'), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[NOTES_CC, SCRIPT]), inport(props=[NOTES_CC]), inport(props=[NOTES_CC]), outport(props=[]), outport(props=[SCRIPT])]}