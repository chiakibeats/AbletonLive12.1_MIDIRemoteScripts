# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\encoder.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.elements import EncoderElement as EncoderElementBase
from ableton.v3.live import liveobj_valid, parameter_value_to_midi_value
from .display_util import make_blank_parameter_message, make_parameter_message
from .midi import ENCODER_ID_TO_SYSEX_ID, ENCODER_VALUE_HEADER, SYSEX_END

class RealigningEncoderMixin:
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._sysex_header = self._get_sysex_header()
        self._last_mapped_value = None

    def realign_value(self):
        if self._sysex_header:
            value_to_send = self._last_mapped_value or self._last_received_value or 0
            self.send_midi(self._sysex_header + (value_to_send, SYSEX_END))

    def receive_value(self, value):
        super().receive_value(value)
        self._last_mapped_value = None

    def _parameter_value_changed(self):
        if liveobj_valid(self.mapped_object):
            self._last_mapped_value = parameter_value_to_midi_value(self.mapped_object)

class EncoderElement(EncoderElementBase):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._last_sent_parameter_message = None

    def notify_parameter_name(self):
        super().notify_parameter_name()
        self._send_parameter_feedback()

    def notify_parameter_value(self):
        super().notify_parameter_value()
        self._send_parameter_feedback()

    def clear_send_cache(self):
        super().clear_send_cache()
        self._last_sent_parameter_message = None

    def _send_parameter_feedback(self):
        ident = self.message_identifier()
        if liveobj_valid(self.mapped_object):
            self._send_message(make_parameter_message(ident, self.parameter_name, self.parameter_value))
            return
        else:
            self._send_message(make_blank_parameter_message(ident))

    def _send_message(self, message):
        if message != self._last_sent_parameter_message:
            self.send_midi(message)
        self._last_sent_parameter_message = message

class RealigningEncoderElement(RealigningEncoderMixin, EncoderElement):

    def _get_sysex_header(self):
        return ENCODER_VALUE_HEADER + (ENCODER_ID_TO_SYSEX_ID[self.message_identifier()], 0)