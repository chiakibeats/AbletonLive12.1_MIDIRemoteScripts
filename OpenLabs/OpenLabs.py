# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\OpenLabs\OpenLabs.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ControlSurface import ControlSurface
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SliderElement import SliderElement
from .SpecialDeviceComponent import SpecialDeviceComponent
from .SpecialTransportComponent import SpecialTransportComponent

class OpenLabs(ControlSurface):
    pass

    def __init__(self, c_instance):
        pass

    def handle_sysex(self, midi_bytes):
        return

    def _setup_mixer_control(self):
        is_momentary = True
        num_tracks = 8
        num_returns = 7
        mixer = MixerComponent(num_tracks, num_returns)
        for track in range(num_tracks):
            strip = mixer.channel_strip(track)
            strip.set_volume_control(SliderElement(MIDI_CC_TYPE, 15, 54 - track))
            strip.set_pan_control(SliderElement(MIDI_CC_TYPE, 15, 80 - track))
            strip.set_mute_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 117 - track))
            strip.set_invert_mute_feedback(True)
        for track in range(num_returns):
            strip = mixer.return_strip(track)
            strip.set_volume_control(SliderElement(MIDI_CC_TYPE, 15, 10 + track))
        mixer.set_bank_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 108), ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 109))
        mixer.set_crossfader_control(SliderElement(MIDI_CC_TYPE, 15, 9))
        mixer.master_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, 15, 46))
        session = SessionComponent(0, 0)
        session.set_select_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 95), ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 92))
        session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 91))

    def _setup_device_and_transport_control(self):
        is_momentary = True
        device_param_controls = []
        for index in range(8):
            device_param_controls.append(EncoderElement(MIDI_CC_TYPE, 15, 62 - index, Live.MidiMap.MapMode.absolute))
        device = SpecialDeviceComponent()
        device.set_bank_nav_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 107), ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 106))
        device.set_parameter_controls(tuple(device_param_controls))
        self.set_device_component(device)
        transport = SpecialTransportComponent()
        transport.set_play_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 20))
        transport.set_stop_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 21))
        transport.set_record_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 22))
        transport.set_seek_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 24), ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 25))
        transport.set_tap_tempo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 94))
        transport.set_undo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 23))
        transport.set_redo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 27))
        transport.set_bts_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 26))