# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\message_box_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import re
from itertools import zip_longest
from ableton.v2.base import const, forward_property, listenable_property, listens, nop
from ableton.v2.base.dependency import dependency
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import BackgroundComponent
from ableton.v2.control_surface.elements import DisplayDataSource
from .consts import DISPLAY_LENGTH, MessageBoxText
FORMAT_SPECIFIER_WITH_MARKUP_PATTERN = re.compile('[%](len=([0-9]+),)?([^%]*?[diouxXeEfFgGcrs])')

def strip_restriction_markup_and_format(text_or_text_spec):
    if isinstance(text_or_text_spec, tuple):
        format_string = text_or_text_spec[0]
        stripped_format_string = re.sub(FORMAT_SPECIFIER_WITH_MARKUP_PATTERN, '%\\g<3>', format_string)
        arguments = text_or_text_spec[1:]
        return stripped_format_string % arguments
    else:  # inserted
        return text_or_text_spec

class Notification(object):
    def __init__(self, parent, *a, **k):
        super(Notification, self).__init__(*a, **k)
        self.hide = parent.hide_notification

class Messenger(object):
    pass
    expect_dialog = dependency(expect_dialog=const(nop))
    show_notification = dependency(show_notification=const(nop))

class MessageBoxComponent(BackgroundComponent):
    pass
    __events__ = ('cancel',)
    num_lines = 4

    def __init__(self, *a, **k):
        super(MessageBoxComponent, self).__init__(*a, **k)
        self._current_text = None
        self._can_cancel = False
        self.data_sources = list(map(DisplayDataSource, ('',) * self.num_lines))
        self._notification_display = None

    def _set_display_line(self, n, display_line):
        if display_line:
            display_line.set_data_sources((self.data_sources[n],))

    def set_display_line1(self, display_line):
        self._set_display_line(0, display_line)

    def set_display_line2(self, display_line):
        self._set_display_line(1, display_line)

    def set_display_line3(self, display_line):
        self._set_display_line(2, display_line)

    def set_display_line4(self, display_line):
        self._set_display_line(3, display_line)

    def set_cancel_button(self, button):
        self._on_cancel_button_value.subject = button
        self._update_cancel_button()

    def _update_cancel_button(self):
        if self.is_enabled():
            button = self._on_cancel_button_value.subject
            if button is not None:
                button.reset()
            if not self._can_cancel or button:
                    button.set_light('MessageBox.Cancel')
                    return
                else:  # inserted
                    return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _update_display(self):
        if self._current_text!= None:
            lines = self._current_text.split('\n')
            for source_line, line in zip_longest(self.data_sources, lines):
                if source_line:
                    source_line.set_display_string(line or '')
                continue
            if self._can_cancel:
                self.data_sources[(-1)].set_display_string('[  Ok  ]'.rjust(DISPLAY_LENGTH - 1))

    @listens('value')
    def _on_cancel_button_value(self, value):
        if self.is_enabled() and self._can_cancel and value:
                    self.notify_cancel()
        else:  # inserted
            return

    @listenable_property
    def text(self):
        return self._current_text

    @text.setter
    def text(self, text):
        if self._current_text!= text:
            self._current_text = text
            self._update_display()
            self.notify_text()

    @listenable_property
    def can_cancel(self):
        return self._can_cancel

    @can_cancel.setter
    def can_cancel(self, can_cancel):
        if self._can_cancel!= can_cancel:
            self._can_cancel = can_cancel
            self._update_cancel_button()
            self._update_display()
            self.notify_can_cancel()

    def update(self):
        super(MessageBoxComponent, self).update()
        self._update_cancel_button()
        self._update_display()

class DialogComponent(Component):
    pass

    def __init__(self, *a, **k):
        super(DialogComponent, self).__init__(*a, **k)
        self._message_box = MessageBoxComponent(parent=self, is_enabled=False)
        self._next_message = None
        self._on_open_dialog_count.subject = self.application
        self._on_message_cancel.subject = self._message_box
    message_box_layer = forward_property('_message_box')('layer')

    def expect_dialog(self, message):
        pass
        self._next_message = message
        self._update_dialog()

    @listens('open_dialog_count')
    def _on_open_dialog_count(self):
        self._update_dialog(open_dialog_changed=True)
        self._next_message = None

    @listens('cancel')
    def _on_message_cancel(self):
        self._next_message = None
        try:
            self.application.press_current_dialog_button(0)
        except RuntimeError:
            pass
        self._update_dialog()

    def _update_dialog(self, open_dialog_changed=False):
        message = self._next_message or MessageBoxText.LIVE_DIALOG
        can_cancel = self._next_message!= None
        self._message_box.text = message
        self._message_box.can_cancel = can_cancel
        self._message_box.set_enabled(self.application.open_dialog_count > 0 or (not open_dialog_changed and self._next_message))

class InfoComponent(BackgroundComponent):
    pass

    def __init__(self, info_text='', *a, **k):
        super(InfoComponent, self).__init__(*a, **k)
        self._data_source = DisplayDataSource()
        self._data_source.set_display_string(info_text)

    def set_display(self, display):
        if display:
            display.set_data_sources([self._data_source])
            return
        else:  # inserted
            return None