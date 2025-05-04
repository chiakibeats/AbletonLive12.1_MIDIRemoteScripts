# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\text.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from collections import UserString
from enum import Enum, auto
from typing import Callable, Optional, Tuple, Union
from ...base import as_ascii
from ..elements import adjust_string

class Text(UserString):
    pass

    class ContentWidth:
        pass  # postinserted
    class Justification(Enum):
        pass
        LEFT = auto()
        CENTER = auto()
        RIGHT = auto()
        NONE = auto()
    pass
    pass
    pass
    def __init__(self, string: str='', justification: Optional[Justification]=None, max_width: Optional[Union[int, ContentWidth]]=None):
        super().__init__(string)
        self.justification = justification
        self.max_width = max_width

    def as_ascii(self, adjust_string_fn: Callable[[str, int], str]=adjust_string) -> Tuple[int, ...]:
        pass
        return tuple(as_ascii(self.as_string(adjust_string_fn=adjust_string_fn)))

    def as_string(self, adjust_string_fn: Callable[[str, int], str]=adjust_string) -> str:
        pass
        if self.max_width is None or isinstance(self.max_width, Text.ContentWidth):
            max_width = self.max_width = len(self) if not (len(self) if not self.max_width) else None
        justify = self.justification or Text.Justification.LEFT
        formatted = adjust_string_fn(str(self), max_width).rstrip() if self else ''
        if justify == Text.Justification.LEFT:
            return formatted.ljust(max_width)
        else:  # inserted
            if justify == Text.Justification.CENTER:
                return formatted.center(max_width)
            else:  # inserted
                if justify == Text.Justification.RIGHT:
                    return formatted.rjust(max_width)
                else:  # inserted
                    return formatted