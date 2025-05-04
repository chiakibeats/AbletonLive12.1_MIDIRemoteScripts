# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\clip_actions.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import depends, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl

class ClipActionsComponent(Component):
    pass
    is_private = True
    quantize_button = ButtonControl()

    @depends(quantization_component=None)
    def __init__(self, quantization_component=None, *a, **k):
        super().__init__(*a, **k)
        self._quantization_component = quantization_component
        self.register_slot(self.song.view, self._update_quantize_button, 'detail_clip')
        self._update_quantize_button()

    @quantize_button.pressed
    def quantize_button(self, _):
        self._quantization_component.quantize_clip(self.song.view.detail_clip)

    def _update_quantize_button(self):
        self.quantize_button.enabled = liveobj_valid(self.song.view.detail_clip)