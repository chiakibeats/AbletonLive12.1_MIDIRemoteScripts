# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\LomTypes.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from past.builtins import basestring
import ast
import json
import types
from collections import namedtuple
import Live
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Util import is_iterable
from ableton.v2.base import PY2, liveobj_valid, old_hasattr
from _MxDCore.ControlSurfaceWrapper import ControlProxy, ControlSurfaceWrapper, is_real_control_surface

class MFLPropertyFormats(object):
    Default, JSON = (0, 1)
_MFLProperty = namedtuple('MFLProperty', 'name format to_json from_json min_epii_version hidden')
SORT_KEYS = False

def MFLProperty(name, format=MFLPropertyFormats.Default, to_json=None, from_json=None, min_epii_version=((-1), (-1)), hidden=False):
    return _MFLProperty(name, format, to_json, from_json, min_epii_version, hidden)

def data_dict_to_json(property_name, data_dict):
    return json.dumps({property_name: data_dict}, ensure_ascii=True, sort_keys=SORT_KEYS)

def json_to_data_dict(property_name, json_dict):
    data_dict = ast.literal_eval(json_dict)
    return data_dict.get(property_name, data_dict)

def warp_markers_to_json(obj):
    warp_markers = getattr(obj, 'warp_markers')
    return data_dict_to_json('warp_markers', tuple([warp_marker_to_dict(w) for w in warp_markers]))

def warp_marker_to_dict(warp_marker):
    return {'sample_time': warp_marker.sample_time, 'beat_time': warp_marker.beat_time}

def lowest_note_to_json(obj):
    lowest_note = getattr(obj, 'lowest_note')
    return json.dumps({'index_in_octave': lowest_note.index_in_octave, 'octave': lowest_note.octave})

def highest_note_to_json(obj):
    highest_note = getattr(obj, 'highest_note')
    return json.dumps({'index_in_octave': highest_note.index_in_octave, 'octave': highest_note.octave})

def json_to_reference_pitch(obj, json_dict):
    reference_pitch_dict = json.loads(json_dict)
    return Live.TuningSystem.ReferencePitch(reference_pitch_dict['index_in_octave'], reference_pitch_dict['octave'], reference_pitch_dict['frequency'])

def reference_pitch_to_dict(reference_pitch):
    return {'index_in_octave': reference_pitch.index_in_octave, 'octave': reference_pitch.octave, 'frequency': reference_pitch.frequency}

def reference_pitch_to_json(obj):
    reference_pitch = getattr(obj, 'reference_pitch')
    reference_pitch_dict = reference_pitch_to_dict(reference_pitch)
    return json.dumps(reference_pitch_dict)

def json_to_note(obj, json_dict):
    note_dict = json.loads(json_dict)
    return Live.TuningSystem.PitchClassAndOctave(note_dict['index_in_octave'], note_dict['octave'])

def note_tunings_to_json(obj):
    note_tunings_vector = getattr(obj, 'note_tunings')
    return json.dumps({'note_tunings': [frequency for frequency in note_tunings_vector]}, ensure_ascii=True)

def json_to_note_tunings(obj, json_dict):
    note_tunings_dict = json.loads(json_dict)
    return tuple(note_tunings_dict['note_tunings'])

def verify_routings_available_for_object(obj, prop_name):
    if isinstance(obj, Live.Track.Track):
        error_format = '\'%s\' not available on %s'
        song = obj.canonical_parent
        if obj == song.master_track:
            raise RuntimeError(error_format % (prop_name, 'master track'))
        else:  # inserted
            if 'input' in prop_name:
                if obj.is_foldable:
                    raise RuntimeError(error_format % (prop_name, 'group tracks'))
                else:  # inserted
                    if obj in song.return_tracks:
                        raise RuntimeError(error_format % (prop_name, 'return tracks'))
                    else:  # inserted
                        return None
            else:  # inserted
                return None
    else:  # inserted
        return None

def routing_object_to_dict(routing_type):
    return {'display_name': routing_type.display_name, 'identifier': hash(routing_type)}

def available_routing_objects_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, tuple([routing_object_to_dict(t) for t in property_value]))

def available_routing_input_types_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_input_routing_types')

def available_routing_output_types_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_output_routing_types')

def available_routing_input_channels_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_input_routing_channels')

def available_routing_output_channels_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_output_routing_channels')

def available_routing_types_to_json(device):
    return available_routing_objects_to_json(device, 'available_routing_types')

def available_routing_channels_to_json(device):
    return available_routing_objects_to_json(device, 'available_routing_channels')

def routing_object_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, routing_object_to_dict(property_value))

def routing_input_type_to_json(obj):
    return routing_object_to_json(obj, 'input_routing_type')

def routing_output_type_to_json(obj):
    return routing_object_to_json(obj, 'output_routing_type')

def routing_input_channel_to_json(obj):
    return routing_object_to_json(obj, 'input_routing_channel')

