# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\browser_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
FilterType = Live.Browser.FilterType
DeviceType = Live.Device.DeviceType

def filter_type_for_hotswap_target(target, default=FilterType.disabled):
    pass
    if isinstance(target, Live.Device.Device):
        if target.type == DeviceType.instrument:
            return FilterType.instrument_hotswap
        elif target.type == DeviceType.audio_effect:
            return FilterType.audio_effect_hotswap
        elif target.type == DeviceType.midi_effect:
            return FilterType.midi_effect_hotswap
        else:
            FilterType.disabled
    elif isinstance(target, Live.DrumPad.DrumPad):
        return FilterType.drum_pad_hotswap
    elif isinstance(target, Live.Chain.Chain):
        return filter_type_for_hotswap_target(target.canonical_parent) if target else FilterType.disabled
    return default

def get_selection_for_new_device(selection, insert_left=False):
    pass
    selected = selection.selected_object
    if isinstance(selected, Live.DrumPad.DrumPad) and selected.chains and selected.chains[0].devices:
        index = 0 if insert_left else -1
        selected = selected.chains[0].devices[index]
    elif not isinstance(selected, Live.Device.Device):
        selected = selection.selected_device
    return selected