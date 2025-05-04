# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_3rd_Gen\Oxygen_3rd_Gen.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from .SpecialMixerComponent import SpecialMixerComponent
from .TransportViewModeSelector import TransportViewModeSelector
IDENTITY_REQUEST = (240, 126, 127, 6, 1, 247)
IDENTITY_RESPONSE = (240, 126, 127, 6, 2)
NUM_TRACKS = 8
GLOBAL_CHANNEL = 15

class Oxygen_3rd_Gen(ControlSurface):
    pass

    def __init__(self, c_instance):
        pass

    def disconnect(self):
        self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = None
        ControlSurface.disconnect(self)

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._send_midi, IDENTITY_REQUEST)

    def handle_sysex(self, midi_bytes):
        if midi_bytes[0:5] == IDENTITY_RESPONSE and midi_bytes[10] == 38:
            self._mixer.master_strip().set_volume_control(None)
            self._mixer.selected_strip().set_volume_control(self._master_slider)

    def _shift_value(self, value):
        for index in range(NUM_TRACKS):
            if value == 0:
                self._mixer.channel_strip(index).set_solo_button(None)
                self._mixer.channel_strip(index).set_mute_button(self._mute_solo_buttons[index])
                self._mixer.set_bank_buttons(None, None)
                self._mixer.set_select_buttons(self._track_up_button, self._track_down_button)
                continue
            else:
                self._mixer.channel_strip(index).set_mute_button(None)
                self._mixer.channel_strip(index).set_solo_button(self._mute_solo_buttons[index])
                self._mixer.set_select_buttons(None, None)
                self._mixer.set_bank_buttons(self._track_up_button, self._track_down_button)
                continue