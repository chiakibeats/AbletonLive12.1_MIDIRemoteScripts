# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import BANK_FORMAT, BANK_MAIN_KEY, BANK_PARAMETERS_KEY, MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, MIDI_SYSEX_TYPE, CompoundElement, ControlElement, DeviceBankRegistry, EnumWrappingParameter, InputControlElement, InternalParameter, NotifyingControlElement, NotifyingList, ParameterProvider, PrioritizedResource, RelativeInternalParameter, SharedResource, all_parameters, find_instrument_devices, find_instrument_meeting_requirement, use
from ableton.v2.control_surface.default_bank_definitions import BANK_DEFINITIONS as V2_BANK_DEFINITIONS
from ableton.v2.control_surface.defaults import DOUBLE_CLICK_DELAY
from ableton.v2.control_surface.elements.encoder import ABSOLUTE_MAP_MODES
from ableton.v2.control_surface.input_control_element import ScriptForwarding
from . import midi
from .banking_util import DEFAULT_BANK_SIZE, BankingInfo, DescribedDeviceParameterBank, create_parameter_bank
from .colors import STANDARD_COLOR_PALETTE, STANDARD_FALLBACK_COLOR_TABLE, BasicColors
from .component import Component
from .consts import ACTIVE_PARAMETER_TIMEOUT, DEFAULT_PRIORITY, HIGH_PRIORITY, LOW_PRIORITY, M4L_PRIORITY, MOMENTARY_DELAY
from .control_surface import ControlSurface, create_control_surface
from .control_surface_specification import ControlSurfaceSpecification
from .default_bank_definitions import BANK_DEFINITIONS
from .default_skin import create_skin, default_skin
from .device_provider import DeviceProvider
from .elements_base import ElementsBase, MapMode, create_button, create_combo_element, create_encoder, create_matrix_identifiers, create_sysex_element, create_sysex_sending_button
from .identification import IdentificationComponent
from .instrument_finder import InstrumentFinderComponent
from .layer import Layer
from .parameter_info import ParameterInfo
from .parameter_mapping_sensitivities import DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, FINE_GRAIN_SENSITIVITY_FACTOR, parameter_mapping_sensitivities
from .session_ring_selection_linking import SessionRingSelectionLinking
from .skin import LiveObjSkinEntry, OptionalSkinEntry, Skin, merge_skins
MIDI_NOTE_TYPE = ('ABSOLUTE_MAP_MODES', 'ACTIVE_PARAMETER_TIMEOUT', 'BANK_DEFINITIONS', 'BANK_FORMAT', 'BANK_MAIN_KEY', 'BANK_PARAMETERS_KEY', 'DEFAULT_BANK_SIZE', 'DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY', 'DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY', 'DEFAULT_PRIORITY', 'DOUBLE_CLICK_DELAY', 'FINE_GRAIN_SENSITIVITY_FACTOR', 'HIGH_PRIORITY', 'LOW_PRIORITY', 'M4L_PRIORITY', 'MIDI_CC_TYPE', 'MIDI_NOTE_TYPE', 'MIDI_PB_TYPE', 'MIDI_SYSEX_TYPE', 'MOMENTARY_DELAY', 'STANDARD_COLOR_PALETTE', 'STANDARD_FALLBACK_COLOR_TABLE', 'V2_BANK_DEFINITIONS', 'BankingInfo', 'BasicColors', 'Component', 'CompoundElement', 'ControlElement', 'ControlSurface', 'ControlSurfaceSpecification', 'DescribedDeviceParameterBank', 'DeviceBankRegistry', 'DeviceProvider', 'ElementsBase', 'EnumWrappingParameter', 'IdentificationComponent', 'InputControlElement', 'InstrumentFinderComponent', 'InternalParameter', 'Layer', 'LiveObjSkinEntry', 'MapMode', 'NotifyingControlElement', 'NotifyingList', 'OptionalSkinEntry', 'ParameterInfo', 'ParameterProvider', 'PrioritizedResource', 'RelativeInternalParameter', 'ScriptForwarding', 'SessionRingSelectionLinking'