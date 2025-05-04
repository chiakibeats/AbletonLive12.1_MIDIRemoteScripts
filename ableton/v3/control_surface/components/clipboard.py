# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\clipboard.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import is_iterable, listenable_property
from .. import Component
from ..controls import ButtonControl
from ..display import Renderable

class ClipboardComponent(Component, Renderable):
    pass
    copy_button = ButtonControl(color='Clipboard.Empty', on_color='Clipboard.Filled', pressed_color='Clipboard.CopyPressed')
    has_content = listenable_property.managed(False)
    is_copying = listenable_property.managed(False)

    def __init__(self, name='Clipboard', *a, **k):
        super().__init__(*a, name=name, **k)
        self._source_obj = None
        self._did_paste = False
        self._pending_clear = False
        self.register_clipboard()

    def set_copy_button(self, button):
        self.clear()
        self.copy_button.set_control_element(button)

    def copy_or_paste(self, obj):
        pass
        if self.has_content:
            self.paste(obj)
            return
        else:
            self.copy(obj)

    def copy(self, obj):
        pass
        if not self.any_clipboard_has_content:
            self._source_obj = self._do_copy(obj)
            self.update()
            return

    def paste(self, obj):
        pass
        if self._is_source_valid():
            self._did_paste = self._do_paste(obj)
            if self._did_paste:
                self.clear()
        else:
            self.clear(notify=True)

    def clear(self, notify=False):
        pass
        self._source_obj = None
        self._pending_clear = False
        self.update()
        if notify:
            self.notify(self.notifications.Clipboard.clear)

    @copy_button.pressed
    def copy_button(self, _):
        self._pending_clear = self.has_content
        self.is_copying = True

    @copy_button.released
    def copy_button(self, _):
        if self._did_paste or self._pending_clear:
            self.clear(notify=True)
            return
        else:
            self.is_copying = self.has_content

    def update(self):
        super().update()
        self._did_paste = False
        self.has_content = self._is_source_valid()
        self.is_copying = self.has_content or self.copy_button.is_pressed
        self.copy_button.is_on = self.has_content

    def _do_copy(self, obj):
        pass
        self._source_obj = obj
        return self._source_obj

    def _do_paste(self, obj):
        pass
        self._did_paste = obj is not None
        return self._did_paste

    def _is_source_valid(self):
        pass
        return self._source_obj is not None

class BufferedClipboardComponent(ClipboardComponent):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._buffer = []

    @property
    def buffer(self):
        pass
        return self._buffer

    def clear(self, notify=False):
        self._buffer = []
        super().clear(notify=notify)

    def append_buffer(self, obj):
        pass
        self._buffer.append(obj)

    def extend_buffer(self, obj):
        pass
        self._buffer.extend(obj)

    def _is_source_valid(self):
        pass
        return bool(self._buffer)