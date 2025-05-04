# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\display_target.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import ControlElement
from ableton.v3.control_surface.midi import SYSEX_END
CONFIG_COMMAND = 4
TEXT_COMMAND = 6
CANCEL_TARGET_BYTE = 0
SHOW_TARGET_BYTE = 127
TRIGGER_FIELD_BYTE_OFFSET = 64

class DisplayTargetElement(ControlElement):
    pass

    def __init__(self, header, target, num_fields, disable_caching=False, *a, **k):
        super().__init__(*a, is_private=True, **k)
        self._header = header
        self._target = target
        self._num_fields = num_fields
        self._disable_caching = disable_caching
        self._last_config = None
        self._last_text_fields = [None] * self._num_fields

    def clear_send_cache(self):
        self.reset()

    def reset(self):
        self._last_config = None
        self._last_text_fields = [None] * self._num_fields

    def cancel(self):
        self.reset()
        self._send_config(CANCEL_TARGET_BYTE)

    def send_data(self, config, text_fields, show_immediately=False, trigger=False):
        if self._last_config != config or self._disable_caching:
            self.reset()
            self._send_config(config)
            self._last_config = config
        if self._last_text_fields != text_fields or trigger:
            for i, text in enumerate(text_fields):
                self._send_text(i, text, trigger=trigger)
            self._last_text_fields = text_fields
            if show_immediately:
                self._send_config(SHOW_TARGET_BYTE)
                return
        else:
            return

    def _send_config(self, config):
        self.send_midi(self._header + (CONFIG_COMMAND, self._target, config, SYSEX_END))

    def _send_text(self, field, text, trigger=False):
        if self._last_text_fields[field] != text or trigger:
            if trigger:
                field += TRIGGER_FIELD_BYTE_OFFSET
            self.send_midi(self._header + (TEXT_COMMAND, self._target, field) + text + (SYSEX_END,))
            return
        else:
            return None