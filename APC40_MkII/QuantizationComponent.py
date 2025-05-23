# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40_MkII\QuantizationComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

import Live
from _Framework.Control import RadioButtonControl, control_list
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
AVAILABLE_QUANTIZATION = [Live.Song.Quantization.q_no_q, Live.Song.Quantization.q_8_bars, Live.Song.Quantization.q_4_bars, Live.Song.Quantization.q_2_bars, Live.Song.Quantization.q_bar, Live.Song.Quantization.q_quarter, Live.Song.Quantization.q_eight, Live.Song.Quantization.q_sixtenth]

class QuantizationComponent(ControlSurfaceComponent):
    quantization_buttons = control_list(RadioButtonControl)

    def __init__(self, *a, **k):
        super(QuantizationComponent, self).__init__(*a, **k)
        self.quantization_buttons.control_count = len(AVAILABLE_QUANTIZATION) + 1
        self._on_clip_trigger_quantization_changed.subject = self.song()
        self._on_clip_trigger_quantization_changed()

    @quantization_buttons.checked
    def quantization_buttons(self, button):
        if 0 <= button.index < len(AVAILABLE_QUANTIZATION):
            quantization = AVAILABLE_QUANTIZATION[button.index]
            if quantization != self.song().clip_trigger_quantization:
                self.song().clip_trigger_quantization = quantization
                return

    @subject_slot('clip_trigger_quantization')
    def _on_clip_trigger_quantization_changed(self):
        self._get_button(self.song().clip_trigger_quantization).is_checked = True

    def _get_button(self, quantization):
        if quantization in AVAILABLE_QUANTIZATION:
            return self.quantization_buttons[AVAILABLE_QUANTIZATION.index(quantization)]
        else:
            return self.quantization_buttons[-1]