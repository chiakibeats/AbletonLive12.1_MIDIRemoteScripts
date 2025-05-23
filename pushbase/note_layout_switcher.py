# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\note_layout_switcher.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import nop
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl
from .message_box_component import Messenger

class ContextualButtonControl(ButtonControl):

    class State(ButtonControl.State):

        def on_context_changed(self):
            if self.is_pressed:
                self._release_button()

class ModeSwitcherBase(Component, Messenger):
    cycle_button = ContextualButtonControl()
    lock_button = ButtonControl()
    locked_mode = None

    def __init__(self, *a, **k):
        super(ModeSwitcherBase, self).__init__(*a, **k)
        self._cycle_mode = nop
        self._on_unlocked_release = nop
        self._get_current_alternative_mode = nop

    def release_alternative_layout(self):
        self.cycle_button.on_context_changed()

    def _should_unlock(self):
        return bool(self.locked_mode)

    @cycle_button.released_immediately
    def cycle_button(self, button):
        if self._should_unlock():
            self._unlock_alternative_mode(self.locked_mode)
        else:
            self._on_unlocked_release()

    @cycle_button.pressed_delayed
    def cycle_button(self, button):
        self._cycle_mode()

    @cycle_button.released_delayed
    def cycle_button(self, button):
        self._cycle_mode()

    @lock_button.pressed
    def lock_button(self, button):
        if not self._should_unlock():
            self._lock_alternative_mode(self._get_current_alternative_mode())

    def _lock_alternative_mode(self, mode):
        if mode:
            mode.cycle_mode()
            self.cycle_button.color = 'DefaultButton.Alert'
            self.locked_mode = mode
            if mode.get_mode_message():
                self.show_notification(mode.get_mode_message() + ': Locked')
                return
        else:
            return

    def _unlock_alternative_mode(self, locked_mode):
        if locked_mode:
            if locked_mode.get_mode_message():
                self.show_notification(locked_mode.get_mode_message() + ': Unlocked')
            locked_mode.cycle_mode(-1)
            self.cycle_button.color = 'DefaultButton.On'

    def on_enabled_changed(self):
        super(ModeSwitcherBase, self).on_enabled_changed()
        if self.is_enabled() or self.cycle_button.is_pressed:
            self._cycle_mode()

class NoteLayoutSwitcher(ModeSwitcherBase):
    pass
    pass

    def __init__(self, switch_note_mode_layout=None, get_current_alternative_layout_mode=None, *a, **k):
        super(NoteLayoutSwitcher, self).__init__(*a, **k)
        self._get_current_alternative_mode = get_current_alternative_layout_mode
        self._cycle_mode = self._cycle_alternative_note_layout
        self._on_unlocked_release = switch_note_mode_layout

    def _should_unlock(self):
        return bool(self.song.view.selected_track.get_data('alternative_mode_locked', False))

    def _lock_alternative_mode(self, mode):
        super(NoteLayoutSwitcher, self)._lock_alternative_mode(mode)
        if mode:
            self.song.view.selected_track.set_data('alternative_mode_locked', True)

    def _unlock_alternative_mode(self, _mode):
        super(NoteLayoutSwitcher, self)._unlock_alternative_mode(self._get_current_alternative_mode())
        self.song.view.selected_track.set_data('alternative_mode_locked', False)

    def _cycle_alternative_note_layout(self):
        cyclable_mode = self._get_current_alternative_mode()
        if cyclable_mode:
            cyclable_mode.cycle_mode()