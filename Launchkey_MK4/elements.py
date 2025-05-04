# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\elements.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import nop
from ableton.v3.control_surface import MIDI_NOTE_TYPE, ElementsBase, MapMode, PrioritizedResource, create_matrix_identifiers
from . import midi
from .display_target import DisplayTargetElement
from .multi_button import MultiButtonElement

class LaunchkeyCommonElements(ElementsBase):
    pass

    def __init__(self, sysex_header, *a, **k):
        super().__init__(*a, **k)
        self.add_modifier_button(105, 'Pad_Function_Button')
        self.add_multi_button(29, 64, 'Pad_Mode_Element')
        self.add_multi_button(30, 65, 'Encoder_Mode_Element')
        self.add_multi_button(60, 82, 'Scale_Behavior_Element')
        self.add_multi_button(61, 81, 'Root_Note_Element')
        self.add_multi_button(62, 80, 'Scale_Type_Element')
        self.add_multi_button(63, 72, 'Shift_Button', resource_type=PrioritizedResource)
        self.add_button(73, 'Arp_Button', channel=6, is_private=True)
        self.add_button(74, 'Scale_Button', channel=6, is_private=True)
        self.add_button(104, 'Scene_Launch_Button')
        self.add_mono_button(51, 'Encoder_Up_Button')
        self.add_mono_button(52, 'Encoder_Down_Button')
        self.add_mono_button(106, 'Pad_Up_Button')
        self.add_mono_button(107, 'Pad_Down_Button')
        self.add_mono_button(115, 'Play_Button')
        self.add_mono_button(117, 'Record_Button')
        self.add_shifted_control(self.encoder_up_button)
        self.add_shifted_control(self.encoder_down_button)
        self.add_shifted_control(self.play_button)
        self.add_modified_control(control=self.pad_down_button, modifier=self.pad_function_button)
        self.add_button_matrix(create_matrix_identifiers(36, 52, width=4, flip_rows=True), 'Drum_Pads', msg_type=MIDI_NOTE_TYPE, channels=9)
        self.add_button_matrix(midi.MAIN_PAD_IDS, 'Main_Pads', msg_type=MIDI_NOTE_TYPE)
        self.add_submatrix(self.main_pads, 'Lower_Pads', rows=(1, 2))
        self.add_button_matrix([range(128)], 'Keyboard', msg_type=MIDI_NOTE_TYPE, channels=8, is_private=True)
        self.add_encoder_matrix([range(85, 93)], 'Encoders', map_mode=MapMode.LinearBinaryOffset, channels=15)
        self.add_button_matrix([range(85, 93)], 'Encoder_Touch_Elements', channels=14, is_private=True)
        self.add_sysex_element(midi.make_connection_message(sysex_header)[:-2], 'Connection_Element')
        self.pad_mode_element.send_value = nop
        self.encoder_mode_element.send_value = nop
        self.add_display_command_for_target('Static', sysex_header, 32, 9)
        self.add_display_command_for_target('Temp', sysex_header, 33, 3, disable_caching=True)
        self.add_display_command_for_target('Daw_Label', sysex_header, 34, 1)
        self.add_display_command_for_target('Mixer_Label', sysex_header, 36, 1)
        for i in range(8):
            self.add_display_command_for_target('Encoder_{}'.format(i), sysex_header, 21 + i, 3)
        if sysex_header == midi.MK4_SYSEX_HEADER:
            for i in range(9):
                self.add_display_command_for_target('Fader_{}'.format(i), sysex_header, 5 + i, 3)
    pass

    def add_display_command_for_target(self, name, sysex_header, target, num_fields, disable_caching=False):
        self.add_element('{}_Display_Command'.format(name), DisplayTargetElement, sysex_header, target, num_fields, disable_caching=disable_caching)

    def add_multi_button(self, identifier, secondary_identifier, name, **k):
        self.add_element(name, MultiButtonElement, identifier, secondary_identifier=secondary_identifier, channel=6, **k)

    def add_mono_button(self, identifier, name):
        self.add_button(identifier, name, led_channel=3)

    def add_shifted_control(self, button):
        self.add_modified_control(control=button, modifier=self.shift_button)

class Elements(LaunchkeyCommonElements):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_multi_button(31, 66, 'Fader_Mode_Element')
        self.add_button(45, 'Fader_Button_Mode_Button')
        self.add_mono_button(74, 'Capture_Button')
        self.add_mono_button(75, 'Quantise_Button')
        self.add_mono_button(76, 'Metronome_Button')
        self.add_mono_button(77, 'Undo_Button')
        self.add_mono_button(102, 'Track_Right_Button')
        self.add_mono_button(103, 'Track_Left_Button')
        self.add_mono_button(108, 'Shifted_Track_Right_Button')
        self.add_mono_button(109, 'Shifted_Track_Left_Button')
        self.add_mono_button(116, 'Stop_Button')
        self.add_mono_button(118, 'Loop_Button')
        self.add_shifted_control(self.undo_button)
        self.add_button_matrix([range(37, 45)], 'Fader_Buttons')
        self.add_encoder(13, 'Master_Fader', channel=15)
        self.add_button(13, 'Master_Fader_Touch_Element', channel=14, is_private=True)
        self.add_encoder_matrix([range(5, 13)], 'Faders', channels=15)
        self.add_button_matrix([range(5, 13)], 'Fader_Touch_Elements', channels=14, is_private=True)