# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\SlideComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ScrollComponent import Scrollable, ScrollComponent
from _Framework.SubjectSlot import Subject, subject_slot
from _Framework.Util import clamp

class Slideable(Subject):
    pass
    __subject_events__ = ('page_offset', 'page_length', 'position', 'position_count', 'contents')

    def contents_range(self, pmin, pmax):
        pass
        pos_count = self.position_count
        first_pos = max(int(pmin), 0)
        last_pos = min(int(pmax), pos_count)
        return list(range(first_pos, last_pos))

    def contents(self, position):
        return False

    @property
    def position_count(self):
        raise NotImplementedError

    @property
    def position(self):
        raise NotImplementedError

    @property
    def page_offset(self):
        raise NotImplementedError

    @property
    def page_length(self):
        raise NotImplementedError

class SlideComponent(CompoundComponent, Scrollable):

    def __init__(self, slideable=None, *a, **k):
        super(SlideComponent, self).__init__(*a, **k)
        slideable = slideable or self
        self._slideable = slideable
        self._position_scroll, self._page_scroll = self.register_components(ScrollComponent(), ScrollComponent())
        self._position_scroll.scrollable = self
        self._page_scroll.can_scroll_up = self.can_scroll_page_up
        self._page_scroll.can_scroll_down = self.can_scroll_page_down
        self._page_scroll.scroll_down = self.scroll_page_down
        self._page_scroll.scroll_up = self.scroll_page_up
        self._on_position_changed.subject = slideable

    def set_scroll_up_button(self, button):
        self._position_scroll.set_scroll_up_button(button)

    def set_scroll_down_button(self, button):
        self._position_scroll.set_scroll_down_button(button)

    def set_scroll_page_up_button(self, button):
        self._page_scroll.set_scroll_up_button(button)

    def set_scroll_page_down_button(self, button):
        self._page_scroll.set_scroll_down_button(button)

    def scroll_page_up(self):
        self._scroll_page(1)

    def scroll_page_down(self):
        self._scroll_page(-1)

    def scroll_up(self):
        self._scroll_position(1)

    def scroll_down(self):
        self._scroll_position(-1)

    def can_scroll_page_up(self):
        model = self._slideable
        return model.position < model.position_count - model.page_length

    def can_scroll_page_down(self):
        return self._slideable.position > 0

    def can_scroll_up(self):
        return self.can_scroll_page_up()

    def can_scroll_down(self):
        return self.can_scroll_page_down()

    def _scroll_position(self, delta):
        if self.is_enabled():
            model = self._slideable
            model.position = clamp(model.position + delta, 0, model.position_count - model.page_length)

    def _scroll_page(self, sign):
        if self.is_enabled():
            model = self._slideable
            remainder = (model.position - model.page_offset) % model.page_length
            if sign > 0:
                delta = model.page_length - remainder
            elif remainder == 0:
                delta = -model.page_length
            else:
                delta = -remainder
            self._scroll_position(delta)

    def update(self):
        self._position_scroll.update()
        self._page_scroll.update()

    @subject_slot('position')
    def _on_position_changed(self):
        self._position_scroll.update()
        self._page_scroll.update()