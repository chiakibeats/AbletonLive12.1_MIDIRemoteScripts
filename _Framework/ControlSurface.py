# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ControlSurface.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import logging
import traceback
from contextlib import contextmanager
from functools import partial, wraps
from itertools import chain
import Live
from ableton.v2.base import old_hasattr
from . import Defaults, Task
from .ControlElement import OptimizedOwnershipHandler
from .Dependency import inject
from .InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_STATUS, MIDI_PB_TYPE, MIDI_SYSEX_TYPE, InputControlElement
from .MessageScheduler import MessageScheduler
from .PhysicalDisplayElement import PhysicalDisplayElement
from .Profile import profile
from .SubjectSlot import SlotManager, Subject
from .Util import BooleanContext, const, find_if, first, in_range
logger = logging.getLogger(__name__)

def _scheduled_method(method):
    pass

    @wraps(method)
    def wrapper(self, *a, **k):

        def doit():
            return method(self, *a, **k)
        self.schedule_message(1, doit)
    return wrapper
CS_LIST_KEY = 'control_surfaces'

def publish_control_surface(control_surface):
    get_control_surfaces().append(control_surface)

def get_control_surfaces():
    if isinstance(__builtins__, dict):
        if CS_LIST_KEY not in list(__builtins__.keys()):
            __builtins__[CS_LIST_KEY] = []
        return __builtins__[CS_LIST_KEY]
    else:
        if not old_hasattr(__builtins__, CS_LIST_KEY):
            setattr(__builtins__, CS_LIST_KEY, [])
        return getattr(__builtins__, CS_LIST_KEY)

