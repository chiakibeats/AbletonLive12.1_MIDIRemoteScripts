# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_25_Classic\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .Axiom import Axiom

def create_instance(c_instance):
    return Axiom(c_instance)
from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[408], model_name='USB Axiom 25'), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), inport(props=[PLAIN_OLD_MIDI]), outport(props=[SCRIPT])]}