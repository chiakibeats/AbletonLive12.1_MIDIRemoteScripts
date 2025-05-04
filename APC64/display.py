# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from dataclasses import dataclass
from math import floor
from typing import Optional, Tuple
from ableton.v3.control_surface.display import DefaultNotifications, DisplaySpecification, Text, view
from ableton.v3.live import display_name, liveobj_name, parameter_owner, song
from .colors import SimpleColor, make_color_for_liveobj
CONTROL_SURFACE_DISPLAY_PAD_MODES = ['session', 'session_overview', 'drum']

@dataclass
class Content:
    header_color: SimpleColor
    lines: Optional[Tuple[str, str, str]]

class Notifications(DefaultNotifications):
    controlled_range = DefaultNotifications.DefaultText()
    generic = DefaultNotifications.DefaultText()

    class Transport(DefaultNotifications.Transport):
        metronome = DefaultNotifications.DefaultText()
        record_quantize = DefaultNotifications.DefaultText()

    class Track(DefaultNotifications.Track):
        select = 'default_lines'

    class Device(DefaultNotifications.Device):
        select = 'default_lines'
        bank = 'default_lines'
        lock = DefaultNotifications.DefaultText()

def get_active_parameter(state):
    return state.active_parameter.parameter or (state.elements.encoder.mapped_object if state.encoder_modes.selected_mode in ('fixed_length', 'quantize') else None)

def get_default_lines(state):
    return (liveobj_name(state.target_track.target_track), liveobj_name(state.device.device) or '-', state.device.bank_name or '-')

def format_notification(state, notification_text):
    if notification_text == 'default_lines':
        lines = get_default_lines(state)
    elif 'ERROR' in notification_text or 'INFO' in notification_text:
        lines = [Text(t, max_width=Text.ContentWidth()) for t in notification_text.split('\n')]
    else:
        text = notification_text.split('\n')
        lines = ('', Text(text[0], max_width=Text.ContentWidth()), text[1].title())
    return Content(header_color=make_color_for_liveobj(state.target_track.target_track), lines=tuple(lines))

def create_root_view() -> view.View[Optional[Content]]:

    @view.View
    def main_view(state) -> Optional[Content]:
        active_parameter = get_active_parameter(state)
        return Content(make_color_for_liveobj(state.target_track.target_track), (getattr(parameter_owner(active_parameter), 'name', ''), Text(display_name(active_parameter), max_width=display_name(active_parameter) in ['Fixed Length', 'Quantization']), str(active_parameter)) if state.encoder_modes.selected_mode == 'tempo' else ('', 'Tempo', '{} BPM'.format(floor(song().tempo))), get_default_lines(state) if state.pad_modes.selected_mode in CONTROL_SURFACE_DISPLAY_PAD_MODES else None)
    return view.CompoundView(view.DisconnectedView(render_condition=lambda state: not state.identification.is_identified or not state.connected or state.encoder_modes.selected_mode == 'swing'), view.NotificationView(format_notification, suppressing_signals=(lambda state, _: get_active_parameter(state) is not None or state.elements.tempo_button.is_pressed,), render_condition=lambda state, notification: notification != 'default_lines' or state.pad_modes.selected_mode not in CONTROL_SURFACE_DISPLAY_PAD_MODES, supports_new_line=True), main_view)

def protocol(elements):

    def display(content: Content):
        if content:
            elements.track_color_element.set_light(content.header_color)
        if content and content.lines:
            elements.display_ownership_command.send_value(1)
            elements.display_line_1.display_message(content.lines[0])
            elements.display_line_2.display_message(content.lines[1])
            elements.display_line_3.display_message(content.lines[2])
            return
        else:
            elements.display_ownership_command.send_value(0)
    return display
display_specification = DisplaySpecification(create_root_view=create_root_view, protocol=protocol, notifications=Notifications)