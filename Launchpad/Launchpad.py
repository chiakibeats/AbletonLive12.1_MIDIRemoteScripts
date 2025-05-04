# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad\Launchpad.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from .ConfigurableButtonElement import ConfigurableButtonElement
from .MainSelectorComponent import MainSelectorComponent
SIDE_NOTES = (8, 24, 40, 56, 72, 88, 104, 120)
DRUM_NOTES = (41, 42, 43, 44, 45, 46, 47, 57, 58, 59, 60, 61, 62, 63, 73, 74, 75, 76, 77, 78, 79, 89, 90, 91, 92, 93, 94, 95, 105, 106, 107)

class Launchpad(ControlSurface):
    pass

    def __init__(self, c_instance):
        pass

    def disconnect(self):
        self._suppress_send_midi = True
        for control in self.controls:
            if isinstance(control, ConfigurableButtonElement):
                control.remove_value_listener(self._button_value)
            continue
        self._selector = None
        self._user_byte_write_button.remove_value_listener(self._user_byte_value)
        self._config_button.remove_value_listener(self._config_value)
        ControlSurface.disconnect(self)
        self._suppress_send_midi = False
        self._config_button.send_value(32)
        self._config_button.send_value(0)
        self._config_button = None
        self._user_byte_write_button.send_value(0)
        self._user_byte_write_button = None

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._update_hardware)

    def handle_sysex(self, midi_bytes):
        if len(midi_bytes) == 8 and midi_bytes[1:5] == (0, 32, 41, 6):
            response = int(midi_bytes[5])
            response += int(midi_bytes[6]) << 8
            if response == Live.Application.encrypt_challenge2(self._challenge):
                self._on_handshake_successful()

    def _on_handshake_successful(self):
        self._suppress_send_midi = False
        self.set_enabled(True)

    def build_midi_map(self, midi_map_handle):
        ControlSurface.build_midi_map(self, midi_map_handle)
        if self._selector.mode_index == 1:
            new_channel = self._selector.channel_for_current_mode()
            for note in DRUM_NOTES:
                self._translate_message(MIDI_NOTE_TYPE, note, 0, note, new_channel)

    def _send_midi(self, midi_bytes, optimized=None):
        sent_successfully = False
        if not self._suppress_send_midi:
            sent_successfully = ControlSurface._send_midi(self, midi_bytes, optimized=optimized)
        return sent_successfully

    def _update_hardware(self):
        self._suppress_send_midi = False
        self._wrote_user_byte = True
        self._user_byte_write_button.send_value(1)
        self._suppress_send_midi = True
        self.set_enabled(False)
        self._suppress_send_midi = False
        self._send_challenge()

    def _send_challenge(self):
        for index in range(4):
            challenge_byte = self._challenge >> 8 * index & 127
            self._send_midi((176, 17 + index, challenge_byte))

    def _user_byte_value(self, value):
        if not self._wrote_user_byte:
            enabled = value == 1
            self._control_is_with_automap = not enabled
            self._suppress_send_midi = self._control_is_with_automap
            if not self._control_is_with_automap:
                for control in self.controls:
                    if isinstance(control, ConfigurableButtonElement):
                        control.set_force_next_value()
                    continue
            self._selector.set_mode(0)
            self.set_enabled(enabled)
            self._suppress_send_midi = False
        else:
            self._wrote_user_byte = False

    def _button_value(self, value):
        return

    def _config_value(self, value):
        return

    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        if not self._suppress_session_highlight:
            ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)