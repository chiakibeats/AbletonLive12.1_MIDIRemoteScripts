# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\mode\modes.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from typing import cast
from ableton.v2.control_surface import StackingResource
from ableton.v2.control_surface.mode import _ModeEntry, tomode
from ...base import listenable_property, task
from .. import Component
from ..controls import ButtonControl, SendValueInputControl
from ..display import Renderable
from . import ImmediateBehaviour, make_mode_button_control

class ModesComponent(Component, Renderable):
    pass
    mode_selection_control = SendValueInputControl()
    cycle_mode_button = ButtonControl()
    default_behaviour = ImmediateBehaviour()
    pass
    previous_mode = listenable_property.managed(None)
    pass
    pass
    pass
    pass
    def __init__(self, name=None, support_momentary_mode_cycling=True, default_behaviour=None, is_private=False, *a, **k):
        super().__init__(*a, name=name, is_private=is_private, **k)
        self._support_momentary_mode_cycling = support_momentary_mode_cycling
        self._mode_list = []
        self._mode_map = {}
        self._last_selected_mode = None
        self._mode_stack = StackingResource(self._do_enter_mode, self._do_leave_mode)
        self._push_mode_tasks = {}
        self._pop_mode_tasks = {}
        if default_behaviour is not None:
            self.default_behaviour = default_behaviour

    def disconnect(self):
        self._mode_stack.release_all()
        super().disconnect()

    @property
    def modes(self):
        pass
        return self._mode_list

    @property
    def active_modes(self):
        pass
        return self._mode_stack.clients

    @listenable_property
    def selected_mode(self):
        pass
        return self._mode_stack.owner or self._last_selected_mode

    @selected_mode.setter
    def selected_mode(self, mode):
        self.previous_mode = self.selected_mode
        if self.is_enabled():
            if self.selected_mode!= mode and mode is not None:
                    self.push_mode(mode)
                    self.pop_unselected_modes()
                    self.notify(self.notifications.Modes.select, cast(str, self.name), cast(str, mode))
                else:  # inserted
                    self._mode_stack.release_all()
                    return
            else:  # inserted
                return None
        else:  # inserted
            self._last_selected_mode = mode

    def get_mode(self, name):
        pass
        entry = self._mode_map.get(name, None)
        return entry and entry.mode

    def get_mode_button(self, name):
        pass
        return getattr(self, '%s_button' % name)

    def get_mode_groups(self, name):
        pass
        entry = self._mode_map.get(name, None)
        return entry.groups if entry else set()

    def push_mode(self, mode, delay=0):
        pass
        self._cancel_push_mode_task(mode)
        if mode in self._pop_mode_tasks:
            self._cancel_pop_mode_task(mode)
            return
        else:  # inserted
            if not delay:
                self._do_push_mode(mode)
                return
            else:  # inserted
                self._push_mode_tasks[mode] = self._tasks.add(task.sequence(task.wait(delay), task.run(partial(self._do_push_mode, mode))))
                return

    def _do_push_mode(self, mode):
        self._cancel_push_mode_task(mode)
        self._mode_stack.grab(mode)

    def _cancel_push_mode_task(self, mode):
        if mode in self._push_mode_tasks:
            self._push_mode_tasks[mode].kill()
            self._tasks.remove(self._push_mode_tasks[mode])
            del self._push_mode_tasks[mode]

    def pop_mode(self, mode, delay=0):
        pass
        self._cancel_pop_mode_task(mode)
        if mode in self._push_mode_tasks:
            self._cancel_push_mode_task(mode)
            return
        else:  # inserted
            if not delay:
                self._do_pop_mode(mode)
                return
            else:  # inserted
                self._pop_mode_tasks[mode] = self._tasks.add(task.sequence(task.wait(delay), task.run(partial(self._do_pop_mode, mode))))
                return

    def _do_pop_mode(self, mode):
        self._cancel_pop_mode_task(mode)
        if len(self.active_modes) <= 1:
            return
        else:  # inserted
            self._mode_stack.release(mode)

    def _cancel_pop_mode_task(self, mode):
        if mode in self._pop_mode_tasks:
            self._pop_mode_tasks[mode].kill()
            self._tasks.remove(self._pop_mode_tasks[mode])
            del self._pop_mode_tasks[mode]

    def pop_unselected_modes(self):
        pass
        self._mode_stack.release_stacked()

    def pop_groups(self, groups):
        pass
        if not isinstance(groups, set):
            groups = set(groups)
        for client in self._mode_stack.clients:
            if self.get_mode_groups(client) & groups:
                self._mode_stack.release(client)
            continue

    def cycle_mode(self, delta=1):
        pass
        current_index = self._mode_list.index(self.selected_mode) if self.selected_mode else -delta
        current_index = (current_index + delta) % len(self._mode_list)
        self.selected_mode = self._mode_list[current_index]
    pass
    def add_mode(self, name, mode_or_component, groups=None, behaviour=None, selector=None):
        pass
        groups = set(groups) if groups is not None else set()
        mode = tomode(mode_or_component)
        behaviour = behaviour or self.default_behaviour
        self._mode_list.append(name)
        self._mode_map[name] = _ModeEntry(mode=mode, cycle_mode_button_color='{}.On'.format(self._get_mode_color_base_name(name)), behaviour=behaviour, groups=groups)
        self.add_mode_button_control(name, behaviour)
        if callable(selector):
            selector(self, name)
            return

    def add_mode_button_control(self, mode_name, behaviour):
        pass
        mode_color_basename = self._get_mode_color_base_name(mode_name)
        colors = {'mode_selected_color': '{}.On'.format(mode_color_basename), 'mode_unselected_color': '{}.Off'.format(mode_color_basename), 'mode_group_active_color': '{}.On'.format(mode_color_basename)}
        button_control = make_mode_button_control(self, mode_name, behaviour, **colors)
        self.add_control('{}_button'.format(mode_name), button_control)
        self._update_mode_controls(self.selected_mode)

    @mode_selection_control.value
    def mode_selection_control(self, value, _):
        self._handle_mode_selection_control_value(value)

    def _handle_mode_selection_control_value(self, value):
        modes = self.modes
        if value < len(modes):
            self.selected_mode = modes[value]
            return

    @cycle_mode_button.pressed
    def cycle_mode_button(self, _):
        if self._mode_list:
            self.cycle_mode(1)

    @cycle_mode_button.released_delayed
    def cycle_mode_button(self, _):
        if self._mode_list and self._support_momentary_mode_cycling:
                self.cycle_mode((-1))
                return
        else:  # inserted
            return

    def _do_enter_mode(self, name):
        entry = self._mode_map[name]
        entry.mode.enter_mode()
        self._update_mode_controls(name)
        self.notify_selected_mode(name)
        self.notify(self.notifications.Modes.select, cast(str, self.name), cast(str, name))

    def _do_leave_mode(self, name):
        self._mode_map[name].mode.leave_mode()
        if self._mode_stack.stack_size == 0:
            self._update_mode_controls(None)
            self.notify_selected_mode(None)

    def _get_mode_behaviour(self, name):
        entry = self._mode_map.get(name, None)
        return entry.behaviour if entry is not None else self.default_behaviour

    def _get_mode_color_base_name(self, mode_name):
        return '{}.{}'.format(self.name.title().replace('_', ''), mode_name.title().replace('_', ''))

    def on_enabled_changed(self):
        super().on_enabled_changed()
        if not self.is_enabled():
            self._last_selected_mode = self.selected_mode
            self._mode_stack.release_all()
            return
        else:  # inserted
            if self._last_selected_mode:
                self.push_mode(self._last_selected_mode)
                return
            else:  # inserted
                return None

    def _update_mode_controls(self, selected_mode):
        entry = self._mode_map.get(selected_mode)
        color = entry.cycle_mode_button_color if entry else None
        if color is not None:
            self.cycle_mode_button.color = color
        if selected_mode in self._mode_list:
            self.mode_selection_control.value = self._mode_list.index(selected_mode)
            return