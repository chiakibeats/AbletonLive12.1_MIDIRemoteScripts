# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\legacy_bank_definitions.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
from _Generic.Devices import BANK_NAME_DICT, DEVICE_BOB_DICT, DEVICE_DICT
from ableton.v2.base.collection import IndexedDict
from ..base import memoize
from . import BANK_PARAMETERS_KEY
BEST_OF_PARAMETERS_KEY = 'Best of Parameters'

@memoize
def banked():
    pass
    return {device_name: IndexedDict([(bank_name, {BANK_PARAMETERS_KEY: parameters}) for bank_name, parameters in zip(bank_names, DEVICE_DICT[device_name])]) for device_name, bank_names in BANK_NAME_DICT.items()}

@memoize
def best_of_banks():
    pass
    return {device_name: IndexedDict([(BEST_OF_PARAMETERS_KEY, {BANK_PARAMETERS_KEY: parameters[0]})]) for device_name, parameters in DEVICE_BOB_DICT.items()}