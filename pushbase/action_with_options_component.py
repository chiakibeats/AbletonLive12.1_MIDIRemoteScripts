# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\action_with_options_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import zip_longest
from ableton.v2.base import clamp, in_range, task
from ableton.v2.control_surface import Component, defaults
from ableton.v2.control_surface.control import ButtonControl, control_list
from ableton.v2.control_surface.elements import DisplayDataSource
from . import consts

class ActionWithSettingsComponent(Component):
    action_button = ButtonControl(**consts.SIDE_BUTTON_COLORS)
    SETTINGS_DELAY = defaults.MOMENTARY_DELAY

    def __init__(self, *a, **k):
        super(ActionWithSettingsComponent, self).__init__(*a, **k)
        self._is_showing_settings = False
        self._settings_task = task.Task()

    def show_settings(self):
        pass
        return True

    def hide_settings(self):
        pass
        return

    def trigger_action(self):
        pass
        return

    def post_trigger_action(self):
        pass
        return

    def _do_show_settings(self):
        self._is_showing_settings = self.show_settings()

    def _do_hide_settings(self):
        self.hide_settings()
        self._is_showing_settings = False

    @action_button.pressed
    def action_button(self, button):
        self._settings_task.kill()
        self._settings_task = self._tasks.add(task.sequence(task.wait(self.SETTINGS_DELAY), task.run(self._do_show_settings)))
        self.trigger_action()

    @action_button.released
    def action_button(self, button):
        self._settings_task.kill()
        if self._is_showing_settings:
            self.hide_settings()
            self._is_showing_settings = False
            return
        else:
            self.post_trigger_action()

class OptionsComponent(Component):
    __events__ = ('selected_option',)
    unselected_color = 'Option.Unselected'
    selected_color = 'Option.Selected'
    _selected_option = None
    select_buttons = control_list(ButtonControl, control_count=0)

    def __init__(self, num_options=8, num_labels=4, num_display_segments=None, *a, **k):
        super(OptionsComponent, self).__init__(*a, **k)
        num_display_segments = num_display_segments or num_options
        self._label_data_sources = [DisplayDataSource() for _ in range(num_labels)]
        self._data_sources = [DisplayDataSource() for _ in range(num_display_segments)]
        self._option_names = []

    def _get_option_names(self):
        return self._option_names

    def _set_option_names(self, value):
        self._option_names = value
        self.select_buttons.control_count = len(value)
        if self._selected_option:
            currently_selected_option = self.selected_option
            self.selected_option = clamp(self._selected_option, 0, len(self._option_names) - 1)
            if currently_selected_option != self.selected_option:
                self.notify_selected_option(self.selected_option)
        self._update_select_buttons()
        self._update_data_sources()
    option_names = property(_get_option_names, _set_option_names)

    def _get_selected_option(self):
        return self._selected_option

    def _set_selected_option(self, selected_option):
        self._selected_option = selected_option
        self._update_select_buttons()
        self._update_data_sources()
    selected_option = property(_get_selected_option, _set_selected_option)

    def set_display_line(self, line):
        if line:
            self._update_data_sources()
            line.set_num_segments(len(self._data_sources))
            for segment in range(len(self._data_sources)):
                line.segment(segment).set_data_source(self._data_sources[segment])

    def set_label_display_line(self, line):
        if line:
            line.set_num_segments(len(self._label_data_sources))
            for segment in range(len(self._label_data_sources)):
                line.segment(segment).set_data_source(self._label_data_sources[segment])

    def _get_labels(self):
        return [segment.display_string() for segment in self._label_data_sources]

    def _set_labels(self, labels):
        for segment, label in zip_longest(self._label_data_sources, labels or []):
            segment.set_display_string(label)
    labels = property(_get_labels, _set_labels)

    def set_blank_display_line1(self, line):
        if line:
            line.reset()
        else:
            return None

    def set_blank_display_line2(self, line):
        if line:
            line.reset()
        else:
            return None

    def set_state_buttons(self, buttons):
        if buttons:
            buttons.reset()

    @select_buttons.pressed
    def _on_select_value(self, button):
        index = list(self.select_buttons).index(button)
        if in_range(index, 0, len(self.option_names)):
            self.selected_option = index
            self.notify_selected_option(self.selected_option)

    def _update_select_buttons(self):
        for index, button in enumerate(self.select_buttons):
            button.color = self.selected_color if index == self._selected_option else self.unselected_color
            continue

    def _update_data_sources(self):
        for index, (source, name) in enumerate(zip_longest(self._data_sources, self.option_names)):
            if name:
                source.set_display_string((consts.CHAR_SELECT if index == self._selected_option else ' ') + name)
                continue
            else:
                source.set_display_string('')
                continue

class ActionWithOptionsComponent(ActionWithSettingsComponent):

    def __init__(self, num_options=8, *a, **k):
        super(ActionWithOptionsComponent, self).__init__(*a, **k)
        self._options = OptionsComponent(parent=self, num_options=num_options)
        self._options.set_enabled(False)

    @property
    def options(self):
        return self._options

    def show_settings(self):
        self._options.set_enabled(True)
        return True

    def hide_settings(self):
        self._options.set_enabled(False)

class ToggleWithOptionsComponent(ActionWithOptionsComponent):
    __events__ = ('toggle_option', 'is_active')
    _is_active = False
    _just_activated = False

    def __init__(self, *a, **k):
        super(ToggleWithOptionsComponent, self).__init__(*a, **k)
        self.action_button.color = 'DefaultButton.Off'

    def _get_is_active(self):
        return self._is_active

    def _set_is_active(self, value):
        if value != self._is_active:
            self._is_active = value
            self.notify_is_active(value)
            self.action_button.color = 'DefaultButton.On' if value else 'DefaultButton.Off'
    is_active = property(_get_is_active, _set_is_active)

    def trigger_action(self):
        if self._is_active:
            self._just_activated = False
            return
        else:
            self.is_active = True
            self._just_activated = True
            self.notify_toggle_option(True)

    def post_trigger_action(self):
        if not self._just_activated:
            self.is_active = False
            self.notify_toggle_option(False)
            return
        else:
            return None