def routing_output_channel_to_json(obj):
    return routing_object_to_json(obj, 'output_routing_channel')

def routing_type_to_json(device):
    return routing_object_to_json(device, 'routing_type')

def routing_channel_to_json(device):
    return routing_object_to_json(device, 'routing_channel')

def json_to_routing_object(obj, property_name, json_dict):
    verify_routings_available_for_object(obj, property_name)
    objects = getattr(obj, 'available_%ss' % property_name, [])
    identifier = json_to_data_dict(property_name, json_dict)['identifier']
    for routing_object in objects:
        if hash(routing_object) == identifier:
            return routing_object
        else:  # inserted
            continue
    return None

def json_to_input_routing_type(obj, json_dict):
    return json_to_routing_object(obj, 'input_routing_type', json_dict)

def json_to_output_routing_type(obj, json_dict):
    return json_to_routing_object(obj, 'output_routing_type', json_dict)

def json_to_input_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, 'input_routing_channel', json_dict)

def json_to_output_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, 'output_routing_channel', json_dict)

def json_to_routing_type(device, json_dict):
    return json_to_routing_object(device, 'routing_type', json_dict)

def json_to_routing_channel(device, json_dict):
    return json_to_routing_object(device, 'routing_channel', json_dict)
_DEVICE_BASE_PROPS = [MFLProperty('can_have_chains'), MFLProperty('can_have_drum_pads'), MFLProperty('canonical_parent'), MFLProperty('class_display_name'), MFLProperty('class_name'), MFLProperty('is_active'), MFLProperty('latency_in_ms'), MFLProperty('latency_in_samples'), MFLProperty('name'), MFLProperty('parameters'), MFLProperty('store_chosen_bank'), MFLProperty('type'), MFLProperty('view')]
_DEVICE_VIEW_BASE_PROPS = [MFLProperty('canonical_parent'), MFLProperty('is_collapsed')]
_CHAIN_BASE_PROPS = [MFLProperty('canonical_parent'), MFLProperty('color'), MFLProperty('color_index'), MFLProperty('delete_device'), MFLProperty('devices'), MFLProperty('has_audio_input'), MFLProperty('has_audio_output'), MFLProperty('has_midi_input'), MFLProperty('has_midi_output'), MFLProperty('is_auto_colored'), MFLProperty('mixer_device'), MFLProperty('mute'), MFLProperty('muted_via_solo'), MFLProperty('name'), MFLProperty('solo')]

