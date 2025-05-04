# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

import logging
import weakref
from functools import partial
from Live.Base import Timer
from ableton.v3.base import const, listens
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, HIDDEN, NOTES_CC, PORTS_KEY, SCRIPT, SYNC, TYPE_KEY, controller_id, inport, outport
from ableton.v3.control_surface.components import GridResolutionComponent, SequencerClip, SessionNavigationComponent
from ableton.v3.live import liveobj_valid
from . import midi
from .auto_arm import AutoArmComponent
from .clip_actions import ClipActionsComponent, QuantizationStrength
from .colors import Colors
from .device import DeviceComponent
from .device_navigation import DeviceNavigationComponent
from .device_provider import DeviceProvider
from .dialog import DialogComponent
from .display import display_specification
from .drum_group import DrumGroupComponent
from .elements import Elements
from .firmware import FirmwareComponent, ShutDownState
from .instrument import InstrumentComponent, NoteLayout
from .loop_length import LoopLengthComponent
from .mappings import create_mappings
from .note_repeat import NoteRepeatComponent, NoteRepeatModel
from .notification_suppression import NotificationSuppressionComponent
from .recording import RecordingComponent
from .session import SessionComponent
from .skin import Skin
from .step_sequence import DEFAULT_GRID_RESOLUTION_INDEX, GRID_RESOLUTIONS, StepSequenceComponent
from .track_list import TrackListComponent
from .transport import TransportComponent
from .volume_parameters import VolumeParametersComponent
logger = logging.getLogger(__name__)
PITCH_PROVIDERS = {'drum': 'Drum_Group', 'instrument': 'Instrument', 'simpler': 'Sliced_Simpler'}

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=10626, product_ids=[6488], model_name='Ableton Move'), PORTS_KEY: [inport(props=[HIDDEN, NOTES_CC, SCRIPT]), inport(props=[HIDDEN]), outport(props=[HIDDEN, NOTES_CC, SYNC, SCRIPT]), outport(props=[HIDDEN])], AUTO_LOAD_KEY: True, TYPE_KEY: 'move'}

def create_instance(c_instance):
    return Move(specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Colors)
    num_tracks = 7
    num_scenes = 4
    include_returns = True
    right_align_non_player_tracks = True
    include_auto_arming = True
    quantized_parameter_sensitivity = 0.5
    feedback_channels = midi.NOTE_MODE_FEEDBACK_CHANNELS
    playing_feedback_velocity = Colors.GREEN.midi_value
    recording_feedback_velocity = Colors.RED.midi_value
    identity_response_id_bytes = midi.MANUFACTURER_ID + (88, 50, 1, 0)
    hello_messages = (midi.make_get_control_mode_message(),)
    goodbye_messages = (midi.make_shut_down_image_message(),)
    create_mappings_function = create_mappings
    device_provider_type = DeviceProvider
    auto_arm_component_type = AutoArmComponent
    component_map = {'Clip_Actions': ClipActionsComponent, 'Device': DeviceComponent, 'Device_Navigation': DeviceNavigationComponent, 'Drum_Group': DrumGroupComponent, 'Instrument': InstrumentComponent, 'Loop_Length': LoopLengthComponent, 'Note_Repeat': NoteRepeatComponent, 'Notification_Suppression': NotificationSuppressionComponent, 'Recording': RecordingComponent, 'Session': SessionComponent, 'Session_Navigation': partial(SessionNavigationComponent, respect_borders=True), 'Step_Sequence': StepSequenceComponent, 'Transport': TransportComponent, 'Track_List': TrackListComponent}
    display_specification = display_specification

def note_mode_for_track(track, instrument_finder):
    if liveobj_valid(track) and track.has_midi_input:
        if liveobj_valid(instrument_finder.drum_group):
            return 'drum'
        elif liveobj_valid(instrument_finder.sliced_simpler):
            return 'simpler'
        else:
            return 'instrument'
    else:
        return 'audio'

