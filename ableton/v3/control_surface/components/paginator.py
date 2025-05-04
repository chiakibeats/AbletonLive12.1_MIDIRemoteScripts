# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\paginator.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import EventObject, depends, forward_property, listens
from .. import Component

class Paginator(EventObject):
    pass
    __events__ = ('page', 'page_time', 'page_length')
    can_change_page = lambda: False
    page_length = NotImplemented
    page_time = NotImplemented

class NoteEditorPaginator(Component, Paginator):
    pass
    can_change_page = forward_property('_note_editor')('can_change_page')
    page_length = forward_property('_note_editor')('page_length')

    @depends(note_editor=None)
    def __init__(self, note_editor=None, *a, **k):
        super().__init__(*a, **k)
        self._note_editor = note_editor
        self._last_page_time = 0.0
        self.__on_page_length_changed.subject = note_editor
        self.__on_active_steps_changed.subject = note_editor

    @property
    def page_time(self):
        return self._note_editor.page_time

    @page_time.setter
    def page_time(self, time):
        can_change_page = self.can_change_page
        if not can_change_page or time != self._last_page_time:
            self._note_editor.page_time = time
            self._last_page_time = time
            self.notify_page()
            self.notify_page_time()

    def update(self):
        super().update()
        if self.is_enabled():
            self.notify_page_time()
            self.notify_page()
            self.notify_page_length()

    @listens('active_steps')
    def __on_active_steps_changed(self):
        if self.is_enabled():
            self.notify_page()

    @listens('page_length')
    def __on_page_length_changed(self):
        if self.is_enabled():
            self.notify_page()
            self.notify_page_length()