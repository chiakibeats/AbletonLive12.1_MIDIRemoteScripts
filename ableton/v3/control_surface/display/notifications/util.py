# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\notifications\util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from __future__ import annotations
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from typing_extensions import LiteralString
else:
    LiteralString = str

def toggle_text_generator(format_string: LiteralString) -> Callable[[bool], str]:
    pass

    def notification_fn(is_on: bool):
        return format_string.format('on' if is_on else 'off')
    return notification_fn