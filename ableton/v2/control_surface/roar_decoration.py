# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\roar_decoration.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .decoration import LiveObjectDecorator
from .internal_parameter import EnumWrappingParameter

class RoarDeviceDecorator(LiveObjectDecorator):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._additional_parameters = self._create_parameters()
        self.register_disconnectables(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    def _create_parameters(self):
        return (EnumWrappingParameter(name='Routing', parent=self, values_host=self._live_object, index_property_host=self, values_property='routing_mode_list', index_property='routing_mode_index'),)