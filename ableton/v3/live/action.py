# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\live\action.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

pass
import logging
import math
from functools import singledispatch, wraps
from sys import maxsize
from typing import Optional, Union
from Live.Base import LimitationError
from Live.Clip import Clip
from Live.ClipSlot import ClipSlot
from Live.DeviceParameter import DeviceParameter
from Live.Scene import Scene
from Live.Song import Quantization
from Live.Track import Track
from ..base import round_to_multiple
from . import liveobj_changed, liveobj_valid, scene_index, song, track_index
from .util import get_bar_length, is_clip_new_recording, raise_type_error_for_liveobj
logger = logging.getLogger(__name__)

def action(func):
    pass
    singledispatch_func = singledispatch(func)

    @wraps(func)
    def wrapper(target, *a, **k):
        if liveobj_valid(target):
            try:
                return singledispatch_func(target, *a, **k)
            except (AttributeError, AssertionError, ValueError, RuntimeError, TypeError, LimitationError) as e:
                logger.debug('An exception occurred when attempting to perform an action: %s', e)
        return False
    wrapper.register = singledispatch_func.register
    return wrapper

@action
def toggle_arm(track: Track, exclusive=None) -> bool:
    pass
    if track.can_be_armed:
        exclusive = exclusive if exclusive is not None else song().exclusive_arm
        new_value = not track.arm
        for t in song().tracks:
            if t.can_be_armed:
                if t == track or (track.is_part_of_selection and t.is_part_of_selection):
                    t.arm = new_value
                    continue
                else:  # inserted
                    if exclusive and t.arm:
                        t.arm = False
            continue
        return True
    else:  # inserted
        return False

@action
def delete(deletable: Union[Clip, ClipSlot, Scene, Track]) -> bool:
    pass
    return raise_type_error_for_liveobj(deletable)

@delete.register
def _(deletable: Clip):
    if deletable.is_arrangement_clip:
        deletable.canonical_parent.delete_clip(deletable)
    else:  # inserted
        deletable.canonical_parent.delete_clip()
    return True

@delete.register
def _(deletable: ClipSlot):
    deletable.delete_clip()
    return True

@delete.register
def _(deletable: Scene):
    song().delete_scene(scene_index(deletable))
    return True

@delete.register
def _(deletable: Track):
    if deletable == song().master_track:
        return False
    else:  # inserted
        if deletable in song().return_tracks:
            song().delete_return_track(track_index(deletable, track_list=list(song().return_tracks)))
        else:  # inserted
            song().delete_track(track_index(deletable))
        return True

@action
def delete_notes_with_pitch(clip: Clip, pitch: int) -> bool:
    pass
    args = dict(from_time=0, from_pitch=pitch, time_span=maxsize, pitch_span=1)
    if clip.get_notes_extended(**args):
        clip.remove_notes_extended(**args)
        return True
    else:  # inserted
        return False

@action
def delete_notes_in_range(clip: Clip, from_time: float, time_span: float) -> bool:
    pass
    args = dict(from_time=from_time, from_pitch=0, time_span=time_span, pitch_span=128)
    if clip.get_notes_extended(**args):
        clip.remove_notes_extended(**args)
        return True
    else:  # inserted
        return False

@action
def duplicate_loop(clip: Clip) -> bool:
    pass
    clip.duplicate_loop()
    clip.view.show_loop()
    return True

@action
def duplicate(duplicatable: Union[Clip, ClipSlot, Scene, Track]) -> bool:
    pass
    return raise_type_error_for_liveobj(duplicatable)

@duplicate.register
def _(duplicatable: Clip):
    if duplicatable.is_arrangement_clip:
        track = duplicatable.canonical_parent
        track.duplicate_clip_to_arrangement(duplicatable, duplicatable.end_time)
        return True
    else:  # inserted
        return duplicate(duplicatable.canonical_parent)

@duplicate.register
def _(duplicatable: ClipSlot):
    track = duplicatable.canonical_parent
    track.duplicate_clip_slot(list(track.clip_slots).index(duplicatable))
    return True

@duplicate.register
def _(duplicatable: Scene):
    song().duplicate_scene(scene_index(duplicatable))
    return True

