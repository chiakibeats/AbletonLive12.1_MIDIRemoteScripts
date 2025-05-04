# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AIRA_MX_1\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:24:29 UTC (1744269869)

from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .RolandMX1 import RolandMX1

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410, product_ids=[419], model_name=['MX-1']), PORTS_KEY: [inport(props=[]), inport(props=[SCRIPT]), outport(props=[]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return RolandMX1(c_instance=c_instance)