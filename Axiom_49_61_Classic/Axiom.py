# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_49_61_Classic\Axiom.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
import MidiRemoteScript
from _Generic.util import DeviceAppointer
from _Axiom.consts import *
from _Axiom.Encoders import Encoders
from _Axiom.Pads import Pads
from _Axiom.Transport import Transport
from .SliderSection import SliderSection

class Axiom(object):
    pass

    def __init__(self, c_instance):
        self.__c_instance = c_instance
        self.__current_track = self.song().view.selected_track
        self.__current_device = self.__current_track.view.selected_device
        self.song().add_visible_tracks_listener(self.__tracks_changed)
        self.__transport_unit = Transport(self)
        self.__encoder_unit = Encoders(self, True)
        self.__slider_unit = SliderSection(self)
        self.__pad_unit = Pads(self)
        self._device_appointer = DeviceAppointer(song=self.song(), appointed_device_setter=self._set_appointed_device)

    def application(self):
        pass
        return Live.Application.get_application()

    def song(self):
        pass
        return self.__c_instance.song()

    def disconnect(self):
        pass
        self.song().remove_visible_tracks_listener(self.__tracks_changed)
        self._device_appointer.disconnect()
        self.__encoder_unit.disconnect()

    def can_lock_to_devices(self):
        return True

    def suggest_input_port(self):
        pass
        return str('USB Axiom')

    def suggest_output_port(self):
        pass
        return str('USB Axiom')

    def suggest_map_mode(self, cc_no, channel):
        pass
        suggested_map_mode = Live.MidiMap.MapMode.absolute
        if cc_no in AXIOM_ENCODERS:
            suggested_map_mode = Live.MidiMap.MapMode.relative_smooth_binary_offset
        return suggested_map_mode

    def show_message(self, message):
        self.__c_instance.show_message(message)

    def supports_pad_translation(self):
        return True

    def connect_script_instances(self, instanciated_scripts):
        pass
        return

    def request_rebuild_midi_map(self):
        pass
        self.__c_instance.request_rebuild_midi_map()

    def send_midi(self, midi_event_bytes):
        pass
        self.__c_instance.send_midi(midi_event_bytes)

    def refresh_state(self):
        pass
        return

    def build_midi_map(self, midi_map_handle):
        pass
        script_handle = self.__c_instance.handle()
        self.__transport_unit.build_midi_map(script_handle, midi_map_handle)
        self.__encoder_unit.build_midi_map(script_handle, midi_map_handle)
        self.__slider_unit.build_midi_map(script_handle, midi_map_handle)
        self.__pad_unit.build_midi_map(script_handle, midi_map_handle)
        self.__c_instance.set_pad_translation(PAD_TRANSLATION)

    def update_display(self):
        pass
        if self.__transport_unit:
            self.__transport_unit.refresh_state()
            return
        else:
            return None

    def receive_midi(self, midi_bytes):
        pass
        if midi_bytes[0] & 240 == CC_STATUS:
            channel = midi_bytes[0] & 15
            cc_no = midi_bytes[1]
            cc_value = midi_bytes[2]
            if list(AXIOM_TRANSPORT).count(cc_no) > 0:
                self.__transport_unit.receive_midi_cc(cc_no, cc_value)
            elif list(AXIOM_BUTTONS).count(cc_no) > 0:
                self.__slider_unit.receive_midi_cc(cc_no, cc_value, channel)
            elif list(AXIOM_ENCODERS).count(cc_no) > 0:
                self.__encoder_unit.receive_midi_cc(cc_no, cc_value, channel)
            elif list(AXIOM_PADS).count(cc_no) > 0:
                self.__pad_unit.receive_midi_cc(cc_no, cc_value, channel)
                return
            else:
                return None
        elif midi_bytes[0] == 240:
            return
        else:
            return None

    def lock_to_device(self, device):
        self.__encoder_unit.lock_to_device(device)

    def unlock_from_device(self, device):
        self.__encoder_unit.unlock_from_device(device)

    def _set_appointed_device(self, device):
        self.__encoder_unit.set_appointed_device(device)

    def __tracks_changed(self):
        self.request_rebuild_midi_map()

    def bank_changed(self, new_bank):
        if self.__encoder_unit.set_bank(new_bank):
            self.request_rebuild_midi_map()

    def restore_bank(self, bank):
        self.__encoder_unit.restore_bank(bank)
        self.request_rebuild_midi_map()

    def instance_identifier(self):
        return self.__c_instance.instance_identifier()