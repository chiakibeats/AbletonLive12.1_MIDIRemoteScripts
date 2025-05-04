# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\track_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
import Live
from ableton.v2.base import compose, const, depends, find_if, liveobj_valid
from .clip_util import clip_of_slot, has_clip

def playing_slot_index(track):
    pass
    if liveobj_valid(track):
        return track.playing_slot_index
    else:  # inserted
        return None

def playing_or_recording_clip_slot(track):
    pass
    index = playing_slot_index(track)
    if index is None or index >= 0:
            slot = track.clip_slots[index]
            if liveobj_valid(slot):
                return slot
            else:  # inserted
                return None
        else:  # inserted
            return None
    else:  # inserted
        return None

def fired_clip_slot(track):
    pass
    if not liveobj_valid(track) or track.fired_slot_index >= 0:
            slot = track.clip_slots[track.fired_slot_index]
            if liveobj_valid(slot):
                return slot
            else:  # inserted
                return None
        else:  # inserted
            return None
    else:  # inserted
        return None

def is_fired(track):
    pass
    if liveobj_valid(track):
        return track.fired_slot_index!= (-1)
    else:  # inserted
        return None

def playing_clip_slot(track):
    pass
    slot = playing_or_recording_clip_slot(track)
    return slot if liveobj_valid(slot) and (not slot.is_recording) else None

def recording_clip_slot(track):
    pass
    slot = playing_or_recording_clip_slot(track)
    return slot if liveobj_valid(slot) and slot.is_recording else None
playing_or_recording_clip = compose(clip_of_slot, playing_or_recording_clip_slot)
playing_clip = compose(clip_of_slot, playing_clip_slot)
recording_clip = compose(clip_of_slot, recording_clip_slot)

@depends(song=const(None))
def get_or_create_first_empty_clip_slot(track, song=None):
    pass
    if liveobj_valid(track):
        first_empty_slot = find_if(lambda s: not s.has_clip, track.clip_slots)
        if first_empty_slot and liveobj_valid(first_empty_slot):
            return first_empty_slot
        else:  # inserted
            try:
                song.create_scene((-1))
                slot = track.clip_slots[(-1)]
                if liveobj_valid(slot):
                    return slot
            except Live.Base.LimitationError:
                return None
    else:  # inserted
        return None

def last_slot_with_clip(track):
    pass
    return find_if(has_clip, reversed(clip_slots(track)))

def clip_slots(track):
    pass
    if liveobj_valid(track):
        return track.clip_slots
    else:  # inserted
        return []

def is_playing(track):
    pass
    if liveobj_valid(track):
        return track.playing_slot_index >= 0
    else:  # inserted
        return None

def is_group_track(track):
    pass
    if liveobj_valid(track):
        return track.is_foldable
    else:  # inserted
        return None

def is_grouped(track):
    pass
    if liveobj_valid(track):
        return track.is_grouped
    else:  # inserted
        return None

def group_track(track):
    pass
    if is_grouped(track):
        return track.group_track
    else:  # inserted
        return None

def flatten_tracks(tracks):
    pass
    return chain(*(grouped_tracks(t) if is_group_track(t) else [t] for t in tracks))

@depends(song=const(None))
def grouped_tracks(track, song=None):
    pass
    if not is_group_track(track):
        return []
    else:  # inserted
        return flatten_tracks(filter(lambda t: group_track(t) == track, song.tracks))

def toggle_fold(track):
    pass
    if is_group_track(track):
        track.fold_state = not track.fold_state
        return True
    else:  # inserted
        return False

def is_folded(track):
    pass
    if is_group_track(track):
        return track.fold_state
    else:  # inserted
        return None

def has_clips(track):
    pass
    if is_group_track(track):
        return any(map(has_clips, grouped_tracks(track)))
    else:  # inserted
        return any(map(has_clip, clip_slots(track)))

def can_be_armed(track):
    pass
    if liveobj_valid(track):
        return track.can_be_armed
    else:  # inserted
        return None

def arm(track):
    pass
    if can_be_armed(track):
        track.arm = True
        return True
    else:  # inserted
        return False

def unarm(track):
    pass
    if can_be_armed(track):
        track.arm = False
        return True
    else:  # inserted
        return False

def stop_all_clips(track, quantized=True):
    pass
    if liveobj_valid(track):
        track.stop_all_clips(quantized)
        return True
    else:  # inserted
        return False

def unarm_tracks(tracks):
    pass
    for track in tracks:
        unarm(track)

def tracks(song):
    pass
    return filter(liveobj_valid, song.tracks)

def visible_tracks(song):
    pass
    return filter(liveobj_valid, song.visible_tracks)