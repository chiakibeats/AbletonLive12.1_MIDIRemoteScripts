# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control_surface.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.builtins import unicode
import logging
import traceback
from collections import OrderedDict
from contextlib import contextmanager
from functools import partial
from itertools import chain
from pickle import dumps, loads
import Live
from ..base import BooleanContext, EventObject, const, find_if, first, in_range, inject, lazy_attribute, liveobj_valid, old_hasattr, task
from . import defaults, midi
from .control_element import OptimizedOwnershipHandler
from .device_bank_registry import DeviceBankRegistry
from .device_provider import DeviceProvider
from .elements import PhysicalDisplayElement
from .input_control_element import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, MIDI_SYSEX_TYPE, InputControlElement, ScriptForwarding
from .message_scheduler import MessageScheduler
from .profile import profile
__all__ = ('SimpleControlSurface', 'ControlSurface')
logger = logging.getLogger(__name__)
CS_LIST_KEY = 'control_surfaces'

def publish_control_surface(control_surface):
    get_control_surfaces().append(control_surface)

def get_control_surfaces():
    if isinstance(__builtins__, dict):
        if CS_LIST_KEY not in __builtins__.keys():
            __builtins__[CS_LIST_KEY] = []
        return __builtins__[CS_LIST_KEY]
    else:
        if not old_hasattr(__builtins__, CS_LIST_KEY):
            setattr(__builtins__, CS_LIST_KEY, [])
        return getattr(__builtins__, CS_LIST_KEY)

class SimpleControlSurface(EventObject):
    pass
    __events__ = ('received_midi', 'disconnect')
    preferences_key = None
    pass
    handle_undo_steps = False
    pass

    def __init__(self, c_instance=None, *a, **k):
        super(SimpleControlSurface, self).__init__(*a, **k)
        self.canonical_parent = None
        publish_control_surface(self)
        self._c_instance = c_instance
        self._pad_translations = None
        self._components = []
        self._displays = []
        self._controls = []
        self._forwarding_long_identifier_registry = {}
        self._forwarding_registry = {}
        self._is_sending_scheduled_messages = BooleanContext()
        self._remaining_scheduled_messages = []
        self._task_group = task.TaskGroup(auto_kill=False)
        self._in_build_midi_map = BooleanContext()
        self._suppress_requests_counter = 0
        self._rebuild_requests_during_suppression = 0
        self._enabled = True
        self._in_component_guard = BooleanContext()
        self._accumulate_midi_messages = BooleanContext()
        self._midi_message_dict = {}
        self._midi_message_list = []
        self._midi_message_count = 0
        self.mxd_midi_scheduler = MessageScheduler(self._do_send_midi, self._task_group.add(task.TimedCallbackTask()))
        self._ownership_handler = OptimizedOwnershipHandler()
        self._control_surface_injector = inject(element_ownership_handler=const(self._ownership_handler), parent_task_group=const(self._task_group), show_message=const(self.show_message), register_component=const(self._register_component), register_control=const(self._register_control), request_rebuild_midi_map=const(self.request_rebuild_midi_map), set_pad_translations=const(self.set_pad_translations), send_midi=const(self._send_midi), song=const(self.song), set_session_highlight=const(self._c_instance.set_session_highlight)).everywhere()

    @property
    def components(self):
        pass
        return tuple(filter(lambda comp: not comp.is_private, self._components))

    @property
    def root_components(self):
        pass
        return tuple(filter(lambda comp: comp.is_root and (not comp.is_private), self._components))

    @property
    def controls(self):
        pass
        return self._controls

    def _get_tasks(self):
        return self._task_group
    _tasks = property(_get_tasks)

    @property
    def application(self):
        pass
        return Live.Application.get_application()

    @property
    def song(self):
        pass
        return self._c_instance.song()

    def disconnect(self):
        pass

    def can_lock_to_devices(self):
        pass
        return False

    def suggest_map_mode(self, cc_no, channel):
        pass
        suggested_map_mode = -1
        for control in self._controls:
            if isinstance(control, InputControlElement) and control.message_type() == MIDI_CC_TYPE and (control.message_identifier() == cc_no) and (control.message_channel() == channel):
                suggested_map_mode = control.message_map_mode()
                break
            else:
                pass
                continue
        return suggested_map_mode

    def supports_pad_translation(self):
        pass
        return self._pad_translations is not None

    def show_message(self, message):
        pass
        self._c_instance.show_message(message)

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

    def update_display_hook(self):
        pass
        return

    @profile
    def receive_midi(self, midi_bytes):
        pass

    @profile
    def receive_midi_chunk(self, midi_chunk):
        pass

    @staticmethod
    def _receive_midi_data(recipient, data):
        recipient.receive_value(data)

    def _do_receive_midi(self, midi_bytes):
        self.notify_received_midi(*midi_bytes)
        self.mxd_midi_scheduler.handle_message(midi_bytes)
        self.process_midi_bytes(midi_bytes, self._receive_midi_data)

    @staticmethod
    def _merge_midi_data(recipient, data, midi_data):
        if recipient.allow_receiving_chunks:
            _, values = midi_data.setdefault(recipient, (recipient, []))
            values.append(data)
            return
        else:
            midi_data[object()] = (recipient, data)

    def _do_receive_midi_chunk(self, midi_chunk):
        pass
        midi_data_for_recipient = OrderedDict()
        for midi_bytes in midi_chunk:
            self.notify_received_midi(*midi_bytes)
            self.mxd_midi_scheduler.handle_message(midi_bytes)
            self.process_midi_bytes(midi_bytes, partial(self._merge_midi_data, midi_data=midi_data_for_recipient))
        for recipient, data in midi_data_for_recipient.values():
            if recipient.allow_receiving_chunks:
                recipient.receive_chunk(tuple(data))
                continue
            else:
                recipient.receive_value(data)
                continue

    def process_midi_bytes(self, midi_bytes, midi_processor):
        pass
        if midi.is_sysex(midi_bytes):
            result = self.get_registry_entry_for_sysex_midi_message(midi_bytes)
            if result is not None:
                identifier, recipient = result
                midi_processor(recipient, midi_bytes[len(identifier):-1])
                return
            elif self.received_midi_listener_count() == 0:
                logger.warning('Got unknown sysex message: ' + midi.pretty_print_bytes(midi_bytes))
                return
            else:
                return None
        else:
            recipient = self.get_recipient_for_nonsysex_midi_message(midi_bytes)
            if recipient is not None:
                midi_processor(recipient, midi.extract_value(midi_bytes))
                return
            elif self.received_midi_listener_count() == 0:
                logger.warning('Got unknown message: ' + midi.pretty_print_bytes(midi_bytes))
                return
            else:
                return None

    def get_recipient_for_nonsysex_midi_message(self, midi_bytes):
        forwarding_key = midi_bytes[:1 if midi.is_pitchbend(midi_bytes) else 2]
        if forwarding_key in self._forwarding_registry:
            return self._forwarding_registry[forwarding_key]
        else:
            return None

    def get_registry_entry_for_sysex_midi_message(self, midi_bytes):
        return find_if(lambda identifier_recipient: midi_bytes[:len(identifier_recipient[0])] == identifier_recipient[0], self._forwarding_long_identifier_registry.items())

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
            self._task_group.add(task.sequence(task.delay(delay_in_ticks), message))
            return
        else:
            self._task_group.add(message)

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
        self._controls.append(control)
        control.canonical_parent = self
        if isinstance(control, PhysicalDisplayElement):
            self._displays.append(control)
        if old_hasattr(control, '_is_resource_based'):
            control._is_resource_based = True
            return

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
        return find_if(lambda c: c.name == control_name, self._controls)

    def get_component_by_name(self, component_name):
        return find_if(lambda c: c.name == component_name, self.components)

    def _send_midi(self, midi_event_bytes, optimized=True):
        pass
        if self._accumulate_midi_messages:
            sysex_status_byte = 240
            entry = (self._midi_message_count, midi_event_bytes)
            if optimized and midi_event_bytes[0] != sysex_status_byte:
                key = (midi_event_bytes[0], midi_event_bytes[1])
                self._midi_message_dict[key] = entry
            else:
                self._midi_message_list.append(entry)
            self._midi_message_count += 1
        else:
            self._do_send_midi(midi_event_bytes)
        return True

    def _flush_midi_messages(self):
        sorted_messages = sorted(chain(self._midi_message_list, self._midi_message_dict.values()), key=first)
        for _, message in sorted_messages:
            self._do_send_midi(message)
        self._midi_message_dict.clear()
        self._midi_message_list[:] = []
        self._midi_message_count = 0

    def _do_send_midi(self, midi_event_bytes):
        try:
            self._c_instance.send_midi(midi_event_bytes)
        except Exception:
            logger.error('Error while sending midi message %s', str(midi_event_bytes))
            traceback.print_exc()
            return False
        return True

    def _install_mapping(self, midi_map_handle, control, parameter, feedback_delay, feedback_map):
        success = False
        feedback_rule = None
        if control.message_type() == MIDI_NOTE_TYPE:
            feedback_rule = Live.MidiMap.NoteFeedbackRule()
            feedback_rule.note_no = control.message_identifier()
            feedback_rule.vel_map = feedback_map
        elif control.message_type() == MIDI_CC_TYPE:
            feedback_rule = Live.MidiMap.CCFeedbackRule()
            feedback_rule.cc_no = control.message_identifier()
            feedback_rule.cc_value_map = feedback_map
        elif control.message_type() == MIDI_PB_TYPE:
            feedback_rule = Live.MidiMap.PitchBendFeedbackRule()
            feedback_rule.value_pair_map = feedback_map
        feedback_rule.channel = control.message_channel()
        feedback_rule.delay_in_ms = feedback_delay
        feedback_rule.enabled = control.is_feedback_enabled
        if control.message_type() == MIDI_NOTE_TYPE:
            success = Live.MidiMap.map_midi_note_with_feedback_map(midi_map_handle, parameter, control.message_channel(), control.message_identifier(), feedback_rule)
        elif control.message_type() == MIDI_CC_TYPE:
            success = Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, parameter, control.message_channel(), control.message_identifier(), control.message_map_mode(), feedback_rule, not control.needs_takeover(), control.mapping_sensitivity)
        elif control.message_type() == MIDI_PB_TYPE:
            success = Live.MidiMap.map_midi_pitchbend_with_feedback_map(midi_map_handle, parameter, control.message_channel(), feedback_rule, not control.needs_takeover())
        if success:
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, parameter)
        return success

    def _install_forwarding(self, midi_map_handle, control, forwarding_type=ScriptForwarding.exclusive):
        success = False
        should_consume_event = forwarding_type == ScriptForwarding.exclusive
        if control.message_type() == MIDI_NOTE_TYPE:
            success = Live.MidiMap.forward_midi_note(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier(), should_consume_event)
        elif control.message_type() == MIDI_CC_TYPE:
            success = Live.MidiMap.forward_midi_cc(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier(), should_consume_event)
        elif control.message_type() == MIDI_PB_TYPE:
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

    @lazy_attribute
    def preferences(self):
        pass
        if self.preferences_key is None:
            raise RuntimeError('Trying to access preferences without providing a preference_key')
        else:
            preferences = self._c_instance.preferences(self.preferences_key)
            pref_dict = {}
            try:
                pref_dict = loads(bytes(preferences))
            except Exception as e:
                logger.error('Error while loading control surface preferences %s', str(e))
            preferences.set_serializer(lambda: dumps(pref_dict))
            return pref_dict

    def _pre_serialize(self):
        pass
        if self.preferences_key is not None:
            preferences = self._c_instance.preferences(self.preferences_key)
            dump = dumps(self.preferences)
            preferences.set_serializer(lambda: dump)

class ControlSurface(SimpleControlSurface):
    pass
    device_provider_class = DeviceProvider
    pass

    def __init__(self, *a, **k):
        super(ControlSurface, self).__init__(*a, **k)
        self._device_provider = None
        self._device_bank_registry = None
        if self.device_provider_class:
            self._init_device_provider()
        self._device_support_injector = inject(device_provider=const(self.device_provider), device_bank_registry=const(self._device_bank_registry)).everywhere()

    def _init_device_provider(self):
        self._device_provider = self.register_disconnectable(self.device_provider_class(song=self.song))
        self._device_bank_registry = self.register_disconnectable(DeviceBankRegistry())
        self._c_instance.update_locks()
        self._device_provider.update_device_selection()

    @property
    def device_provider(self):
        return self._device_provider

    def disconnect(self):
        self._device_provider = None
        self._device_bank_registry = None
        super(ControlSurface, self).disconnect()

    def can_lock_to_devices(self):
        return True

    def lock_to_device(self, device):
        pass

    def unlock_from_device(self, device):
        pass

    def restore_bank(self, bank_index):
        pass

    def toggle_lock(self):
        pass
        self._c_instance.toggle_lock()

    @contextmanager
    def _component_guard(self):
        if False:
            yield
        pass