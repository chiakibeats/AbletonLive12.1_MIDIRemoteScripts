# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\AxiomPro.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.LogicalDisplaySegment import LogicalDisplaySegment
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from .DisplayingMixerComponent import DisplayingMixerComponent
from .EncoderMixerModeSelector import EncoderMixerModeSelector
from .MixerOrDeviceModeSelector import MixerOrDeviceModeSelector
from .NotifyingMixerComponent import NotifyingMixerComponent
from .PageableDeviceComponent import PageableDeviceComponent
from .PeekableEncoderElement import PeekableEncoderElement
from .SelectButtonModeSelector import SelectButtonModeSelector
from .TransportViewModeSelector import TransportViewModeSelector
SYSEX_START = (240, 0, 1, 5, 32, 127)
PAD_TRANSLATIONS = ((0, 2, 85, 15), (1, 2, 86, 15), (2, 2, 87, 15), (3, 2, 88, 15), (0, 3, 81, 15), (1, 3, 82, 15), (2, 3, 83, 15), (3, 3, 84, 15))

class AxiomPro(ControlSurface):
    pass

    def __init__(self, c_instance):
        pass

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self._waiting_for_first_response = True
        self.schedule_message(10, self._send_midi, SYSEX_START + (32, 46, 247))

    def handle_sysex(self, midi_bytes):
        if midi_bytes[0:-2] == SYSEX_START + (32,):
            msg_id_byte = midi_bytes[-2]
            is_setup_response = msg_id_byte in (46, 38)
            has_sliders = msg_id_byte == 46
            if is_setup_response:
                if self._waiting_for_first_response:
                    self._waiting_for_first_response = False
                    self._display_on_button.send_value(0)
                    for component in self.components:
                        component.set_enabled(True)
                    self._display_on_button.send_value(127)
                    self._send_midi(SYSEX_START + (16, 247))
                    self._send_midi(SYSEX_START + (17, 3, 0, 1, 65, 98, 108, 101, 116, 111, 110, 32, 76, 105, 118, 101, 32, 67, 111, 110, 116, 114, 111, 108, 32, 0, 1, 4, 83, 117, 114, 102, 97, 99, 101, 32, 118, 49, 46, 48, 46, 48, 46, 247))
                self._mixer_encoder_modes.set_show_volume_page(not has_sliders)
                for display in self._displays:
                    display.set_block_messages(False)
                self.schedule_message(25, self._refresh_displays)
                return
            elif msg_id_byte == 43:
                self._send_midi(SYSEX_START + (16, 247))
                for display in self._displays:
                    if display is self._track_display:
                        display.update()
                        continue
                    else:
                        display.set_block_messages(True)
                        continue

    def disconnect(self):
        ControlSurface.disconnect(self)
        self._send_midi(SYSEX_START + (32, 0, 247))
        self._send_midi(SYSEX_START + (16, 247))
        self._send_midi(SYSEX_START + (17, 3, 0, 4, 65, 98, 108, 101, 116, 111, 110, 32, 76, 105, 118, 101, 32, 67, 111, 110, 116, 114, 111, 108, 32, 0, 1, 4, 83, 117, 114, 102, 97, 99, 101, 32, 67, 108, 111, 115, 101, 100, 46, 247))