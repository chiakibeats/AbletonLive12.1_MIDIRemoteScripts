# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\control_surface_specification.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from types import SimpleNamespace
from . import DEFAULT_BANK_SIZE, BasicColors, midi
from .components import AutoArmComponent, BasicRecordingMethod, SessionRingComponent, TargetTrackComponent
from .consts import LOW_PRIORITY
from .default_bank_definitions import BANK_DEFINITIONS
from .default_skin import default_skin
from .device_provider import DeviceProvider
from .display import DisplaySpecification
from .parameter_mapping_sensitivities import DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY

class ControlSurfaceSpecification(SimpleNamespace):
    pass
    elements_type = None
    control_surface_skin = default_skin
    display_specification = DisplaySpecification()
    num_tracks = 8
    num_scenes = 1
    include_returns = False
    include_master = False
    right_align_non_player_tracks = False
    snap_track_offset = False
    include_auto_arming = False
    link_session_ring_to_track_selection = False
    link_session_ring_to_scene_selection = False
    session_ring_component_type = SessionRingComponent
    target_track_component_type = TargetTrackComponent
    auto_arm_component_type = AutoArmComponent
    device_provider_type = DeviceProvider
    recording_method_type = BasicRecordingMethod
    feedback_channels = None
    playing_feedback_velocity = BasicColors.ON.midi_value
    recording_feedback_velocity = BasicColors.ON.midi_value
    background_priority = LOW_PRIORITY
    identity_response_id_bytes = None
    custom_identity_response = None
    identity_request = midi.SYSEX_IDENTITY_REQUEST_MESSAGE
    identity_request_delay = 0.0
    hello_messages = None
    goodbye_messages = None
    send_goodbye_messages_last = True
    create_mappings_function = lambda *x: {}
    component_map = {}
    parameter_bank_definitions = BANK_DEFINITIONS
    parameter_bank_size = DEFAULT_BANK_SIZE
    continuous_parameter_sensitivity = DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY
    quantized_parameter_sensitivity = DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY