# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\parameter_info.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import ParameterInfo as ParameterInfoBase
from ..live import liveobj_valid

class ParameterInfo(ParameterInfoBase):
    pass

    def __init__(self, parameter=None, name=None, *a, **k):
        super().__init__(*a, parameter=parameter, name=name, **k)
        if liveobj_valid(parameter) and name is not None:
            parameter.display_name = name

    @property
    def original_name(self):
        return self.parameter.original_name if liveobj_valid(self.parameter) else ''