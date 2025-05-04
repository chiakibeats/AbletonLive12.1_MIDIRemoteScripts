# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\live\util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

global _current_song  # inserted
pass
from functools import singledispatch
from typing import Any, Union
import Live
from Live.Clip import Clip
from Live.ClipSlot import ClipSlot
from Live.DeviceParameter import DeviceParameter
from Live.MixerDevice import MixerDevice
from Live.Scene import Scene
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import find_nearest_color
from ableton.v2.control_surface.internal_parameter import InternalParameterBase
from ..base import clamp, find_if, hex_to_rgb
TRANSLATED_MIXER_PARAMETER_NAMES = {'Track Volume': 'Volume', 'Track Panning': 'Pan'}
pass
UNDECLARED_QUANTIZED_PARAMETERS = {'AutoFilter': ('LFO Sync Rate',), 'AutoPan': ('Sync Rate',), 'BeatRepeat': ('Gate', 'Grid', 'Interval', 'Offset', 'Variation'), 'Corpus': ('LFO Sync Rate',), 'Flanger': ('Sync Rate',), 'FrequencyShifter': ('Sync Rate',), 'GlueCompressor': ('Ratio', 'Attack', 'Release'), 'MidiArpeggiator': ('Offset', 'Synced Rate', 'Repeats', 'Ret. Interval', 'Transp. Steps'), 'MidiNoteLength': ('Synced Length',), 'MidiScale': ('Base',), 'MultiSampler': ('L 1 Sync Rate', 'L 2 Sync Rate', 'L 3 Sync Rate'), 'Operator': ('LFO Sync',), 'OriginalSimpler': ('L Sync Rate',), 'Phaser': ('LFO Sync Rate',)}
pass
_current_song = None

class LiveObjectTypeError(Exception):
    pass  # postinserted
def raise_type_error_for_liveobj(obj, return_value: Any=False) -> Any:
    pass
    pass
    return return_value

def application():
    pass
    return Live.Application.get_application()

def song():
    global _current_song  # inserted
    pass
    if liveobj_valid(_current_song):
        return _current_song
    else:  # inserted
        _current_song = application().get_document()
        return _current_song

def set_song(song_obj, from_test=False):
    global _current_song  # inserted
    pass
    _current_song = song_obj

def get_bar_length(clip=None):
    pass
    obj = clip if liveobj_valid(clip) else song()
    return 4.0 * obj.signature_numerator / obj.signature_denominator

def is_arrangement_view_active():
    pass
    return application().view.focused_document_view == 'Arranger'

def is_song_recording():
    pass
    return song().session_record or song().record_mode

def is_track_recording(track):
    pass
    playing_slot = playing_clip_slot(track)
    return liveobj_valid(playing_slot) and playing_slot.is_recording

def is_clip_new_recording(clip):
    pass
    return clip.is_recording and (not clip.is_overdubbing)

def is_clip_playing(clip):
    pass
    return song().is_playing and (clip.is_playing or clip.is_triggered)

def playing_clip_slot(track):
    pass
    if track.clip_slots:
        index = track.playing_slot_index
        if index >= 0:
            return track.clip_slots[index]
    return None

def selected_clip_slot(track):
    pass
    return track.clip_slots[scene_index()] if track.clip_slots else None

def prepare_new_clip_slot(track, stop=False):
    pass
    slot = None
    if track.clip_slots:
        try:
            new_scene_index = _next_empty_clip_slot_index(track)
            song().view.selected_scene = song().scenes[new_scene_index]
            slot = track.clip_slots[scene_index()]
            if stop:
                track.stop_all_clips(False)
        except Live.Base.LimitationError:
            pass
    return slot

def _next_empty_clip_slot_index(track):
    current_index = scene_index()
    scene_count = len(song().scenes)
    while track.clip_slots[current_index].has_clip:
        while True:  # inserted
            current_index += 1
            if current_index == scene_count:
                song().create_scene(scene_count)
            pass
                break
            else:  # inserted
                continue
    return current_index

def is_track_armed(track):
    pass
    return liveobj_valid(track) and track.can_be_armed and (track.arm or track.implicit_arm)

def any_track_armed():
    pass
    return any((t.can_be_armed and t.arm for t in song().tracks))

def find_parent_track(liveobj):
    pass
    parent = liveobj.canonical_parent
    if isinstance(parent, Live.Track.Track):
        return parent
    else:  # inserted
        return find_parent_track(parent)

def all_visible_tracks():
    pass
    return list(tuple(song().visible_tracks) + tuple(song().return_tracks) + (song().master_track,))