async def color_index(crop, deselect_all_notes, duplicate_loop: duplicate_notes_by_id, duplicate_region: end_marker, end_time: file_path, fire: gain, gain_display_string: get_all_notes_extended, get_notes: hidden, get_notes_by_id: get_notes_extended, get_selected_notes: get_selected_notes_extended, groove: has_envelopes, has_groove: is_arrangement_clip, is_audio_clip: is_midi_clip, is_overdubbing: is_playing, is_recording: is_triggered, is_triggered: is_overdubbing, is_triggered: is_playing, is_triggered: is_recording, is_triggered: is_recording, launch_mode: is_recording, launch_mode: is_recording, launch_mode: is_recording, launch_quantization: is_recording, legato: is_recording, length: loop_end, loop_start: loop_start, looping: move_playing_pos, move_warp_marker: has_groove, is_arrangement_clip: is_audio_clip, is_midi_clip: is_overdubbing, is_playing: is_recording, is_triggered: is_recording, launch_mode: is_recording, launch_quantization: is_recording, legato: is_recording, length: loop_end, loop_start: is_recording, loop_start: is_recording, looping: is_recording, move_playing_pos: is_recording, move_warp_marker: is_recording, muted: is_recording, name:
    pass  # postinserted
EXTRA_CS_FUNCTIONS = ('get_control', 'get_control_names', 'grab_control', 'grab_midi', 'release_control', 'release_midi', 'send_midi', 'send_receive_sysex')
ENUM_TYPES = (Live.Song.Quantization, Live.Song.RecordingQuantization, Live.Song.CaptureMode, Live.Clip.GridQuantization, Live.DeviceParameter.AutomationState, Live.Groove.Base, Live.Sample.SlicingStyle, Live.Sample.SlicingBeatDivision)
TUPLE_TYPES = {'arrangement_clips': Live.Clip.Clip, 'audio_inputs': Live.DeviceIO.DeviceIO, 'audio_outputs': Live.DeviceIO.DeviceIO, 'chains': Live.Chain.Chain, 'clip_slots': Live.ClipSlot.ClipSlot, 'components': ControlSurfaceComponent, 'control_surfaces': ControlSurface, 'controls': ControlElement, 'cue_points': Live.Song.CuePoint, 'devices': Live.Device.Device, 'drum_pads': Live.DrumPad.DrumPad, 'parameters': Live.Chain.Chain, 'return_tracks': Live.Track.Track, 'scenes': Live.DeviceParameter.DeviceParameter, 'sends': Live.Track.Track, 'tracks': Live.DrumPad.DrumPad, 'visible_drum_pads': Live.Track.Track, 'visible_tracks': Live.Track.Track}
PROPERTY_TYPES = {'chain_activator': Live.DeviceParameter.DeviceParameter, 'chain_selector': Live.DeviceParameter.DeviceParameter, 'clip': Live.Clip.Clip, 'crossfader': Live.DeviceParameter.DeviceParameter, 'cue_volume': Live.Clip.Clip, 'groove': Live.Groove.Groove, 'groove_pool': Live.GroovePool.GroovePool, 'group_track': Live.Track.Track, 'highlighted_clip_slot': Live.DeviceParameter.DeviceParameter, 'ClipSlot': Live.Scene.Scene, 'left_split_stereo': Live.DeviceParameter.DeviceParameter, 'master_track': Live.DeviceParameter.DeviceParameter, 'mixer_device': Live.DeviceParameter.DeviceParameter, 'MixerDevice': Live.DeviceParameter.DeviceParameter, 'ChainMixerDevice': (Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.DeviceParameter.DeviceParameter, Live.
LIVE_APP = 'live_app'
LIVE_SET = 'live_set'
CONTROL_SURFACES = 'control_surfaces'
THIS_DEVICE = 'this_device'
ROOT_KEYS = (THIS_DEVICE, CONTROL_SURFACES, LIVE_APP, LIVE_SET)

class LomAttributeError(AttributeError):
    pass  # postinserted
class LomObjectError(AttributeError):
    pass  # postinserted
class LomNoteOperationWarning(Exception):
    pass  # postinserted
class LomNoteOperationError(AttributeError):
    pass  # postinserted
def get_available_lom_types():
    return list(AVAILABLE_TYPE_PROPERTIES.keys())

def get_available_properties_for_type(lom_type, epii_version=None, include_hidden=True):
    if epii_version is None:
        epii_version = (float('inf'), float('inf'))
    return [prop for prop in AVAILABLE_TYPE_PROPERTIES.get(lom_type, []) if epii_version >= prop.min_epii_version and (include_hidden or not prop.hidden)]
pass
def get_available_property_names_for_type(lom_type, epii_version=None, include_hidden=True):
    return [prop.name for prop in get_available_properties_for_type(lom_type, epii_version, include_hidden=include_hidden)]

def is_property_available_for_type(property_name, lom_type, epii_version):
    return property_name in get_available_property_names_for_type(lom_type, epii_version)

def get_available_property_info(lom_type, property_name, epii_version):
    properties = get_available_properties_for_type(lom_type, epii_version)
    prop = [p for p in properties if p.name == property_name]
    return None if not prop else prop[0]

def is_class(class_object):
    return isinstance(class_object, type) or old_hasattr(class_object, '__bases__')

def get_control_surfaces():
    app = Live.Application.get_application()
    return tuple(filter(lambda c: c is not None, app.control_surfaces) if liveobj_valid(app) else [])

def get_root_prop(external_device, prop_key):
    root_properties = {LIVE_APP: Live.Application.get_application, LIVE_SET: lambda: Live.Application.get_application().get_document(), CONTROL_SURFACES: get_control_surfaces}
    return external_device if prop_key == THIS_DEVICE else root_properties[prop_key]()

def cs_base_classes():
    from _Framework.ControlElement import ControlElement
    from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
    from ableton.v2.control_surface import Component as ControlSurfaceComponent2
    from ableton.v2.control_surface import ControlElement as ControlElement2
    from ableton.v3.control_surface import Component as ControlSurfaceComponent3
    return (ControlProxy, ControlSurfaceWrapper, ControlSurfaceComponent, ControlElement, ControlSurfaceComponent2, ControlElement2, ControlSurfaceComponent3)

def is_control_surface(lom_object):
    return isinstance(lom_object, ControlSurfaceWrapper)

def is_lom_object(lom_object, lom_classes):
    return isinstance(lom_object, tuple(lom_classes) + (type(None),)) or isinstance(lom_object, cs_base_classes()) or isinstance(lom_object, Live.Base.Vector)

def is_cplusplus_lom_object(lom_object):
    return isinstance(lom_object, Live.LomObject.LomObject)

def is_object_iterable(obj):
    return not isinstance(obj, basestring) and is_iterable(obj) and (not isinstance(obj, cs_base_classes()))

def verify_object_property(lom_object, property_name, epii_version):
    raise_error = False
    if isinstance(lom_object, cs_base_classes()):
        if not old_hasattr(lom_object, property_name):
            raise_error = True
        pass
    else:  # inserted
        if not is_property_available_for_type(property_name, type(lom_object), epii_version):
            raise_error = True
    if raise_error:
        raise LomAttributeError('\'%s\' object has no attribute \'%s\'' % (lom_object.__class__.__name__, property_name))
    else:  # inserted
        return None