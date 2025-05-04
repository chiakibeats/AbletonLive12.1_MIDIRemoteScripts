# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\SpecialModesComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ModesComponent import ModesComponent, ReenterBehaviour

class SpecialModesComponent(ModesComponent):

    def on_enabled_changed(self):
        super(SpecialModesComponent, self).on_enabled_changed()
        if not self.is_enabled():
            self._last_selected_mode = None

class SpecialReenterBehaviour(ReenterBehaviour):
    pass

    def __init__(self, mode_name=None, *a, **k):
        super(ReenterBehaviour, self).__init__(*a, **k)
        self._mode_name = mode_name

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(ReenterBehaviour, self).press_immediate(component, mode)
        if was_active and self._mode_name is not None and component.get_mode(self._mode_name):
            component.push_mode(self._mode_name)
            component.pop_unselected_modes()
            return

class CancelingReenterBehaviour(SpecialReenterBehaviour):

    def __init__(self, *a, **k):
        super(CancelingReenterBehaviour, self).__init__(*a, **k)
        self._reenter_mode_active = False

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(CancelingReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            self._reenter_mode_active = True

    def release_immediate(self, component, mode):
        super(CancelingReenterBehaviour, self).release_immediate(component, mode)
        self._return(component, mode)

    def release_delayed(self, component, mode):
        super(CancelingReenterBehaviour, self).release_delayed(component, mode)
        self._return(component, mode)

    def _return(self, component, mode):
        if self._reenter_mode_active:
            component.push_mode(mode)
            component.pop_unselected_modes()
            self._reenter_mode_active = False