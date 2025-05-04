# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_Mini\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .LaunchkeyMini import LaunchkeyMini

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[53], model_name='Launchkey Mini'), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[SCRIPT]), outport(props=[NOTES_CC]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return LaunchkeyMini(c_instance)