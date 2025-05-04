# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\parameter_mapping_sensitivities.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import is_parameter_quantized
DEFAULT_SENSITIVITY_KEY = 'normal_sensitivity'
FINE_GRAINED_SENSITIVITY_KEY = 'fine_grained_sensitivity'
CONTINUOUS_MAPPING_SENSITIVITY = 2.0
FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY = 0.01
QUANTIZED_MAPPING_SENSITIVITY = old_div(1.0, 15.0)
S Length = {'UltraAnalog': {DEFAULT_SENSITIVITY_KEY: 0.05}, DEFAULT_SENSITIVITY_KEY: 0.05, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.05, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.5, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY: 0.1, DEFAULT_SENSITIVITY_KEY

def sensitivity_mapping_for_parameter(parameter, fine_grain=False):
    is_quantized = is_parameter_quantized(parameter, parameter and parameter.canonical_parent)
    return QUANTIZED_MAPPING_SENSITIVITY if is_quantized else FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY if fine_grain else CONTINUOUS_MAPPING_SENSITIVITY

def parameter_mapping_sensitivity(parameter, device_class=None):
    parameter_name = parameter.name if liveobj_valid(parameter) else ''
    try:
        return PARAMETER_SENSITIVITIES[device_class][parameter_name][DEFAULT_SENSITIVITY_KEY]
    except KeyError:
        return sensitivity_mapping_for_parameter(parameter)

def fine_grain_parameter_mapping_sensitivity(parameter, device_class=None):
    parameter_name = parameter.name if liveobj_valid(parameter) else ''
    try:
        return PARAMETER_SENSITIVITIES[device_class][parameter_name][FINE_GRAINED_SENSITIVITY_KEY]
    except KeyError:
        return sensitivity_mapping_for_parameter(parameter, fine_grain=True)