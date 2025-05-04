# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\custom_bank_definitions.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from copy import deepcopy
from ableton.v2.base.collection import IndexedDict
from ableton.v3.control_surface import BANK_DEFINITIONS, BANK_MAIN_KEY, BANK_PARAMETERS_KEY
from ableton.v3.live import liveobj_valid
from .banking_util import use
SHIFTED_PARAMETER_MAPPINGS = {'DrumCell': ('Detune', 'Length'), 'OriginalSimpler': ('Detune', 'L Rate', 'L Sync Rate', 'S Length')}
pass
def is_shifted_parameter_mapping(device_name, parameter):
    pass
    return liveobj_valid(parameter) and parameter.original_name in SHIFTED_PARAMETER_MAPPINGS.get(device_name, ())
CUSTOM_BANK_DEFINITIONS = deepcopy(BANK_DEFINITIONS)
CUSTOM_BANK_DEFINITIONS['ChannelEq'] = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: ('Low Gain', 'Mid Gain', use('Mid Freq').with_name('Mid Frequency'), 'High Gain', use('Highpass On').with_name('High-Pass'), use('Gain').with_name('Output'), '', '')}),))
CUSTOM_BANK_DEFINITIONS['Chorus2'] = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: ('Mode', 'Rate', 'Amount', use('Shape').if_parameter('Mode').has_value('Vibrato').else_use('Feedback'), use('HPF Freq').with_name('High-Pass Freq'), use('').if_parameter('Mode').has_value('Vibrato').else_use('Width'), 'Warmth', 'Dry/Wet')}),))
CUSTOM_BANK_DEFINITIONS['Delay'] = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: (use('L 16th').with_name('Time in 16ths').if_parameter('L Sync').has_value('On').else_use('L Time').with_name('Time'), 'Feedback', use('Filter Freq').with_name('Filter Frequency'), 'Filter Width', use('Mod Freq').with_name('Modulation Freq'), use('Filter < Mod').with_name('Filter Modulation'), use('Dly < Mod').with_name('Time Modulation'), 'Dry/Wet')}),))
DrumCell = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: (use('Transpose').if_shift(False).else_use('Detune'), 'Start', 'Attack', 'Hold', use('Decay').if_shift(False).else_use('Length').else_use('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type').with_name('FX Type'
CUSTOM_BANK_DEFINITIONS['PhaserNew'] = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: ('Mode', use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Frequency'), 'Amount', 'Feedback', use('Center Freq').if_parameter('Mode').has_value('Phaser').else_use('Flange Time').if_parameter('Mode').has_value('Flanger').else_use('Doubler Time').if_parameter('Mode').has_value('Doubler'), 'Notches', 'Warmth', 'Dry/Wet')}),))
CUSTOM_BANK_DEFINITIONS['Redux2'] = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: ('Sample Rate', 'Jitter', 'Bit Depth', use('Quantizer Shape').with_name('Shape'), use('Pre-Filter On').with_name('Pre-Filter'), use('Post-Filter On').with_name('Post-Filter'), use('Post-Filter').with_name('Post-Filter Freq'), 'Dry/Wet')}),))
CUSTOM_BANK_DEFINITIONS['Reverb'] = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: ('Decay Time', 'Room Size', 'In Filter Freq', 'Predelay', 'Stereo Image', use('LowShelf Gain').with_name('Lo Shelf Gain'), use('HiFilter Freq').with_name('Hi Filter Freq').if_parameter('HiFilter Type').has_value('Lowpass').else_use('HiShelf Gain').with_name('Hi Shelf Gain'), 'Dry/Wet')}),))
CUSTOM_BANK_DEFINITIONS['Saturator'] = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: ('Drive', 'Type', use('Color Amt Low').with_name('Color Low'), use('Color Freq').with_name('Color Frequency'), use('Color Width').with_name('Color Width'), use('Color Amt Hi').with_name('Color High'), 'Output', 'Dry/Wet')}),))
OriginalSimpler = IndexedDict(((BANK_MAIN_KEY, {BANK_PARAMETERS_KEY: (use('Transpose').if_shift(False).else_use('Detune'), use('Ve Attack').with_name('Attack').if_parameter('Multi Sample').else_use('Division').if_parameter('Slice by').has_value('Beat').if_parameter('Regions').if_parameter('Region').has_value(''), use('Nudge').with_name('Ve Decay').if_parameter('Decay').has_value('Classic').else_use('End'), use('Ve Sustain').with_name('Sustain').with_name('Fade In').with_name('S Length').if_shift(False).else_use('L Rate').with_name('LFO Rate').else_use('L Sync').with_name('LFO Rate'))}),))