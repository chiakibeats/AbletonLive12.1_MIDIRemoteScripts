# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_Mini32\AxiomAirMini32.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ControlSurface import ControlSurface
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from Axiom_DirectLink.BestBankDeviceComponent import BestBankDeviceComponent
from .DeviceNavComponent import DeviceNavComponent
from .EncoderMixerModeSelector import EncoderMixerModeSelector
from .MixerOrDeviceModeSelector import MixerOrDeviceModeSelector
SYSEX_START = (240, 0, 1, 5, 32, 127)
ENGAGE_HYPERCONTROL = (32, 60, 247)
DISABLE_HYPERCONTROL = (32, 0, 247)
NUM_TRACKS = 8
GLOBAL_CHANNEL = 15
PAD_TRANSLATIONS = ((0, 0, 85, 14), (1, 0, 86, 14), (2, 0, 87, 14), (3, 0, 88, 14), (0, 1, 81, 14), (1, 1, 82, 14), (2, 1, 83, 14), (3, 1, 84, 14), (0, 2, 85, 15), (1, 2, 86, 15), (2, 2, 87, 15), (3, 2, 88, 15), (0, 3, 81, 15), (1, 3, 82, 15), (2, 3, 83, 15), (3, 3, 84, 15))

def make_button(cc_no):
    is_momentary = True
    return ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no)

def make_encoder(cc_no):
    return EncoderElement(MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no, Live.MidiMap.MapMode.absolute)

class AxiomAirMini32(ControlSurface):
    pass

    def __init__(self, c_instance):
        pass

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._send_midi, SYSEX_START + ENGAGE_HYPERCONTROL)
        for component in self.components:
            if isinstance(component, ModeSelectorComponent):
                component.set_mode(0)
            continue

    def handle_sysex(self, midi_bytes):
        return

    def disconnect(self):
        ControlSurface.disconnect(self)
        self._send_midi(SYSEX_START + DISABLE_HYPERCONTROL)

class SpecialMixerComponent(MixerComponent):
    pass

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return SpecialChanStripComponent()

class SpecialChanStripComponent(ChannelStripComponent):
    pass

    def set_arm_button(self, button):
        if button != self._arm_button:
            if self._arm_button != None:
                self._arm_button.remove_value_listener(self._arm_value)
                self._arm_button.reset()
            self._arm_pressed = False
            self._arm_button = button
            if self._arm_button != None:
                self._arm_button.add_value_listener(self._arm_value)
            self.update()
            return