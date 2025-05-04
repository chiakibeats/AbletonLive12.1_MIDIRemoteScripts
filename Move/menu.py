# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\menu.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from dataclasses import dataclass
from typing import Callable, List, Optional
from ableton.v3.base import PITCH_NAMES, depends, nop
from .clip_actions import QUANTIZATION_MAP
from .display_util import MAX_LINES, Content, HorizontalListContent, VerticalListContent
from .firmware import LedBrightness
from .melodic_pattern import SCALES
from .step_sequence import DEFAULT_GRID_RESOLUTION_INDEX

def list_content(menu, list_index):
    pass
    start = menu.index
    start = max(0, start - 1 if start < len(menu.items) - 1 else start - 2)
    items = menu.items[start:max(start + MAX_LINES, start + 2)]
    return VerticalListContent(lines=[str(item.name_transform() or item.name) for item in items], list_index=list_index, list_cursor_char=menu.items[menu.index].cursor_char if menu.items else '')

def simple_content(menu_item, _):
    pass
    return HorizontalListContent(lines=[menu_item.name, menu_item.items[menu_item.index].name])

@depends(firmware=None)
def create_settings_menu(component, firmware=None):
    pass
    menu = Menu(items=[MenuItem(name_transform=lambda: 'Battery {}%'.format(firmware.battery_level), items=[MenuItem()], content_fn=lambda *_: Content(lines=['{}\nBattery {}%'.format(firmware.charging_state, firmware.battery_level)])), MenuItem(name='Standalone', click_action=firmware.switch_to_standalone), MenuItem(name='Brightness', name_transform=lambda: 'Brightness {}'.format(firmware.led_brightness.name.title()), items=[MenuItem(name=led.name.title()) for led in LedBrightness], property_setter=firmware.set_led_brightness_index, content_fn=simple_content)])

    def update(_):
        menu.items[2].index = list(LedBrightness).index(firmware.led_brightness)
        component.update_menu(menu)
    for event in ['battery_level', 'charging_state', 'led_brightness']:
        component.register_slot(firmware, update, event)
    return menu

@depends(song=None, note_layout=None)
def create_scale_menu(component, song=None, note_layout=None):
    pass
    menu = Menu(items=[MenuItem(name_transform=lambda: 'In-Key' if note_layout.is_in_key else 'Chromatic', click_action=note_layout.toggle_is_in_key), MenuItem(name_transform=lambda p: PITCH_NAMES[song.root_note], items=lambda x: setattr(note_layout, 'root_note', x)), MenuItem(name_transform=lambda s: song.scale_name, items=lambda x: setattr(note_layout, 'scale', SCALES[x]))])

    def update(_):
        menu.items[1].index = note_layout.root_note
        menu.items[2].index = SCALES.index(note_layout.scale)
        component.update_menu(menu)
    component.register_slot(note_layout, update, 'root_note')
    component.register_slot(note_layout, update, 'scale')
    return menu

@depends(song=None, quantization_strength=None, grid_resolution=None)
pass
def create_workflow_menu(component, song=None, quantization_strength=None, grid_resolution=None):
    pass
    menu = Menu(items=[MenuItem(name='Quantize', name_transform=lambda x: 'Quantize {}%'.format(int(quantization_strength.value * 100)), items=[MenuItem(name='{}%'.format(i * 10)) for i in range(1, 11)], items=[MenuItem(name=s[1]) for s in QUANTIZATION_MAP.values()], content_fn=simple_content, index=DEFAULT_GRID_RESOLUTION_INDEX)])
    component.register_slot(song, lambda: component.update_menu(menu), 'session_automation_record')
    return menu

@dataclass
class Menu:
    pass
    items: List = None
    index: int = 0
    content_fn: Callable = list_content

@dataclass
class MenuItem(Menu):
    pass
    name: Optional[str] = None
    name_transform: Optional[Callable] = nop
    cursor_char: Optional[str] = '-'
    click_action: Optional[Callable] = None
    property_setter: Optional[Callable] = None

    def __post_init__(self):
        if self.items:
            self.cursor_char = '>'