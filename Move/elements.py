# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\elements.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.control_surface import MIDI_NOTE_TYPE, ElementsBase, MapMode, PrioritizedResource, create_matrix_identifiers
from ableton.v3.control_surface.elements import ButtonMatrixElement, LockableButtonElement, LockableComboElement, TouchElement
from . import midi
from .display_util import DisplayElement
from .encoder import ColoredEncoderElement, MoveEncoderElement
from .step_button import StepButtonComboElement
MAP_MODE = MapMode.LinearTwoCompliment
ENCODER_SENSITIVITY = 2.0

class Elements(ElementsBase):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_modifier_button(60, 'Duplicate_Button')
        self.add_modifier_button(86, 'Record_Button', is_rgb=True)
        self.add_modifier_button(88, 'Mute_Button')
        self.add_modifier_button(119, 'Delete_Button')
        self.add_button(3, 'Wheel_Push_Button')
        self.add_button(9, 'Wheel_Touch_Button', msg_type=MIDI_NOTE_TYPE)
        self.add_button(50, 'Layout_Button')
        self.add_button(51, 'Back_Button')
        self.add_button(52, 'Capture_Button')
        self.add_button(54, 'Minus_Button')
        self.add_button(55, 'Plus_Button')
        self.add_button(56, 'Undo_Button')
        self.add_button(58, 'Loop_Button')
        self.add_button(62, 'Left_Button')
        self.add_button(63, 'Right_Button')
        self.add_button(85, 'Play_Button', is_rgb=True)
        self.add_button(118, 'Sampling_Button', is_rgb=True)
        self.add_element('Shift_Button', LockableButtonElement, identifier=49, double_click_time=0.4, resource_type=PrioritizedResource)
        self.add_modified_control(control=self.minus_button, modifier=self.shift_button)
        self.add_modified_control(control=self.plus_button, modifier=self.shift_button)
        self.add_modified_control(control=self.left_button, modifier=self.shift_button)
        self.add_modified_control(control=self.right_button, modifier=self.shift_button)
        self.add_modified_control(control=self.layout_button, modifier=self.shift_button)
        self.add_modified_control(control=self.wheel_push_button, modifier=self.mute_button)
        self.add_lockable_combo_with_shift(self.play_button)
        self.add_lockable_combo_with_shift(self.undo_button)
        self.add_button_matrix(create_matrix_identifiers(40, 44, flip_rows=True), 'Track_State_Buttons', is_rgb=True)
        self.add_button_matrix([[16, 17, 18, 19], [20, 21, 22, 23], [24, 25, 26, 27], [28, 29, 30, 31]], 'Step_Buttons', msg_type=MIDI_NOTE_TYPE, is_rgb=True)
        self.track_select_matrix = ButtonMatrixElement(name='Track_Select_Matrix', rows=[self.step_buttons_raw[slice(0, 14, 2)]], is_private=True)
        self.track_stop_matrix = ButtonMatrixElement(name='Track_Stop_Matrix', rows=[self.step_buttons_raw[slice(1, 14, 2)]], is_private=True)
        shifted_step_button_indices = (1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15)
        for index in shifted_step_button_indices:
            self.add_element('Step_Button_{}_With_Shift'.format(index), StepButtonComboElement, control=self.step_buttons_raw[index], modifier=self.shift_button)
        self.add_button_matrix(create_matrix_identifiers(68, 100, 8, flip_rows=True), 'Pads', msg_type=MIDI_NOTE_TYPE, is_rgb=True)
        self.add_submatrix(self.pads, 'Pads_Columns_0_thru_6', columns=(0, 7))
        self.add_submatrix(self.pads, 'Pads_Column_7', columns=(7, 8))
        self.add_encoder(14, 'Wheel', map_mode=MAP_MODE)
        self.add_element('Volume_Encoder', MoveEncoderElement, identifier=79, map_mode=MAP_MODE, sensitivity_modifier=self.shift_button)
        self.add_matrix([range(71, 79)], 'Encoders', map_mode=MAP_MODE, sensitivity_modifier=self.shift_button, element_factory=ColoredEncoderElement)
        self.add_matrix([range(9)], 'Encoder_Touch_Elements', msg_type=MIDI_NOTE_TYPE, resource_type=PrioritizedResource, element_factory=lambda identifier, **k: TouchElement(identifier, encoder=self.encoders_raw[identifier] if identifier < 8 else self.volume_encoder, **k))
        self.add_submatrix(self.encoder_touch_elements, 'Parameter_Touch_Elements', columns=(0, 8))
        self.add_element('Display', DisplayElement)
        self.add_sysex_element(midi.make_power_state_message()[:-1], 'Power_State_Element')
        self.add_sysex_element(midi.make_get_control_mode_message()[:-1], 'Control_Mode_Element')
        self.add_sysex_element(midi.make_get_led_brightness_message()[:-1], 'LED_Brightness_Element')

    def add_lockable_combo_with_shift(self, control):
        self.add_modified_control(control=control, modifier=self.shift_button, name='{}_With_Shift'.format(control.name), element_factory=LockableComboElement)