# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\drift_decoration.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .decoration import LiveObjectDecorator
from .internal_parameter import EnumWrappingParameter

class DriftDeviceDecorator(LiveObjectDecorator):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._additional_parameters = self._create_parameters()
        self.register_disconnectables(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    def _create_parameters(self):
        return (EnumWrappingParameter(name='Voice Mode', parent=self, values_host=self._live_object, index_property_host=self, values_property='voice_mode_list', index_property='voice_mode_index'), EnumWrappingParameter(name='Voice Count', parent=self, values_host=self._live_object, index_property_host=self, values_property='voice_count_list', index_property='voice_count_index'), EnumWrappingParameter(name='LP Mod Src 1', parent=self, values_host=self._live_object, index_property_host=self, values_property='mod_matrix_filter_source_1_list', index_property='mod_matrix_filter_source_1_index'), EnumWrappingParameter(name='LP Mod Src 2', parent=self, values_host=self._live_object, index_property_host=self, values_property='mod_matrix_filter_source_2_list', index_property='mod_matrix_filter_source_2_index'))