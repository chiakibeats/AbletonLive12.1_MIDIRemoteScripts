# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import _Framework.Capabilities as caps
from .VCM600 import VCM600

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=6817, product_ids=[64], model_name=['VCM-600']), caps.PORTS_KEY: [caps.inport(props=[caps.SCRIPT]), caps.outport(props=[caps.SCRIPT])]}

def create_instance(c_instance):
    pass
    return VCM600(c_instance)