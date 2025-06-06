# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\page.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import EventObject, clamp
from .. import Component
from .scroll import Scrollable, ScrollComponent

class Pageable(EventObject):
    pass
    __events__ = ('position',)
    position_count = NotImplemented
    position = NotImplemented
    page_offset = NotImplemented
    page_length = NotImplemented

class PageComponent(Component, Scrollable):
    pass

    def __init__(self, pageable=None, scroll_skin_name=None, *a, **k):
        super().__init__(*a, **k)
        self._pageable = pageable or self
        self._position_scroll = ScrollComponent(self, parent=self, scroll_skin_name=scroll_skin_name)
        self._page_scroll = ScrollComponent(parent=self, scroll_skin_name=scroll_skin_name)
        self._page_scroll.can_scroll_up = self.can_scroll_page_up
        self._page_scroll.can_scroll_down = self.can_scroll_page_down
        self._page_scroll.scroll_down = self.scroll_page_down
        self._page_scroll.scroll_up = self.scroll_page_up
        self.register_slot(self._pageable, self.update, 'position')

    def set_scroll_up_button(self, button):
        self._position_scroll.set_scroll_up_button(button)

    def set_scroll_down_button(self, button):
        self._position_scroll.set_scroll_down_button(button)

    def set_scroll_encoder(self, encoder):
        self._position_scroll.set_scroll_encoder(encoder)

    def set_scroll_page_up_button(self, button):
        self._page_scroll.set_scroll_up_button(button)

    def set_scroll_page_down_button(self, button):
        self._page_scroll.set_scroll_down_button(button)

    def set_scroll_page_encoder(self, encoder):
        self._page_scroll.set_scroll_encoder(encoder)

    def scroll_page_up(self):
        self._scroll_page(1)

    def scroll_page_down(self):
        self._scroll_page(-1)

    def scroll_up(self):
        self._scroll_position(1)

    def scroll_down(self):
        self._scroll_position(-1)

    def can_scroll_page_up(self):
        model = self._pageable
        return model.position < model.position_count - model.page_length

    def can_scroll_page_down(self):
        return self._pageable.position > 0

    def can_scroll_up(self):
        return self.can_scroll_page_up()

    def can_scroll_down(self):
        return self.can_scroll_page_down()

    def _scroll_position(self, delta):
        if self.is_enabled():
            model = self._pageable
            model.position = clamp(model.position + delta, 0, model.position_count - model.page_length)

    def _scroll_page(self, sign):
        if self.is_enabled():
            model = self._pageable
            remainder = (model.position - model.page_offset) % model.page_length
            if sign > 0:
                delta = model.page_length - remainder
            elif remainder == 0:
                delta = -model.page_length
            else:
                delta = -remainder
            self._scroll_position(delta)

    def update(self):
        super().update()
        self._position_scroll.update()
        self._page_scroll.update()