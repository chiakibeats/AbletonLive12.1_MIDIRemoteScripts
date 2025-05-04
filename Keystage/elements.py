# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Keystage\elements.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import ElementsBase
from ableton.v3.control_surface.display import Text
from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START

class Elements(ElementsBase):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_button(41, 'Play_Button')
        self.add_button(42, 'Stop_Button')
        self.add_button(43, 'Rewind_Button')
        self.add_button(44, 'Fastforward_Button')
        self.add_button(45, 'Record_Button')
        self.add_button(46, 'Loop_Button')
        self.add_button(47, 'Tempo_Button')
        self.add_button(48, 'Metronome_Button')
        self.add_button(49, 'Undo_Button')
        self.add_button(58, 'Down_Button')
        self.add_button(59, 'Up_Button')
        self.add_encoder_matrix([range(8)], 'Knobs')
        self.add_sysex_element((SYSEX_START, 66), 'Firmware_Element')

    def add_display_lines(self, sysex_header):
        self.main_display_lines = (self.add_display_line(sysex_header, 'Display_Main_0', max_width=6, justification=Text.Justification.RIGHT), self.add_display_line(sysex_header, 'Display_Main_1', line_index=1))
        self.parameter_display_lines = [(self.add_display_line(sysex_header, 'Display_P{}_Name', display_index=i), self.add_display_line(sysex_header, 'Display_P{}_Value', display_index=i, line_index=1)) for i in range(1, 9)]

    def add_display_line(self, sysex_header, name, max_width=12, display_index=0, line_index=0, justification=Text.Justification.CENTER):
        line_header = sysex_header + (max_width + 3, 0, 0, 40, display_index, line_index)
        name = name.format(display_index)
        self.add_sysex_display_line(line_header, name, lambda text: line_header + text + (SYSEX_END,), default_formatting=Text(max_width=max_width, justification=justification))
        return getattr(self, name.lower())