# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\SpecialMixerComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.MixerComponent import MixerComponent
from .DisplayingChanStripComponent import DisplayingChanStripComponent

class SpecialMixerComponent(MixerComponent):
    pass

    def __init__(self, name_display, value_display, num_tracks, num_returns=0):
        MixerComponent.__init__(self, num_tracks, num_returns=0)
        self._name_display = name_display
        self._value_display = value_display
        for index in range(num_tracks):
            self._channel_strips[index].set_name_display(self._name_display)
            self._channel_strips[index].set_value_display(self._value_display)
        for index in range(num_returns):
            self._return_strips[index].set_name_display(self._name_display)
            self._return_strips[index].set_value_display(self._value_display)
        self._selected_strip.set_name_display(self._name_display)
        self._selected_strip.set_value_display(self._value_display)

    def disconnect(self):
        MixerComponent.disconnect(self)
        self._name_display = None
        self._value_display = None

    def tracks_to_use(self):
        return self.song().visible_tracks + self.song().return_tracks

    def _create_strip(self):
        return DisplayingChanStripComponent()