class Move(ControlSurface):
    preferences_key = 'Move'

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._can_enable_session_ring = False
        script_ref = weakref.ref(self)

        def display_timer_callback():
            if script_ref():
                script_ref()._render_and_update_display()
        self._display_timer = Timer(callback=display_timer_callback, interval=1, repeat=True)
        self._display_timer.start()
        logger.info('Script Loaded')

    def disconnect(self):
        super().disconnect()
        self._display_timer.stop()
        self._display_timer = None
        logger.info('Script Unloaded')

    def setup(self):
        self.component_map['Dialog'] = DialogComponent()
        super().setup()
        self.component_map['Global_Modes'].selected_mode = 'standalone'
        self.__on_main_mode_changed.subject = self.component_map['Main_Modes']
        self.__on_shut_down_state_changed.subject = self.component_map['Firmware']
        self.__on_control_mode_changed.subject = self.component_map['Firmware']
        note_editor = self.component_map['Step_Sequence'].note_editor
        self.component_map['Instrument'].set_note_editor(note_editor)
        self.component_map['Device'].set_note_editor(note_editor)

        def set_button_pressed_color(component_name, button_name):
            button_control = getattr(self.component_map[component_name], button_name)
            button_control.pressed_color = 'DefaultButton.Pressed'
        set_button_pressed_color('Transport', 'metronome_button')
        set_button_pressed_color('Accent', 'accent_button')

    def on_identified(self, response_bytes):
        super().on_identified(response_bytes)
        logger.info('Script Identified')
        for entry in midi.extract_identity_response_info(response_bytes):
            logger.info(entry)

    def identification_state_changed(self, state):
        if state:
            self.elements.display.initialize()
        else:
            self.elements.display.soft_disconnect()
        self.__on_control_mode_changed(self.component_map['Firmware'].in_control_surface_mode)

    def target_track_changed(self, _):
        self._update_note_mode()

    def drum_group_changed(self, _):
        self._update_note_mode()

    def sliced_simpler_changed(self, _):
        self._update_note_mode()

    @listens('in_control_surface_mode')
    def __on_control_mode_changed(self, in_control_surface_mode):
        enabled = in_control_surface_mode and self._identification.is_identified
        if enabled:
            self.component_map['Firmware'].initialize()
            self.component_map['Global_Modes'].selected_mode = 'default'
            self.component_map['Menu_Modes'].selected_mode = 'default'
            self.__on_main_mode_changed(self.component_map['Main_Modes'].selected_mode)
            self.refresh_state()
        else:
            self.component_map['Firmware'].reset()
            self.component_map['Global_Modes'].selected_mode = 'standalone'
            self.set_can_auto_arm(False)
            self.set_can_update_controlled_track(False)
        self._session_ring.set_enabled(enabled)

    @listens('shut_down_state')
    def __on_shut_down_state_changed(self, state):
        if state == ShutDownState.in_progress:
            logger.info('Shutting Down')

    @listens('selected_mode')
    def __on_main_mode_changed(self, mode):
        self.set_can_auto_arm(mode == 'note')
        self.set_can_update_controlled_track(mode == 'note')
        self._update_note_mode()
        if mode == 'note':
            self._auto_arm.restore_auto_arm()

    def _update_note_mode(self):
        if self.component_map['Main_Modes'].selected_mode == 'note':
            note_mode = note_mode_for_track(self.component_map['Target_Track'].target_track, self.instrument_finder)
            self.component_map['Note_Modes'].selected_mode = note_mode
            pitch_provider = PITCH_PROVIDERS.get(note_mode, None)
            self.component_map['Step_Sequence'].set_pitch_provider(self.component_map[pitch_provider] if pitch_provider else None)

    def _get_additional_dependencies(self):
        note_layout = self.register_disconnectable(NoteLayout(preferences=self.preferences))
        note_repeat = self.register_disconnectable(NoteRepeatModel(note_repeat=self._c_instance.note_repeat))
        quantization_strength = self.register_disconnectable(QuantizationStrength(preferences=self.preferences))
        sequencer_clip = self.register_disconnectable(SequencerClip(target_track=self._target_track))
        self.component_map['Firmware'] = FirmwareComponent()
        self.component_map['Volume_Parameters'] = VolumeParametersComponent()
        return {'firmware': const(self.component_map['Firmware']), 'grid_resolution': const(GridResolutionComponent(resolutions=GRID_RESOLUTIONS, default_index=DEFAULT_GRID_RESOLUTION_INDEX)), 'note_layout': const(note_layout), 'note_repeat': const(note_repeat), 'quantization_strength': const(quantization_strength), 'sequencer_clip': const(sequencer_clip), 'volume_parameters': const(self.component_map['Volume_Parameters'])}