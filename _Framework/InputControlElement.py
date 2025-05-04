# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\InputControlElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import contextlib
import logging
from . import Task
from .Dependency import depends
from .Disconnectable import Disconnectable
from .NotifyingControlElement import NotifyingControlElement
from .Signal import Signal
from .SubjectSlot import SubjectEvent
from .Util import const, in_range, nop
logger = logging.getLogger(__name__)
MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_SYSEX_TYPE = 3
MIDI_INVALID_TYPE = 4
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE, MIDI_CC_TYPE, MIDI_PB_TYPE, MIDI_SYSEX_TYPE, MIDI_INVALID_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224

class ParameterSlot(Disconnectable):
    pass
    _parameter = None
    _control = None

    def __init__(self, parameter=None, control=None, *a, **k):
        super(ParameterSlot, self).__init__(*a, **k)
        self.parameter = parameter
        self.control = control

    def _get_control(self):
        return self._control

    def _set_control(self, control):
        if control!= self._control:
            self.soft_disconnect()
            self._control = control
            self.connect()
    control = property(_get_control, _set_control)

    def _get_parameter(self):
        return self._parameter

    def _set_parameter(self, parameter):
        if parameter!= self._parameter:
            self.soft_disconnect()
            self._parameter = parameter
            self.connect()
    parameter = property(_get_parameter, _set_parameter)

    def connect(self):
        if self._control!= None and self._parameter!= None:
                self._control.connect_to(self._parameter)

    def soft_disconnect(self):
        if self._control!= None and self._parameter!= None:
                self._control.release_parameter()
        else:  # inserted
            return

    def disconnect(self):
        self.parameter = None
        self.control = None
        super(ParameterSlot, self).disconnect()

class InputSignal(Signal):
    pass

    def __init__(self, sender=None, *a, **k):
        super(InputSignal, self).__init__(*a, sender=sender, **k)
        self._input_control = sender

    @contextlib.contextmanager
    def _listeners_update(self):
        if False: yield  # inserted
        pass  # cflow: irreducible

    def connect(self, *a, **k):
        pass  # cflow: irreducible

    def disconnect(self, *a, **k):
        pass  # cflow: irreducible

    def disconnect_all(self, *a, **k):
        pass  # cflow: irreducible