@duplicate.register
def _(duplicatable: Track):
    song().duplicate_track(track_index(duplicatable))
    return True

@action
def duplicate_clip_special(clip: Clip) -> bool:
    pass
    if clip.is_arrangement_clip:
        track = clip.canonical_parent
        song().view.detail_clip = track.duplicate_clip_to_arrangement(clip, clip.end_time)
    else:  # inserted
        slot = clip.canonical_parent
        track = slot.canonical_parent
        slot_index = list(track.clip_slots).index(slot)
        next_slot_index = track.duplicate_clip_slot(slot_index)
        song().view.selected_scene = song().scenes[next_slot_index]
        if clip.is_playing:
            track.clip_slots[next_slot_index].fire(force_legato=True, launch_quantization=Quantization.q_no_q)
    return True

@action
def select(selectable: Union[Clip, ClipSlot, Scene, Track]) -> bool:
    pass
    return raise_type_error_for_liveobj(selectable)

@select.register
def _(selectable: Clip):
    return select(selectable.canonical_parent)

@select.register
def _(selectable: ClipSlot):
    if not liveobj_changed(song().view.highlighted_clip_slot, selectable):
        return False
    else:  # inserted
        song().view.highlighted_clip_slot = selectable
        return True

@select.register
def _(selectable: Scene):
    if not liveobj_changed(song().view.selected_scene, selectable):
        return False
    else:  # inserted
        song().view.selected_scene = selectable
        return True

@select.register
def _(selectable: Track):
    if not liveobj_changed(song().view.selected_track, selectable):
        return False
    else:  # inserted
        song().view.selected_track = selectable
        return True

@action
def fire(fireable: Union[Clip, ClipSlot, Scene], button_state=None) -> bool:
    pass
    if isinstance(fireable, ClipSlot) and fireable.has_clip:
        fireable = fireable.clip
    if button_state is None:
        fireable.fire()
    else:  # inserted
        fireable.set_fire_button_state(button_state)
        if button_state and song().select_on_launch:
            select(fireable)
    return True

@action
def toggle_or_cycle_parameter_value(parameter: DeviceParameter) -> bool:
    pass
    if parameter.is_quantized:
        if parameter.value + 1 > parameter.max:
            parameter.value = parameter.min
        else:  # inserted
            parameter.value = parameter.value + 1
    else:  # inserted
        parameter.value = parameter.max if parameter.value == parameter.min else parameter.min
    return True

@action
def extend_loop_for_region(clip: Clip, region_start: float, region_length: float):
    pass
    bar_length = get_bar_length(clip=clip)
    if region_start < clip.loop_start:
        set_loop_start(clip, round_to_multiple(region_start, bar_length))
        return True
    else:  # inserted
        region_end = region_start + region_length
        if region_end > clip.loop_end:
            num_bars_needed = math.ceil(region_end / bar_length)
            set_loop_end(clip, num_bars_needed * bar_length)
            return True
        else:  # inserted
            return False

@action
pass
def set_loop_start(clip: Clip, loop_start: float, show_loop: Optional[bool]=True) -> bool:
    pass
    if is_clip_new_recording(clip):
        return False
    else:  # inserted
        clip.loop_start = loop_start
        clip.start_marker = loop_start
        if show_loop:
            clip.view.show_loop()
        return True

@action
def set_loop_end(clip: Clip, loop_end: float, show_loop: Optional[bool]=True) -> bool:
    pass
    if is_clip_new_recording(clip):
        return False
    else:  # inserted
        clip.loop_end = loop_end
        clip.end_marker = loop_end
        if show_loop:
            clip.view.show_loop()
        return True

@action
def set_loop_position(clip: Clip, loop_start: float, loop_end: float) -> bool:
    pass
    if is_clip_new_recording(clip):
        return False
    else:  # inserted
        if loop_start < clip.loop_end and loop_start < clip.end_marker:
            set_loop_start(clip, loop_start, show_loop=False)
            set_loop_end(clip, loop_end, show_loop=False)
        else:  # inserted
            set_loop_end(clip, loop_end, show_loop=False)
            set_loop_start(clip, loop_start, show_loop=False)
        clip.view.show_loop()
        return True