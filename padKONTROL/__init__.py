# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\padKONTROL\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Generic.GenericScript import GenericScript
from .config import *

def create_instance(c_instance):
    pass
    return GenericScript(c_instance, Live.MidiMap.MapMode.absolute, Live.MidiMap.MapMode.absolute, DEVICE_CONTROLS, TRANSPORT_CONTROLS, VOLUME_CONTROLS, TRACKARM_CONTROLS, BANK_CONTROLS, CONTROLLER_DESCRIPTIONS, MIXER_OPTIONS)
from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2372, product_ids=[261], model_name='padKONTROL'), PORTS_KEY: [inport(props=[PLAIN_OLD_MIDI]), inport(props=[NOTES_CC, SCRIPT]), inport(props=[]), outport(props=[PLAIN_OLD_MIDI]), outport(props=[SCRIPT])]}