# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Keystage\display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from dataclasses import dataclass
from typing import Optional, Tuple
from ableton.v3.control_surface.display import DisplaySpecification, view
from ableton.v3.live import liveobj_name
Lines = Tuple[str, str]

@dataclass
class Content:
    main_lines: Lines
    parameter_displays: Tuple[Lines, ...]

def create_root_view() -> view.View[Optional[Content]]:

    @view.View
    def main_view(state) -> Optional[Content]:
        return Content(main_lines=(liveobj_name(state.target_track.target_track), liveobj_name(state.device.device) or '-'), parameter_displays=tuple(((knob.parameter_name or '-', knob.parameter_value) for knob in state.elements.knobs)))
    return view.CompoundView(view.DisconnectedView(), main_view)

def protocol(elements):

    def display(content: Optional[Content]):
        if content:
            display_main(content.main_lines)
            display_parameters(content.parameter_displays)

    def display_main(main_lines: Lines):
        for element, line in zip(elements.main_display_lines, main_lines):
            element.display_message(line)

    def display_parameters(parameter_displays: Tuple[Lines, ...]):
        for display_line_elements, parameter_lines in zip(elements.parameter_display_lines, parameter_displays):
            for element, line in zip(display_line_elements, parameter_lines):
                element.display_message(line)
            continue
    return display
display_specification = DisplaySpecification(create_root_view=create_root_view, protocol=protocol)