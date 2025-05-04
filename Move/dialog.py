# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\dialog.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import listenable_property
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.display import Renderable

class DialogComponent(Component, Renderable):
    pass
    any_dialog_open = listenable_property.managed(False)

    def __init__(self, *a, **k):
        super().__init__(*a, name='Dialog', **k)
        self.register_slot(self.application, self._on_dialog_opened, 'open_dialog_count')

    def _on_dialog_opened(self):
        self.any_dialog_open = self.application.open_dialog_count > 0