# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import _Framework.Capabilities as caps
from .KeyLab import KeyLab

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=7285, product_ids=[517, 581, 645], model_name=['KeyLab 25', 'KeyLab 49', 'KeyLab 61']), caps.PORTS_KEY: [caps.inport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE]), caps.outport(props=[caps.SCRIPT])]}

def create_instance(c_instance):
    return KeyLab(c_instance)