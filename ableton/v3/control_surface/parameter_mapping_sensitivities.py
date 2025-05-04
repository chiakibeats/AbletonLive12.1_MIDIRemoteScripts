# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\parameter_mapping_sensitivities.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ..live import is_parameter_quantized, liveobj_valid
DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY = 1.0
pass
DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY = 0.1
pass
FINE_GRAIN_SENSITIVITY_FACTOR = 0.1
pass
QUANTIZED_SENSITIVITY_FACTOR = 8
pass
def get_base_quantized_sensitivity(parameter):
    pass
    v_range = parameter.max - parameter.min
    is_on_off_parameter = v_range == 1.0
    if is_on_off_parameter:
        return 1.0
    else:  # inserted
        return v_range / QUANTIZED_SENSITIVITY_FACTOR

def parameter_mapping_sensitivities(continuous_parameter_sensitivity=DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, quantized_parameter_sensitivity=DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY):
    pass
    described_sensitivities = create_sensitivities(quantized_parameter_sensitivity)

    def inner(parameter, device):
        default = continuous_parameter_sensitivity
        is_quantized = False
        if liveobj_valid(parameter):
            is_quantized = is_parameter_quantized(parameter, device)
            try:
                default = described_sensitivities[device.class_name][parameter.name]
            except KeyError:
                if is_quantized:
                    default = get_base_quantized_sensitivity(parameter) * quantized_parameter_sensitivity
                pass
        return (default, default if is_quantized else default * FINE_GRAIN_SENSITIVITY_FACTOR)
    return inner

def create_sensitivities(quantized_parameter_sensitivity):
    pass
    q_min = quantized_parameter_sensitivity / 2
    q_default = quantized_parameter_sensitivity
    q_median = quantized_parameter_sensitivity * 3
    q_max = quantized_parameter_sensitivity * 6
    return {'BeatRepeat': {'Pitch': q_default}, 'GrainDelay': {'Pitch': q_median}, 'InstrumentImpulse': {'1 Transpose': q_median, '2 Transpose': q_median, '3 Transpose': q_median, '4 Transpose': q_median, '5 Transpose': q_median, '6 Transpose': q_median, '7 Transpose': q_median, '8 Transpose': q_median, 'Global Transpose': q_median}, 'LoungeLizard': {'Semitone': q_default}, 'MidiArpeggiator': {'Transp. Dist.': q_median}, 'MidiScale': {'A Coarse': q_median, 'B Coarse': q_median, 'C Coarse': q_median, 'D Coarse': q_median}, 'MultiSampler': {'I Note': q_median, 'II Pitch': q_median, 'III Pitch': q_median, 'IV Pitch': q_median, 'V Pitch': q_median}, 'Operator': {'Octave': q_min, 'Semitone': q_default}, 'OriginalSimpler': {