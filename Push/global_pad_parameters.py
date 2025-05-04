# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\global_pad_parameters.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Component
from . import sysex

class GlobalPadParameters(Component):

    def __init__(self, aftertouch_threshold=0, *a, **k):
        super(GlobalPadParameters, self).__init__(*a, **k)
        self._pad_parameter_element = None
        self._aftertouch_threshold = aftertouch_threshold

    def _get_aftertouch_threshold(self):
        return self._aftertouch_threshold

    def _set_aftertouch_threshold(self, value):
        self._aftertouch_threshold = value
        self._update_pad_parameter_element()
    aftertouch_threshold = property(_get_aftertouch_threshold, _set_aftertouch_threshold)

    def set_pad_parameter(self, element):
        self._pad_parameter_element = element
        self._update_pad_parameter_element()

    def _update_pad_parameter_element(self):
        if self._pad_parameter_element:
            self._pad_parameter_element.send_value(sysex.make_pad_parameter_message(aftertouch_threshold=self._aftertouch_threshold))

    def update(self):
        super(GlobalPadParameters, self).update()
        if self.is_enabled():
            self._update_pad_parameter_element()