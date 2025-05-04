# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\clip_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
from ableton.v2.base import compose, find_if, liveobj_valid

def has_clip(slot):
    pass
    if liveobj_valid(slot):
        return slot.has_clip
    else:  # inserted
        return None

def clip_of_slot(slot):
    pass
    if liveobj_valid(slot) and liveobj_valid(slot.clip):
            return slot.clip
        else:  # inserted
            return None
    else:  # inserted
        return None

def fire(clip_or_slot, **k):
    pass
    if liveobj_valid(clip_or_slot):
        clip_or_slot.fire(**k)
        return True
    else:  # inserted
        return False

def delete_clip(slot):
    pass
    if liveobj_valid(slot) and has_clip(slot):
        slot.delete_clip()
        return True
    else:  # inserted
        return False

def is_looping(clip):
    pass
    if liveobj_valid(clip):
        return clip.looping
    else:  # inserted
        return None

def get_clip_time(clip):
    pass
    sig_num, sig_denom = (clip.signature_numerator, clip.signature_denominator)
    loop_position = (clip.playing_position - clip.loop_start) * old_div(sig_denom, 4.0)
    beats = int(loop_position) % sig_num + 1
    bars = int(old_div(loop_position, sig_num)) + 1
    return (bars, beats)