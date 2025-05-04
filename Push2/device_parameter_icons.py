# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_parameter_icons.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

DRIFT_OSC1 = ('wave_sine', 'wave_triangle', 'wave_sharktooth', 'wave_saturated', 'wave_saw_up', 'wave_pulse', 'wave_square')
DRIFT_OSC2 = ('wave_sine', 'wave_triangle', 'wave_saturated', 'wave_saw_up', 'wave_square')
DRIFT_LFO = ('wave_sine', 'wave_triangle', 'wave_saw_up', 'wave_saw_down', 'wave_square', 'wave_sh_mono', 'wave_noiseramp', 'wave_linenv', 'wave_logenv')
DRIFT_LFO_MODES = ('lfo_free', 'lfo_time', 'lfo_ratio', 'lfo_sync')
DRIFT_VOICE_MODES = ('voicemode_poly', 'voicemode_mono', 'voicemode_stereo', 'voicemode_unison')
DRIFT_FILTERS = ('filter_low_12', 'filter_low_24')
MELD_OSCILLATOR_TYPES = ('meld_osc_basic_shapes', 'meld_osc_dual_basic_shapes', 'meld_osc_noisy_shapes', 'meld_osc_square_sync', 'meld_osc_square_5th', 'meld_osc_sub', 'meld_osc_swarm_sine', 'meld_osc_swarm_triangle', 'meld_osc_swarm_saw', 'meld_osc_swarm_square', 'meld_osc_harmonic_fm', 'meld_osc_fold_fm', 'meld_osc_squelch', 'meld_osc_simple_fm', 'meld_osc_chip', 'meld_osc_shepards_pi', 'meld_osc_tarp', 'meld_osc_extratone', 'meld_osc_noise_loop', 'meld_osc_filtered_noise', 'meld_osc_bitgrunge', 'meld_osc_crackle', 'meld_osc_rain', 'meld_osc_bubbles')
OPERATOR_OSCILLATORS = ('wave_sine', 'wave_sine_4bit', 'wave_sine_8bit', 'wave_saw_3', 'wave_saw_4', 'wave_saw_6', 'wave_saw_8', 'wave_saw_16', 'wave_saw_32', 'wave_saw_64', 'wave_saw_down', 'wave_square_3', 'wave_square_4', 'wave_square_6', 'wave_square_8', 'wave_square_16', 'wave_square_32', 'wave_square_64', 'wave_square', 'wave_triangle', 'wave_noise_loop', 'wave_noise_white', 'wave_user')
ACTIVATE = ('control_off', 'control_on')
ANALOG_OSCILLATORS = ('wave_sine', 'wave_saw_down', 'wave_square', 'wave_noise_white')
ANALOG_L_F_O = ('wave_sine', 'wave_triangle', 'wave_square', 'wave_noise_white', 'wave_noise_white')
ANALOG_FILTERS = ('filter_low_12', 'filter_low_24', 'filter_band_6', 'filter_band_12', 'filter_notch_12', 'filter_notch_24', 'filter_high_12', 'filter_high_24', 'filter_formant_6', 'filter_formant_12')
RESONANCE_TYPES = ('co_beam', 'co_marimba', 'co_string', 'co_membrane', 'co_plate', 'co_pipe', 'co_tube')
COLLISION_FILTERS = ('filter_low_12', 'filter_high_12', 'filter_band_12', 'filter_band_6')
COLLISION_L_F_O = ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_up', 'wave_saw_down', 'wave_sh_mono', 'wave_noise_white')
IMPULSE_FILTERS = ('filter_low_12', 'filter_low_24', 'filter_band_12', 'filter_band_24', 'filter_high_12', 'filter_high_24', 'filter_notch_12')
SAMPLER_OSCILLATORS = ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_down', 'wave_saw_up', 'wave_sh_mono')
LFO_WAVEFORMS = ('wave_sine', 'wave_square', 'wave_triangle', 'wave_saw_up', 'wave_saw_down', 'wave_sh_stereo', 'wave_sh_mono')
STEREO_MODE = ('lfo_phase', 'lfo_spin')
SYNC = ('lfo_free', 'lfo_sync')
EQ8_FILTER_TYPES = ('filter_high_48', 'filter_high_12', 'filter_low_shelf', 'filter_bell', 'filter_notch_24', 'filter_high_shelf', 'filter_low_12', 'filter_low_48')
CYTOMIC_FILTER_TYPES = ('filter_low_48', 'filter_high_48', 'filter_band_24', 'filter_notch_24', 'filter_morph_24')
FILTER_CIRCUIT_TYPES = ('circuit_clean', 'circuit_osr', 'circuit_ms2', 'circuit_smp', 'circuit_prd')
COMPRESSOR_MODES = ('compressor_peak', 'compressor_rms', 'compressor_expand')
WAVETABLE_LOOP_MODE = ('wavetable_env_loop_none', 'wavetable_env_loop_trigger', 'wavetable_env_loop')
WAVETABLE_OSCILLATOR_SWITCH = ('wavetable_osc_1', 'wavetable_osc_2', 'wavetable_osc_sub', 'wavetable_osc_mix')
WAVETABLE_OSCILLATOR_EFFECT_TYPES = ('wavetable_effect_none', 'wavetable_effect_fm', 'wavetable_effect_classic', 'wavetable_effect_modern')
WAVETABLE_FILTER_TYPES = ('wavetable_filter_1', 'wavetable_filter_2', 'wavetable_filter_3', 'wavetable_filter_4', 'wavetable_filter_5')
WAVETABLE_LFO_TYPES = ('lfo_sine_small', 'lfo_triangle_small', 'lfo_saw_down_small', 'lfo_square_small', 'lfo_random_small')
WAVETABLE_VOICES = ('voices_2', 'voices_3', 'voices_4', 'voices_5', 'voices_6', 'voices_7', 'voices_8')
GENERIC_PARAMETER_IMAGES = {'LFO Waveform': LFO_WAVEFORMS, 'Waveform': ('wave_sine', 'wave_triangle', 'wave_saw_down', 'wave_sh_stereo'), 'Filter Type': ('filter_low_48', 'filter_high_48', 'filter_band_24', 'filter_notch_24'), 'Ext. In On': ACTIVATE, 'LFO Sync': SYNC, 'Sync': SYNC, 'Adaptive Q': ACTIVATE, 'LFO Stereo Mode': STEREO_MODE, 'Side Listen': ACTIVATE, 'EQ On': ACTIVATE, 'EQ Mode': ('filter_low_shelf', 'filter_bell', 'filter_high_shelf', 'filter_low_48', 'filter_band_24', 'filter_high_48')}
LFO2 Shape = {'Drift': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'ANALOG_OSCILLATORS': {'ANALOG_OSCILLATORS': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'ANALOG_OSCILLATORS': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {'Vib On/Off': {''': {''

def get_image_filenames_from_ids(image_ids, small_images=False, image_id_to_filename=IMAGE_ID_TO_FILENAME):
    image_index = 1 if small_images else 0
    return [image_id_to_filename.get(image_id, ('', ''))[image_index] for image_id in image_ids]

def get_image_filenames(parameter_name, device_type, small_images=False, device_parameter_images=DEVICE_PARAMETER_IMAGES, generic_parameter_images=GENERIC_PARAMETER_IMAGES, image_id_to_filename=IMAGE_ID_TO_FILENAME):
    image_ids = []
    if device_type in device_parameter_images and parameter_name in device_parameter_images[device_type]:
        image_ids = device_parameter_images[device_type][parameter_name]
    else:  # inserted
        if parameter_name in generic_parameter_images:
            image_ids = generic_parameter_images[parameter_name]
    return get_image_filenames_from_ids(image_ids, small_images=small_images, image_id_to_filename=image_id_to_filename)