def simple_track_name(track):
    pass
    if track == song().master_track:
        return 'Master'
    else:  # inserted
        if track in song().return_tracks:
            return chr(track_index(track, track_list=list(song().return_tracks)) + ord('A'))
        else:  # inserted
            return str(track_index(track) + 1)

def track_index(track=None, track_list=None):
    pass
    track = track or song().view.selected_track
    track_list = track_list or list(song().tracks)
    return track_list.index(track) if track in track_list else (-1)

def scene_index(scene=None):
    pass
    scene = scene or song().view.selected_scene
    return list(song().scenes).index(scene) if scene in song().scenes else (-1)

@singledispatch
pass
def display_name(obj: Union[Scene, Clip, ClipSlot, DeviceParameter], strip_space=True):
    pass
    return raise_type_error_for_liveobj(obj, return_value='')

@display_name.register
def _(scene: Scene, strip_space=True):
    return liveobj_name(scene, strip_space) or 'Scene {}'.format(scene_index(scene) + 1)

@display_name.register
def _(clip: Clip, strip_space=True):
    return liveobj_name(clip, strip_space) or 'Clip'

@display_name.register
def _(clip_slot: ClipSlot, strip_space=True):
    return display_name(clip_slot.clip, strip_space) if liveobj_valid(clip_slot.clip) else 'Slot {}'.format(list(clip_slot.canonical_parent.clip_slots).index(clip_slot) + 1)

@display_name.register
def _(parameter: DeviceParameter, **_):
    if liveobj_valid(parameter):
        try:
            return parameter.display_name
        except AttributeError:
            return TRANSLATED_MIXER_PARAMETER_NAMES.get(parameter.name, parameter.name)
    else:  # inserted
        return ''

@display_name.register
def _(parameter: InternalParameterBase, **_):
    return parameter.name

def liveobj_name(obj, strip_space=True):
    pass
    if liveobj_valid(obj):
        return obj.name.strip() if strip_space else obj.name
    else:  # inserted
        return ''

def is_device_rack(device):
    pass
    return liveobj_valid(device) and device.can_have_chains

def is_instrument_rack(device):
    pass
    return is_device_rack(device) and device.type == Live.Device.DeviceType.instrument

def selected_chain(device):
    pass
    return device.view.selected_chain if is_device_rack(device) and device.view.is_showing_chain_devices and (not device.view.is_collapsed) else None
    else:  # inserted
        return None

def flatten_device_chain(track_or_chain):
    pass
    devices = []
    chain_devices = track_or_chain.devices if liveobj_valid(track_or_chain) else []
    for device in chain_devices:
        devices.append(device)
        devices.extend(flatten_device_chain(selected_chain(device)))
    return devices

def get_parameter_by_name(name, device):
    pass
    if liveobj_valid(device):
        return find_if(lambda p: p.original_name == name and liveobj_valid(p) and (p.is_enabled or False), device.parameters)

def normalized_parameter_value(parameter, value=None):
    pass
    result = 0.0
    if liveobj_valid(parameter):
        value = value if value is not None else parameter.value
        param_range = parameter.max - parameter.min
        result = (value - parameter.min) / param_range
    return clamp(result, 0.0, 1.0)

def parameter_value_to_midi_value(parameter, max_value=128):
    pass
    return int(normalized_parameter_value(parameter) * (max_value - 1))

def parameter_owner(parameter):
    pass
    return parameter.canonical_parent.canonical_parent if isinstance(parameter.canonical_parent, MixerDevice) else parameter.canonical_parent

def is_parameter_quantized(parameter, device):
    pass
    is_quantized = False
    if liveobj_valid(parameter):
        device_class = getattr(device, 'class_name', None)
        is_quantized = parameter.is_quantized or (device_class in UNDECLARED_QUANTIZED_PARAMETERS and parameter.name in UNDECLARED_QUANTIZED_PARAMETERS[device_class])
    return is_quantized

def liveobj_color_to_midi_rgb_values(obj, default_values=(0, 0, 0)):
    pass
    if liveobj_valid(obj):
        return tuple((i // 2 for i in hex_to_rgb(obj.color)))
    else:  # inserted
        return default_values
pass
def liveobj_color_to_value_from_palette(obj, palette=None, fallback_table=None, default_value=0):
    pass
    if liveobj_valid(obj):
        try:
            return palette[obj.color]
        except (KeyError, IndexError):
            return find_nearest_color(fallback_table, obj.color)
    else:  # inserted
        return default_value

def deduplicate_parameters(parameters):
    pass
    param_names = set()
    without_duplicates = []
    for param in parameters:
        name = getattr(param, 'original_name', None)
        without_duplicates.append(None if name and name in param_names else param)
        param_names.add(name)
        continue
    return without_duplicates

def major_version():
    pass
    return Live.Application.get_application().get_major_version()