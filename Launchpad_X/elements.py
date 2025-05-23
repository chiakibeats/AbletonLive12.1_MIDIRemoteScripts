# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\elements.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ableton.v2.base import depends
from ableton.v2.control_surface.elements import ButtonMatrixElement, ColorSysexElement, SysexElement
from novation import sysex
from novation.launchpad_elements import BUTTON_FADER_COLOR_CHANNEL, SESSION_WIDTH, LaunchpadElements, create_button, create_slider
from . import sysex_ids as ids

class Elements(LaunchpadElements):
    model_id = ids.LP_X_ID
    default_layout = sysex.NOTE_LAYOUT_BYTE
    button_fader_cc_offset = 21

    @depends(skin=None)
    def __init__(self, skin=None, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self._create_drum_pads()
        self._create_scale_pads()
        self._create_scale_feedback_switch()
        self.note_mode_button = create_button(96, 'Note_Mode_Button')
        self.custom_mode_button = create_button(97, 'Custom_Mode_Button')
        self.record_button = create_button(98, 'Record_Button')
        self.button_faders = ButtonMatrixElement(rows=[[create_slider(index + self.button_fader_cc_offset, 'Button_Fader_{}'.format(index)) for index in range(SESSION_WIDTH)]], name='Button_Faders')
        self.button_fader_color_elements_raw = [create_button(index + self.button_fader_cc_offset, 'Button_Fader_Color_Element_{}'.format(index), channel=BUTTON_FADER_COLOR_CHANNEL) for index in range(SESSION_WIDTH)]
        self.button_fader_color_elements = ButtonMatrixElement(rows=[self.button_fader_color_elements_raw], name='Button_Fader_Color_Elements')
        self.note_layout_switch = SysexElement(name='Note_Layout_Switch', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (ids.LP_X_ID, sysex.NOTE_LAYOUT_COMMAND_BYTE, v, sysex.SYSEX_END_BYTE), default_value=sysex.SCALE_LAYOUT_BYTE)
        session_button_color_identifier = sysex.STD_MSG_HEADER + (ids.LP_X_ID, 20)
        self.session_button_color_element = ColorSysexElement(name='Session_Button_Color_Element', sysex_identifier=session_button_color_identifier, send_message_generator=lambda v: session_button_color_identifier + v + (sysex.SYSEX_END_BYTE,), skin=skin)
        self.button_fader_setup_element = SysexElement(name='Button_Fader_Setup_Element', send_message_generator=partial(self._fader_setup_message_generator, 0))