# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\global_quantization.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from Live.Song import Quantization
from ableton.v3.base import listens
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import FixedRadioButtonGroup
AVAILABLE_RATES = (Quantization.q_8_bars, Quantization.q_4_bars, Quantization.q_2_bars, Quantization.q_bar, Quantization.q_quarter, Quantization.q_eight, Quantization.q_sixtenth, Quantization.q_thirtytwoth)

class GlobalQuantizationComponent(Component):
    pass
    rate_buttons = FixedRadioButtonGroup(control_count=8, unchecked_color='GlobalQuantization.NotSelected', checked_color='GlobalQuantization.Selected')

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.__on_global_quantization_changed.subject = self.song
        self.__on_global_quantization_changed()

    @rate_buttons.checked
    def rate_buttons(self, button):
        self.song.clip_trigger_quantization = AVAILABLE_RATES[button.index]

    @listens('clip_trigger_quantization')
    def __on_global_quantization_changed(self):
        rate = self.song.clip_trigger_quantization
        self.rate_buttons.checked_index = AVAILABLE_RATES.index(rate) if rate in AVAILABLE_RATES else -1