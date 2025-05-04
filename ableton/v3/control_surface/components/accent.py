# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\accent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import depends, listenable_property
from .. import Component
from ..controls import ToggleButtonControl
from ..display import Renderable

class AccentComponent(Component, Renderable):
    pass
    accent_button = ToggleButtonControl(color='Accent.Off', on_color='Accent.On')

    @depends(full_velocity=None)
    def __init__(self, name='Accent', full_velocity=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._full_velocity = full_velocity
        self.accent_button.connect_property(self, 'activated')

    @listenable_property
    def activated(self):
        return self._full_velocity.enabled

    @activated.setter
    def activated(self, state):
        if state != self._full_velocity.enabled:
            self._full_velocity.enabled = state
            self.notify(self.notifications.full_velocity, state)
            self.notify_activated()

    @accent_button.released_delayed
    def accent_button(self, _):
        self.activated = False

    def update(self):
        super().update()
        if self._full_velocity.enabled != self.accent_button.is_on:
            self._full_velocity.enabled = self.accent_button.is_on