# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\mode\behaviour.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import mixin
from . import ModeButtonBehaviour, pop_last_mode

def make_reenter_behaviour(base_behaviour, on_reenter=None, *a, **k):
    pass
    return mixin(ReenterBehaviourMixin, base_behaviour)(*a, on_reenter=on_reenter, **k)

class ReenterBehaviourMixin:
    pass

    def __init__(self, on_reenter=None, *a, **k):
        super().__init__(*a, **k)
        self._on_reenter = on_reenter

    def press_immediate(self, component, mode):
        pass
        was_active = component.selected_mode == mode
        super().press_immediate(component, mode)
        if was_active:
            self._on_reenter()

class ToggleBehaviour(ModeButtonBehaviour):
    pass

    def __init__(self, return_to_default=False, *a, **k):
        super().__init__(*a, **k)
        self._return_to_default = return_to_default

    def press_immediate(self, component, mode):
        if component.selected_mode == mode:
            if self._return_to_default:
                component.push_mode(component.modes[0])
                component.pop_unselected_modes()
                return
            else:
                pop_last_mode(component, mode)
        else:
            component.push_mode(mode)

class MomentaryBehaviour(ModeButtonBehaviour):
    pass

    def __init__(self, entry_delay=None, exit_delay=None, immediate_exit_delay=None):
        self._entry_delay = entry_delay
        self._exit_delay = exit_delay
        self._immediate_exit_delay = self._exit_delay if immediate_exit_delay is None else immediate_exit_delay

    def press_immediate(self, component, mode):
        component.push_mode(mode, delay=self._entry_delay)

    def release_immediate(self, component, mode):
        component.pop_mode(mode, delay=self._immediate_exit_delay)

    def release_delayed(self, component, mode):
        component.pop_mode(mode, delay=self._exit_delay)