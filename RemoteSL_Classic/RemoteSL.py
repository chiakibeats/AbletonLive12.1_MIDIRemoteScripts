# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL_Classic\RemoteSL.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
import MidiRemoteScript
from _Generic.util import DeviceAppointer
from .consts import *
from .DisplayController import DisplayController
from .EffectController import EffectController
from .MixerController import MixerController

class RemoteSL(object):
    pass

    def __init__(self, c_instance):
        self.__c_instance = c_instance
        self.__automap_has_control = False
        self.__display_controller = DisplayController(self)
        self.__effect_controller = EffectController(self, self.__display_controller)
        self.__mixer_controller = MixerController(self, self.__display_controller)
        self.__components = [self.__effect_controller, self.__mixer_controller, self.__display_controller]
        self.__update_hardware_delay = (-1)
        self._device_appointer = DeviceAppointer(song=self.song(), appointed_device_setter=self._set_appointed_device)

    def disconnect(self):
        pass
        for c in self.__components:
            c.disconnect()
        self._device_appointer.disconnect()
        self.send_midi(ALL_LEDS_OFF_MESSAGE)
        self.send_midi(GOOD_BYE_SYSEX_MESSAGE)

    def application(self):
        pass
        return Live.Application.get_application()

    def song(self):
        pass
        return self.__c_instance.song()

    def suggest_input_port(self):
        pass
        return 'RemoteSL'

    def suggest_output_port(self):
        pass
        return 'RemoteSL'

    def can_lock_to_devices(self):
        pass
        return True

    def lock_to_device(self, device):
        pass
        self.__effect_controller.lock_to_device(device)

    def unlock_from_device(self, device):
        pass
        self.__effect_controller.unlock_from_device(device)

    def _set_appointed_device(self, device):
        pass
        self.__effect_controller.set_appointed_device(device)

    def toggle_lock(self):
        pass
        self.__c_instance.toggle_lock()

    def suggest_map_mode(self, cc_no, channel):
        pass
        result = Live.MidiMap.MapMode.absolute
        if cc_no in fx_encoder_row_ccs:
            result = Live.MidiMap.MapMode.relative_smooth_signed_bit
        return result

    def restore_bank(self, bank):
        self.__effect_controller.restore_bank(bank)

    def supports_pad_translation(self):
        return True

    def show_message(self, message):
        self.__c_instance.show_message(message)

    def instance_identifier(self):
        return self.__c_instance.instance_identifier()

    def connect_script_instances(self, instanciated_scripts):
        pass
        return

    def request_rebuild_midi_map(self):
        pass
        self.__c_instance.request_rebuild_midi_map()

    def send_midi(self, midi_event_bytes):
        pass
        if not self.__automap_has_control:
            self.__c_instance.send_midi(midi_event_bytes)

    def refresh_state(self):
        pass
        self.__update_hardware_delay = 5

    def __update_hardware(self):
        self.__automap_has_control = False
        self.send_midi(WELCOME_SYSEX_MESSAGE)
        for c in self.__components:
            c.refresh_state()

    def build_midi_map(self, midi_map_handle):
        pass
        if not self.__automap_has_control:
            for c in self.__components:
                c.build_midi_map(self.__c_instance.handle(), midi_map_handle)
        self.__c_instance.set_pad_translation(PAD_TRANSLATION)

    def update_display(self):
        pass
        if self.__update_hardware_delay > 0:
            self.__update_hardware_delay -= 1
            if self.__update_hardware_delay == 0:
                self.__update_hardware()
                self.__update_hardware_delay = (-1)
        for c in self.__components:
            c.update_display()
        return None

    def receive_midi(self, midi_bytes):
        pass
        if midi_bytes[0] & 240 in (NOTE_ON_STATUS, NOTE_OFF_STATUS):
            channel = midi_bytes[0] & 15
            note = midi_bytes[1]
            velocity = midi_bytes[2]
            if note in fx_notes:
                self.__effect_controller.receive_midi_note(note, velocity)
                return
            else:  # inserted
                if note in mx_notes:
                    self.__mixer_controller.receive_midi_note(note, velocity)
                    return
                else:  # inserted
                    print('unknown MIDI message %s' % str(midi_bytes))
                    return
        else:  # inserted
            if midi_bytes[0] & 240 == CC_STATUS:
                channel = midi_bytes[0] & 15
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]
                if cc_no in fx_ccs:
                    self.__effect_controller.receive_midi_cc(cc_no, cc_value)
                    return
                else:  # inserted
                    if cc_no in mx_ccs:
                        self.__mixer_controller.receive_midi_cc(cc_no, cc_value)
                        return
                    else:  # inserted
                        print('unknown MIDI message %s' % str(midi_bytes))
                        return
            else:  # inserted
                if midi_bytes[0] == 240:
                    if len(midi_bytes) == 13 and midi_bytes[1:4] == (0, 32, 41) and (midi_bytes[8] == ABLETON_PID) and (midi_bytes[10] == 1):
                                    self.__automap_has_control = midi_bytes[11] == 0
                                    support_mkII = midi_bytes[6] * 100 + midi_bytes[7] >= 1800
                                    if not self.__automap_has_control:
                                        self.send_midi(ALL_LEDS_OFF_MESSAGE)
                                    for c in self.__components:
                                        c.set_support_mkII(support_mkII)
                                        if not self.__automap_has_control:
                                            c.refresh_state()
                                        continue
                                    self.request_rebuild_midi_map()
                                    return
                                else:  # inserted
                                    return None
                            else:  # inserted
                                return None
                        else:  # inserted
                            return None
                    else:  # inserted
                        return None
                else:  # inserted
                    print('unknown MIDI message %s' % str(midi_bytes))