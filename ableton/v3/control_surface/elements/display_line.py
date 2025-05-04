# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\display_line.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import Any, Callable, Generic, TypeVar, Union
from .. import NotifyingControlElement
from ..display import Text, updating_display
DisplayDataType = TypeVar('DisplayDataType')

class DisplayLineElement(NotifyingControlElement, Generic[DisplayDataType]):
    pass

    def __init__(self, display_fn: Callable[[DisplayDataType], Any], formatting_fn: Callable[[Text], DisplayDataType]=lambda message: message.as_ascii(), default_formatting=Text(), *a, **k):
        super().__init__(*a, **k)
        self._display_fn = display_fn
        self._formatting_fn = formatting_fn
        self._default_formatting = default_formatting
        self._last_native_content = None

    def display_message(self, text):
        pass
        if updating_display:
            if self._last_native_content != text:
                self._last_native_content = text
                if not self.grabbed:
                    self._do_display(text)
                else:
                    return None
        else:
            self._do_display(text)

    def _apply_default_formatting(self, text: Text):
        if text.max_width is None:
            text.max_width = self._default_formatting.max_width
        if text.justification is None:
            text.justification = self._default_formatting.justification

    def _do_display(self, message: Union[Text, str]):
        text = message if isinstance(message, Text) else Text(message)
        self._apply_default_formatting(text)
        self._display_fn(self._formatting_fn(text))

    @property
    def grabbed(self):
        return self.resource.stack_size > 1

    def clear_send_cache(self):
        self._last_native_content = None

    def reset(self):
        if self.grabbed:
            self._do_display('')
            self._redisplay_last_native_content()

    def _redisplay_last_native_content(self):
        if self._last_native_content is not None:
            self._do_display(self._last_native_content)
            return
        else:
            return None