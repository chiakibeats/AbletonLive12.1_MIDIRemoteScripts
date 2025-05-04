# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\device_chain_utils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from itertools import chain
import Live
from ableton.v2.base import find_if, liveobj_valid

def is_empty_drum_pad(drum_pad):
    return isinstance(drum_pad, Live.DrumPad.DrumPad) and (not drum_pad.chains or not drum_pad.chains[0].devices)

def is_first_device_on_pad(device, drum_pad):
    return find_if(lambda pad: pad.chains and pad.chains[0].devices and (pad.chains[0].devices[0] == device), drum_pad.canonical_parent.drum_pads)

def is_simpler(device):
    return device and device.class_name == 'OriginalSimpler'