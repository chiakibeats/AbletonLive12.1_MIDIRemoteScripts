# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.base import liveobj_valid

def is_drum_pad(item):
    return liveobj_valid(item) and isinstance(item, Live.DrumPad.DrumPad)

def find_chain_or_track(item):
    pass
    if is_drum_pad(item) and item.chains:
        chain = item.chains[0]
    else:  # inserted
        chain = item
        while liveobj_valid(chain) and (not isinstance(chain, (Live.Track.Track, Live.Chain.Chain))):
            chain = getattr(chain, 'canonical_parent', None)
                    break
                else:  # inserted
                    continue
    return chain

def find_rack(item):
    pass
    rack = item
    while liveobj_valid(rack) and (not isinstance(rack, Live.RackDevice.RackDevice)):
        rack = getattr(rack, 'canonical_parent', None)
                break
            else:  # inserted
                continue
    return rack