class ControlSurface(Subject, SlotManager):
    pass
    received_midi = ()
    __subject_events__ = ('received_midi', 'disconnect')

    def __init__(self, c_instance=None, *a, **k):
        pass
        super(ControlSurface, self).__init__(*a, **k)
        self.canonical_parent = None
        publish_control_surface(self)
        self._c_instance = c_instance
        self.log_message('Initializing...')
        self._pad_translations = None
        self._suggested_input_port = str('')
        self._suggested_output_port = str('')
        self._components = []
        self._displays = []
        self.controls = []
        self._highlighting_session_component = None
        self._device_component = None
        self._forwarding_long_identifier_registry = {}
        self._forwarding_registry = {}
        self._is_sending_scheduled_messages = BooleanContext()
        self._remaining_scheduled_messages = []
        self._task_group = Task.TaskGroup(auto_kill=False)
        self._in_build_midi_map = BooleanContext()
        self._suppress_requests_counter = 0
        self._rebuild_requests_during_suppression = 0
        self._enabled = True
        self._in_component_guard = BooleanContext()
        self._accumulate_midi_messages = BooleanContext()
        self._midi_message_dict = {}
        self._midi_message_list = []
        self._midi_message_count = 0
        self.mxd_midi_scheduler = MessageScheduler(self._do_send_midi, self._task_group.add(Task.TimedCallbackTask()))
        self._control_surface_injector = inject(parent_task_group=const(self._task_group), show_message=const(self.show_message), log_message=const(self.log_message), register_component=const(self._register_component), register_control=const(self._register_control), request_rebuild_midi_map=const(self.request_rebuild_midi_map), set_pad_translations=const(self.set_pad_translations), send_midi=const(self._send_midi), song=self.song).everywhere()
        self.register_slot(self.song(), self._on_track_list_changed, 'visible_tracks')
        self.register_slot(self.song(), self._on_scene_list_changed, 'scenes')
        self.register_slot(self.song().view, self._on_selected_track_changed, 'selected_track')
        self.register_slot(self.song().view, self._on_selected_scene_changed, 'selected_scene')

    @property
    def components(self):
        return tuple([comp for comp in self._components if not comp.is_private])

    @property
    def root_components(self):
        return tuple([comp for comp in self._components if comp.is_root and (not comp.is_private)])

    def _get_tasks(self):
        return self._task_group
    _tasks = property(_get_tasks)

    def application(self):
        pass
        return Live.Application.get_application()

    def song(self):
        pass
        return self._c_instance.song()

    def disconnect(self):
        pass

    def _control_surfaces(self):
        pass
        return get_control_surfaces()

    def can_lock_to_devices(self):
        pass
        return self._device_component != None

    @_scheduled_method
    def lock_to_device(self, device):
        pass

    @_scheduled_method
    def unlock_from_device(self, device):
        pass

    @_scheduled_method
    def restore_bank(self, bank_index):
        pass

    def suggest_input_port(self):
        pass
        return self._suggested_input_port

    def suggest_output_port(self):
        pass
        return self._suggested_output_port

    def suggest_map_mode(self, cc_no, channel):
        pass
        suggested_map_mode = -1
        for control in self.controls:
            if isinstance(control, InputControlElement):
                if control.message_type() == MIDI_CC_TYPE and control.message_identifier() == cc_no and (control.message_channel() == channel):
                    suggested_map_mode = control.message_map_mode()
                    break
            pass
            continue
        return suggested_map_mode

    def suggest_needs_takeover(self, cc_no, channel):
        pass
        needs_takeover = True
        for control in self._controls:
            if isinstance(control, InputControlElement):
                if control.message_type() == MIDI_CC_TYPE and control.message_identifier() == cc_no and (control.message_channel() == channel):
                    needs_takeover = control.needs_takeover()
                    break
            pass
            continue
        return needs_takeover

    def supports_pad_translation(self):
        return self._pad_translations != None

    def set_highlighting_session_component(self, session_component):
        if self._highlighting_session_component is not None:
            self._set_session_highlight(-1, -1, -1, -1, False)
            self._highlighting_session_component.set_highlighting_callback(None)
        if session_component is not None:
            session_component.set_highlighting_callback(self._set_session_highlight)
        self._highlighting_session_component = session_component

    def highlighting_session_component(self):
        pass
        return self._highlighting_session_component

    def show_message(self, message):
        pass
        self._c_instance.show_message(message)

    def log_message(self, *message):
        message = '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, message)))
        console_message = 'LOG: ' + message
        logger.info(console_message)
        if self._c_instance:
            self._c_instance.log_message(message)

    def instance_identifier(self):
        return self._c_instance.instance_identifier()

    def connect_script_instances(self, instanciated_scripts):
        pass
        return

    def request_rebuild_midi_map(self):
        pass
        if self._suppress_requests_counter > 0:
            self._rebuild_requests_during_suppression += 1
            return
        else:
            self._c_instance.request_rebuild_midi_map()

    def build_midi_map(self, midi_map_handle):
        pass

    def toggle_lock(self):
        pass
        self._c_instance.toggle_lock()

    def port_settings_changed(self):
        pass
        self.refresh_state()

    def refresh_state(self):
        pass
        self.update()

    def update(self):
        pass

    @profile
    def update_display(self):
        pass

    @profile
    def receive_midi(self, midi_bytes):
        pass

    def is_sysex_message(self, midi_bytes):
        return len(midi_bytes) != 3

    def _do_receive_midi(self, midi_bytes):
        self.notify_received_midi(*midi_bytes)
        self.mxd_midi_scheduler.handle_message(midi_bytes)
        if not self.is_sysex_message(midi_bytes):
            self.handle_nonsysex(midi_bytes)
            return
        else:
            self.handle_sysex(midi_bytes)

    def get_recipient_for_nonsysex_midi_message(self, midi_bytes):
        is_pitchbend = midi_bytes[0] & 240 == MIDI_PB_STATUS
        forwarding_key = midi_bytes[:1 if is_pitchbend else 2]
        if forwarding_key in self._forwarding_registry:
            return self._forwarding_registry[forwarding_key]
        else:
            return None

    def handle_nonsysex(self, midi_bytes):
        is_pitchbend = midi_bytes[0] & 240 == MIDI_PB_STATUS
        value = midi_bytes[1] + (midi_bytes[2] << 7) if is_pitchbend else midi_bytes[2]
        recipient = self.get_recipient_for_nonsysex_midi_message(midi_bytes)
        if recipient is not None:
            recipient.receive_value(value)
            return
        elif self.received_midi_listener_count() == 0:
            self.log_message('Got unknown message: ' + str(midi_bytes))
            return
        else:
            return None

    def handle_sysex(self, midi_bytes):
        result = find_if(lambda id__: midi_bytes[:len(id__[0])] == id__[0], iter(self._forwarding_long_identifier_registry.items()))
        if result != None:
            id, control = result
            control.receive_value(midi_bytes[len(id):-1])
            return
        elif self.received_midi_listener_count() == 0:
            self.log_message('Got unknown sysex message: ' + str(midi_bytes))
            return
        else:
            return None

    def set_device_component(self, device_component):
        if self._device_component is not None:
            self._device_component.set_lock_callback(None)
        self._device_component = device_component
        self._c_instance.update_locks()
        if device_component is not None:
            device_component.set_lock_callback(self._toggle_lock)
            if device_component.device_selection_follows_track_selection:
                device_component.update_device_selection()
                return
        else:
            return

    @contextmanager
    def suppressing_rebuild_requests(self):
        if False:
            yield
        pass

    def _set_suppress_rebuild_requests(self, suppress_requests):
        if suppress_requests:
            self._suppress_requests_counter += 1
            return
        else:
            self._suppress_requests_counter -= 1
            if self._suppress_requests_counter == 0 and self._rebuild_requests_during_suppression > 0:
                self.request_rebuild_midi_map()
                self._rebuild_requests_during_suppression = 0
                return
            else:
                return

    def set_pad_translations(self, pad_translations):

        def check_translation(translation):
            return True
        self._pad_translations = pad_translations

    def set_enabled(self, enable):
        pass

    def schedule_message(self, delay_in_ticks, callback, parameter=None):
        pass
        if not self._is_sending_scheduled_messages:
            delay_in_ticks -= 1
        message_reference = [None]

        def message(delta):
            if parameter:
                callback(parameter)
            else:
                callback()
            self._remaining_scheduled_messages.remove(message_reference)
        message_reference[0] = message
        self._remaining_scheduled_messages.append(message_reference)
        if delay_in_ticks:
            self._task_group.add(Task.sequence(Task.delay(delay_in_ticks), message))
            return
        else:
            self._task_group.add(message)

    def _process_remaining_scheduled_messages(self):
        current_scheduled_messages = tuple(self._remaining_scheduled_messages)
        for message, in current_scheduled_messages:
            message(None)

    def set_feedback_channels(self, channels):
        self._c_instance.set_feedback_channels(channels)

    def set_controlled_track(self, track):
        pass
        self._c_instance.set_controlled_track(track)

    def release_controlled_track(self):
        pass
        self._c_instance.release_controlled_track()

    def _register_control(self, control):
        pass
        self.controls.append(control)
        control.canonical_parent = self
        if isinstance(control, PhysicalDisplayElement):
            self._displays.append(control)

    def _register_component(self, component):
        pass
        self._components.append(component)
        component.canonical_parent = self

    def _disconnect_and_unregister_all_components(self):
        pass

    @contextmanager
    def component_guard(self):
        if False:
            yield
        pass

    @property
    def in_component_guard(self):
        return bool(self._in_component_guard)

    @contextmanager
    def _component_guard(self):
        if False:
            yield
        pass

    @profile
    def call_listeners(self, listeners):
        pass

    @contextmanager
    def accumulating_midi_messages(self):
        if False:
            yield
        pass

    def get_control_by_name(self, control_name):
        return find_if(lambda c: c.name == control_name, self.controls)

    def _send_midi(self, midi_event_bytes, optimized=True):
        pass
        if self._accumulate_midi_messages:
            sysex_status_byte = 240
            entry = (self._midi_message_count, midi_event_bytes)
            if optimized and midi_event_bytes[0] != sysex_status_byte:
                self._midi_message_dict[midi_event_bytes[0], midi_event_bytes[1]] = entry
            else:
                self._midi_message_list.append(entry)
            self._midi_message_count += 1
        else:
            self._do_send_midi(midi_event_bytes)
        return True

    def _flush_midi_messages(self):
        for _, message in sorted(chain(self._midi_message_list, iter(self._midi_message_dict.values())), key=first):
            self._do_send_midi(message)
        self._midi_message_dict.clear()
        self._midi_message_list[:] = []
        self._midi_message_count = 0

    def _do_send_midi(self, midi_event_bytes):
        try:
            self._c_instance.send_midi(midi_event_bytes)
        except:
            self.log_message('Error while sending midi message', midi_event_bytes)
            traceback.print_exc()
            return False
        return True

    def _install_mapping(self, midi_map_handle, control, parameter, feedback_delay, feedback_map):
        success = False
        feedback_rule = None
        if control.message_type() is MIDI_NOTE_TYPE:
            feedback_rule = Live.MidiMap.NoteFeedbackRule()
            feedback_rule.note_no = control.message_identifier()
            feedback_rule.vel_map = feedback_map
        elif control.message_type() is MIDI_CC_TYPE:
            feedback_rule = Live.MidiMap.CCFeedbackRule()
            feedback_rule.cc_no = control.message_identifier()
            feedback_rule.cc_value_map = feedback_map
        elif control.message_type() is MIDI_PB_TYPE:
            feedback_rule = Live.MidiMap.PitchBendFeedbackRule()
            feedback_rule.value_pair_map = feedback_map
        feedback_rule.channel = control.message_channel()
        feedback_rule.delay_in_ms = feedback_delay
        if control.message_type() is MIDI_NOTE_TYPE:
            success = Live.MidiMap.map_midi_note_with_feedback_map(midi_map_handle, parameter, control.message_channel(), control.message_identifier(), feedback_rule)
        elif control.message_type() is MIDI_CC_TYPE:
            success = Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, parameter, control.message_channel(), control.message_identifier(), control.message_map_mode(), feedback_rule, not control.needs_takeover(), control.mapping_sensitivity)
        elif control.message_type() is MIDI_PB_TYPE:
            success = Live.MidiMap.map_midi_pitchbend_with_feedback_map(midi_map_handle, parameter, control.message_channel(), feedback_rule, not control.needs_takeover())
        if success:
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, parameter)
        return success

    def _install_forwarding(self, midi_map_handle, control):
        success = False
        if control.message_type() is MIDI_NOTE_TYPE:
            success = Live.MidiMap.forward_midi_note(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier())
        elif control.message_type() is MIDI_CC_TYPE:
            success = Live.MidiMap.forward_midi_cc(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier())
        elif control.message_type() is MIDI_PB_TYPE:
            success = Live.MidiMap.forward_midi_pitchbend(self._c_instance.handle(), midi_map_handle, control.message_channel())
        else:
            success = True
        if success:
            forwarding_keys = control.identifier_bytes()
            for key in forwarding_keys:
                registry = self._forwarding_registry if control.message_type() != MIDI_SYSEX_TYPE else self._forwarding_long_identifier_registry
                registry[key] = control
                continue
        return success

    def _translate_message(self, type, from_identifier, from_channel, to_identifier, to_channel):
        if type == MIDI_CC_TYPE:
            self._c_instance.set_cc_translation(from_identifier, from_channel, to_identifier, to_channel)
            return
        elif type == MIDI_NOTE_TYPE:
            self._c_instance.set_note_translation(from_identifier, from_channel, to_identifier, to_channel)
            return
        else:
            return None

    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        if list((track_offset, scene_offset, width, height)).count(-1) != 4:
            pass
        self._c_instance.set_session_highlight(track_offset, scene_offset, width, height, include_return_tracks)

    def _on_track_list_changed(self):
        for component in self._components:
            component.on_track_list_changed()
        self.schedule_message(1, self._on_selected_track_changed)

    def _on_scene_list_changed(self):
        for component in self._components:
            component.on_scene_list_changed()

    def _on_selected_track_changed(self):
        for component in self._components:
            component.on_selected_track_changed()

    def _on_selected_scene_changed(self):
        for component in self._components:
            component.on_selected_scene_changed()

    def _toggle_lock(self):
        self._c_instance.toggle_lock()

    def _refresh_displays(self):
        pass
        for display in self._displays:
            display.update()
            display._tasks.update(Defaults.TIMER_DELAY)

class OptimizedControlSurface(ControlSurface):
    pass

    def __init__(self, *a, **k):
        super(OptimizedControlSurface, self).__init__(*a, **k)
        self._optimized_ownership_handler = OptimizedOwnershipHandler()
        injecting = inject(element_ownership_handler=const(self._optimized_ownership_handler))
        self._ownership_handler_injector = injecting.everywhere()

    @contextmanager
    def _component_guard(self):
        if False:
            yield
        pass

    def _register_control(self, control):
        super(OptimizedControlSurface, self)._register_control(control)
        if old_hasattr(control, '_is_resource_based'):
            control._is_resource_based = True