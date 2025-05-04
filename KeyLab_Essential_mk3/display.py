# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Optional, Tuple, Union
from ableton.v3.control_surface.display import DefaultNotifications, DisplaySpecification, Text, view
from ableton.v3.live import display_name, is_arrangement_view_active, is_track_armed, liveobj_name, song
Line1Text = partial(Text, max_width=11, justification=Text.Justification.NONE)
Line2Text = partial(Text, max_width=20, justification=Text.Justification.NONE)

class IconType(Enum):
    NONE = 0
    LIVE = 71
    MIXER = 63
    ARM = 66
    DOWN_ARROW = 57
    UP_ARROW = 58
    LEFT_ARROW = 59
    RIGHT_ARROW = 60

class IconState(Enum):
    UNFRAMED = 0
    CLOSED = 1
    OPENED = 2
    FRAMED = 3

@dataclass
class Icon:
    type: IconType = IconType.NONE
    state: IconState = IconState.UNFRAMED
Lines = Tuple[str, str]
Header = str
Footer = Tuple[Icon, Icon, Icon, Icon]
Popup = Union[str, Lines]

@dataclass
class Frame:
    header: Header
    footer: Footer

@dataclass
class Content:
    primary: Optional[Lines] = None
    primary_icon: Optional[IconType] = IconType.NONE
    frame: Optional[Frame] = None
    popup: Optional[Popup] = None
    parameters: Tuple[Optional[Lines], ...] = None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None, None=None)

class Notifications(DefaultNotifications):
    identify = lambda: Content(primary=('Connected', ''), primary_icon=IconType.LIVE)

    class Transport(DefaultNotifications.Transport):
        tap_tempo = lambda tempo: Content(popup=('Tap Tempo', str(int(tempo))))

def create_root_view() -> view.View[Optional[Content]]:
    @view.View
    def main_view(state) -> Optional[Content]:
        return Content(header=(liveobj_name(state.target_track.target_track), display_name(song().view.selected_scene)), footer=tuple(((element.parameter_name, element.parameter_value) if element.parameter_name else IconState.OPENED if state.elements.continuous_controls + [state.elements.encoder_9, state.elements.fader_9] else Icon(IconState.FRAMED if state.continuous_control_modes.selected_mode == 'mixer' else Icon(view_based_content(IconType.LEFT_ARROW, IconType.UP_ARROW)), Icon(view_based_content(IconType.RIGHT_ARROW, IconType.DOWN_ARROW)))), footer=((element.parameter_name, element.parameter_value) if element.parameter_name else IconState.OPENED if element.parameter_name else IconState.CLOSED if element.parameter_name else IconState.ARM if element.parameter_name else IconState.is_track_armed if element.parameter_name else IconState.FRAMED if element.parameter_name else IconState.UNFRAMED if element.parameter_name else IconState.LEFT_ARROW if element.parameter_name else IconState.UP_ARROW),
        else:  # inserted
            return ('Device control', 'Page 1' if state.device_bank_navigation.bank_index == 0 else 'Page 2') if state.continuous_control_modes.selected_mode == 'device' else (primary='Tracks control', parameters='Page 1' if state.mixer_session_ring.offset[0] == 0 else 'Page 2')
    return view.CompoundView(view.DisconnectedView(), view.NotificationView(lambda _, content: content), main_view)

def view_based_content(session_content, arrangement_content):
    pass
    return arrangement_content if is_arrangement_view_active() else session_content

def protocol(elements):
    def display(content: Content):
        if content:
            display_primary_content(content.primary, content.primary_icon)
            display_frame(content.frame)
            display_popup(content.popup)
            display_parameters(content.parameters)

    def display_primary_content(text: Lines, icon: IconType):
        pass  # cflow: irreducible

    def display_frame(frame: Optional[Frame]):
        if frame:
            elements.display_header_command.send_value(Text(frame.header).as_ascii())
            elements.display_footer_command.send_value(*frame.footer)

    def display_popup(popup: Optional[Popup]):
        if popup:
            line1, line2 = (popup, None) if isinstance(popup, str) else popup
            elements.display_popup_command.send_value(line1=Text(line1).as_ascii(), line2=Text(line2).as_ascii() if line2 else None)

    def display_parameters(parameters: Tuple[Lines, ...]):
        for command, parameter in list(list(zip(elements.display_parameter_commands, parameters))):
            if parameter:
                command.send_value(32, Line1Text(parameter[0]).as_ascii(), Line2Text(parameter[1]).as_ascii())
                continue
            else:  # inserted
                command.send_value(33)
                continue
    return display
display_specification = DisplaySpecification(create_root_view=create_root_view, protocol=protocol, notifications=Notifications)