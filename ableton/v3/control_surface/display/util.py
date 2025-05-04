# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import List
from ...base import BooleanContext
updating_display = BooleanContext()
pass
pass

def auto_break_lines(text: str, max_width: int, max_lines: int, pad_lines: bool=True) -> List[str]:
    pass
    words = [truncate_with_ellipses(word[:max_width]) if len(word) > max_width else word for word in text.split(' ')]
    lines = ['']
    current_width = 0
    for word in words:
        if current_width + len(word) <= max_width:
            str_to_append = ' {}'.format(word) if current_width != 0 else word
            current_width += len(str_to_append)
            lines[-1] += str_to_append
            continue
        else:
            lines.append(word)
            current_width = len(word)
            continue
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = truncate_with_ellipses(lines[-1])
    if pad_lines and len(lines) < max_lines:
        lines += [''] * (max_lines - len(lines))
    return lines

def truncate_with_ellipses(string: str):
    pass
    return string[:len(string) - 3] + '...' if len(string) > 3 else '.' * len(string)