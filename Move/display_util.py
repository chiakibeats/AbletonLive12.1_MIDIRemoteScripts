# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\display_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import List, NamedTuple, Optional
from _MoveDisplay import HorizontalAlignment, MoveDisplay, VerticalAlignment
from ableton.v3.base import nop
from ableton.v3.control_surface.elements import DisplayLineElement
from .midi import make_wake_up_display_message
MAX_LINES = 3
ELLIPSIS_CHAR = 'c'
AUTOMATION_CHAR = '\ue044'

def on_off_to_title_case(text):
    pass
    return text.replace('\non', '\nOn').replace('\noff', '\nOff')

def parameter_value_string(parameter):
    pass
    value_string = str(parameter)
    if ' dB' in value_string:
        return '{} dB'.format(round(float(value_string.replace(' dB', '')), 1))
    else:
        return value_string

def break_line(line, line_width=128, string_width_fn=len):
    pass
    if '\n' in line:
        lines = line.split('\n')
        if len(lines) > MAX_LINES:
            return lines[:MAX_LINES - 1] + [''.join(lines[MAX_LINES - 1:])]
        else:
            return lines
    else:
        space_width = string_width_fn(' ')
        words = line.split()
        lines = ['']
        current_width = 0
        for word in words:
            width = string_width_fn(word)
            with_space = '{} '.format(word)
            if len(lines) == MAX_LINES or current_width + width <= line_width or (current_width == 0 and width >= line_width):
                current_width += width + space_width
                lines[-1] += with_space
                continue
            else:
                current_width = width + space_width
                lines.append(with_space)
                continue
        return [line.strip() for line in lines]

def get_mode_select_notification(mode):
    pass
    if mode == 'session_overview':
        return 'Session Overview'
    elif mode == 'launch':
        return 'Session Mode'
    elif mode in ['session', 'note']:
        return '{} Mode'.format(mode.title())
    else:
        return None

class LoopOverviewData(NamedTuple):
    pass
    overview_start_position: float
    overview_end_position: float
    current_position: float
    loop_start_position: float
    loop_end_position: float
    playing_position: float
    length_of_one_bar_in_beats: float

@dataclass
class Content:
    pass
    lines: List[str]
    value: Optional[float] = None
    fill_value: Optional[bool] = True
    left_meter: Optional[float] = None
    right_meter: Optional[float] = None
    loop_overview_data: Optional[LoopOverviewData] = None
    horizontal_alignment: Optional[Enum] = HorizontalAlignment.CENTER

    @classmethod
    def with_loop_overview(cls, state, **k):
        pass
        if state.main_modes.selected_mode == 'note' and state.menu_modes.menu_content is None:
            return cls(loop_overview_data=state.loop_selector.loop_overview_data, **k)
        else:
            return cls(**k)

@dataclass
class VerticalListContent(Content):
    pass
    list_index: Optional[int] = 0
    list_cursor_char: Optional[str] = ''

@dataclass
class HorizontalListContent(Content):
    pass
    draw_border: Optional[bool] = True

@dataclass
class NotificationContent(Content):
    pass

class DisplayElement(DisplayLineElement):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, display_fn=nop, **k)
        self._move_display = MoveDisplay()
        self._break_line = partial(break_line, line_width=self._move_display.get_width(), string_width_fn=self._move_display.get_string_width)

    def disconnect(self):
        super().disconnect()
        self._break_line = None
        self._move_display.disconnect()
        self._move_display = None

    def initialize(self):
        pass
        self._move_display.connect()
        self._send_midi(make_wake_up_display_message())

    def soft_disconnect(self):
        pass
        self._move_display.disconnect()

    def _do_display(self, message):
        content = Content(lines=[message]) if isinstance(message, str) else message
        if self._move_display:
            self._move_display.begin_draw()
            if content.lines:
                if isinstance(content, VerticalListContent):
                    self._move_display.draw_vertical_list(content.lines, content.list_cursor_char, content.list_index)
                elif isinstance(content, HorizontalListContent):
                    self._move_display.draw_horizontal_list(content.lines, content.draw_border)
                else:
                    self._draw_lines(content)
            self._draw_value(content)
            self._draw_meter(content)
            self._draw_loop_overview(content)
            self._move_display.end_draw()
            if isinstance(content, NotificationContent):
                self._send_midi(make_wake_up_display_message())
                return

    def _draw_lines(self, content):
        lines = content.lines
        self._move_display.draw_lines(self._break_line(lines[0]) if len(lines) == 1 else lines, content.horizontal_alignment, 0, VerticalAlignment.CENTER, 0)

    def _draw_value(self, content):
        if content.value is not None:
            self._move_display.draw_value(content.value, content.fill_value)

    def _draw_meter(self, content):
        if content.left_meter is not None and content.right_meter is not None:
            self._move_display.draw_meter(content.left_meter, content.right_meter)

    def _draw_loop_overview(self, content):
        if not content.loop_overview_data or len(content.lines) < MAX_LINES:
            self._move_display.draw_loop_overview(*content.loop_overview_data)