class InputControlElement(NotifyingControlElement):
    pass

    class ProxiedInterface(NotifyingControlElement.ProxiedInterface):
        send_value = nop
        receive_value = nop
        use_default_message = nop
        set_channel = nop
        message_channel = const(None)
        mapped_parameter = nop
        mapping_sensitivity = const(None)
        reset_state = nop
    __subject_events__ = (SubjectEvent(name='value', signal=InputSignal, override=True),)
    _input_signal_listener_count = 0
    num_delayed_messages = 1
    send_depends_on_forwarding = True

    @depends(request_rebuild_midi_map=const(nop))
    pass
    pass
    pass
    pass
    pass
    def __init__(self, msg_type=None, channel=None, identifier=None, sysex_identifier=None, request_rebuild_midi_map=None, *a, **k):
        super(InputControlElement, self).__init__(*a, **k)
        self._request_rebuild = request_rebuild_midi_map
        self._msg_type = msg_type
        self._msg_channel = channel
        self._msg_identifier = identifier
        self._msg_sysex_identifier = sysex_identifier
        self._original_channel = channel
        self._original_identifier = identifier
        self._needs_takeover = True
        self._is_mapped = True
        self._is_being_forwarded = True
        self._delayed_messages = []
        self._force_next_send = False
        self._mapping_feedback_delay = 0
        self._mapping_sensitivity = 1.0
        self._suppress_script_forwarding = False
        self._send_delayed_messages_task = self._tasks.add(Task.run(self._send_delayed_messages))
        self._send_delayed_messages_task.kill()
        self._parameter_to_map_to = None
        self._in_parameter_gesture = False
        self._last_sent_message = None
        self._report_input = False
        self._report_output = False

    def message_type(self):
        return self._msg_type

    def message_channel(self):
        return self._msg_channel

    def original_channel(self):
        return self._original_channel

    def message_identifier(self):
        return self._msg_identifier

    def original_identifier(self):
        return self._original_identifier

    def message_sysex_identifier(self):
        return self._msg_sysex_identifier

    def message_map_mode(self):
        raise NotImplementedError

    def _get_mapping_sensitivity(self):
        return self._mapping_sensitivity

    def _set_mapping_sensitivity(self, sensitivity):
        self._mapping_sensitivity = sensitivity
        self._request_rebuild()
    mapping_sensitivity = property(_get_mapping_sensitivity, _set_mapping_sensitivity)

    def _get_suppress_script_forwarding(self):
        return self._suppress_script_forwarding

    def _set_suppress_script_forwarding(self, value):
        if self._suppress_script_forwarding!= value:
            self._suppress_script_forwarding = value
            self._request_rebuild()
    suppress_script_forwarding = property(_get_suppress_script_forwarding, _set_suppress_script_forwarding)

    def force_next_send(self):
        pass
        self._force_next_send = True

    def set_channel(self, channel):
        if self._msg_channel!= channel:
            self._msg_channel = channel
            self._request_rebuild()

    def set_identifier(self, identifier):
        if self._msg_identifier!= identifier:
            self._msg_identifier = identifier
            self._request_rebuild()

    def set_needs_takeover(self, needs_takeover):
        self._needs_takeover = needs_takeover

    def set_feedback_delay(self, delay):
        self._mapping_feedback_delay = delay

    def needs_takeover(self):
        return self._needs_takeover

    def use_default_message(self):
        if (self._msg_channel, self._msg_identifier)!= (self._original_channel, self._original_identifier):
            self._msg_channel = self._original_channel
            self._msg_identifier = self._original_identifier
            self._request_rebuild()

    def _mapping_feedback_values(self):
        value_map = tuple()
        if self._mapping_feedback_delay!= 0:
            if self._msg_type!= MIDI_PB_TYPE:
                value_map = tuple(range(128))
            else:  # inserted
                value_pairs = []
                for value in range(16384):
                    value_pairs.append((value >> 7 & 127, value & 127))
                value_map = tuple(value_pairs)
        return value_map

    def install_connections(self, install_translation, install_mapping, install_forwarding):
        self._send_delayed_messages_task.kill()
        self._is_mapped = False
        self._is_being_forwarded = False
        if self._msg_channel!= self._original_channel or self._msg_identifier!= self._original_identifier:
            install_translation(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)
        if self._parameter_to_map_to!= None:
            self._is_mapped = install_mapping(self, self._parameter_to_map_to, self._mapping_feedback_delay, self._mapping_feedback_values())
        if self.script_wants_forwarding():
            self._is_being_forwarded = install_forwarding(self)
            if self._is_being_forwarded and self.send_depends_on_forwarding:
                    self._send_delayed_messages_task.restart()
                    return
        else:  # inserted
            return

    def script_wants_forwarding(self):
        pass
        return not self._suppress_script_forwarding and self._input_signal_listener_count > 0 or self._report_input

    def begin_gesture(self):
        pass
        if not self._parameter_to_map_to or not self._in_parameter_gesture:
                self._in_parameter_gesture = True
                self._parameter_to_map_to.begin_gesture()
                return
        else:  # inserted
            return

    def end_gesture(self):
        pass
        if self._parameter_to_map_to and self._in_parameter_gesture:
                self._in_parameter_gesture = False
                self._parameter_to_map_to.end_gesture()
                return
        else:  # inserted
            return

    def connect_to(self, parameter):
        pass
        if self._parameter_to_map_to!= parameter:
            if parameter == None:
                self.release_parameter()
                return
            else:  # inserted
                self._parameter_to_map_to = parameter
                self._request_rebuild()

    def release_parameter(self):
        if self._parameter_to_map_to!= None:
            self.end_gesture()
            self._parameter_to_map_to = None
            self._request_rebuild()

    def mapped_parameter(self):
        return self._parameter_to_map_to

    def _status_byte(self, channel):
        status_byte = channel
        if self._msg_type == MIDI_NOTE_TYPE:
            status_byte += MIDI_NOTE_ON_STATUS
        else:  # inserted
            if self._msg_type == MIDI_CC_TYPE:
                status_byte += MIDI_CC_STATUS
            else:  # inserted
                if self._msg_type == MIDI_PB_TYPE:
                    status_byte += MIDI_PB_STATUS
                else:  # inserted
                    raise NotImplementedError
        return status_byte

    def identifier_bytes(self):
        pass
        if self._msg_type == MIDI_PB_TYPE:
            return ((self._status_byte(self._msg_channel),),)
        else:  # inserted
            if self._msg_type == MIDI_SYSEX_TYPE:
                return (self.message_sysex_identifier(),)
            else:  # inserted
                if self._msg_type == MIDI_NOTE_TYPE:
                    return ((self._status_byte(self._msg_channel), self.message_identifier()), (self._status_byte(self._msg_channel) - 16, self.message_identifier()))
                else:  # inserted
                    return ((self._status_byte(self._msg_channel), self.message_identifier()),)

    def _send_delayed_messages(self):
        self.clear_send_cache()
        for value, channel in self._delayed_messages:
            self._do_send_value(value, channel=channel)
        self._delayed_messages[:] = []

    def send_value(self, value, force=False, channel=None):
        value = int(value)
        self._verify_value(value)
        if force or self._force_next_send:
            self._do_send_value(value, channel)
        else:  # inserted
            if self.send_depends_on_forwarding:
                pass  # postinserted
            if self._is_being_forwarded:
                pass  # postinserted
            if self._send_delayed_messages_task.is_running:
                first = 1 - self.num_delayed_messages
                self._delayed_messages = self._delayed_messages[first:] + [(value, channel)]
            else:  # inserted
                if (value, channel)!= self._last_sent_message:
                    self._do_send_value(value, channel)
        self._force_next_send = False
        return

    def _do_send_value(self, value, channel=None):
        data_byte1 = self._original_identifier
        data_byte2 = value
        status_byte = self._status_byte(self._original_channel if channel is None else channel)
        if self._msg_type == MIDI_PB_TYPE:
            data_byte1 = value & 127
            data_byte2 = value >> 7 & 127
        if self.send_midi((status_byte, data_byte1, data_byte2)):
            self._last_sent_message = (value, channel)
            if self._report_output:
                is_input = True
                self._report_value(value, not is_input)
                return
        else:  # inserted
            return

    def clear_send_cache(self):
        self._last_sent_message = None

    def reset(self):
        pass
        self.send_value(0)

    def reset_state(self):
        self.use_default_message()
        self.suppress_script_forwarding = False
        self.release_parameter()

    def receive_value(self, value):
        value = getattr(value, 'midi_value', value)
        self._verify_value(value)
        self._last_sent_message = None
        self.notify_value(value)
        if self._report_input:
            is_input = True
            self._report_value(value, is_input)

    def set_report_values(self, report_input, report_output):
        pass
        self._report_input = report_input
        self._report_output = report_output

    def _verify_value(self, value):
        if self._msg_type < MIDI_SYSEX_TYPE:
            upper_bound = 16384 if self._msg_type == MIDI_PB_TYPE else 128

    def _report_value(self, value, is_input):
        self._verify_value(value)
        message = str(self.__class__.__name__) + ' ('
        if self._msg_type == MIDI_NOTE_TYPE:
            message += 'Note ' + str(self._msg_identifier) + ', '
        else:  # inserted
            if self._msg_type == MIDI_CC_TYPE:
                message += 'CC ' + str(self._msg_identifier) + ', '
            else:  # inserted
                message += 'PB '
        message += 'Chan. ' + str(self._msg_channel)
        message += ') '
        message += 'received value ' if is_input else 'sent value '
        message += str(value)
        logger.debug(message)

    @property
    def _last_sent_value(self):
        return self._last_sent_message[0] if self._last_sent_message else (-1)