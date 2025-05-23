# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\mixable_utilities.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.base import old_hasattr
from ableton.v2.control_surface import find_instrument_meeting_requirement

def is_chain(track_or_chain):
    return isinstance(getattr(track_or_chain, 'proxied_object', track_or_chain), Live.Chain.Chain)

def is_midi_track(track):
    return getattr(track, 'has_midi_input', False) and (not is_chain(track))

def is_audio_track(track):
    return getattr(track, 'has_audio_input', False) and (not is_chain(track))

def can_play_clips(mixable):
    return old_hasattr(mixable, 'fired_slot_index')

def find_drum_rack_instrument(track):
    return find_instrument_meeting_requirement(lambda i: i.can_have_drum_pads, track)

def find_simpler(track_or_chain):
    return find_instrument_meeting_requirement(lambda i: old_hasattr(i, 'playback_mode'), track_or_chain)