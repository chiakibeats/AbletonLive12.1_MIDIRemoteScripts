# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\FANTOM\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.components import DEFAULT_DRUM_TRANSLATION_CHANNEL
from ableton.v3.control_surface.legacy_bank_definitions import best_of_banks
from . import sysex
from .colors import Rgb, Skin
from .elements import NUM_SCENES, NUM_TRACKS, Elements
from .mappings import create_mappings
from .mixer import MixerComponent
from .session import SessionComponent
from .transport import TransportComponent

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410, product_ids=[544, 643], model_name=['FANTOM-6 7 8', 'FANTOM-06 07 08']), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT, REMOTE])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return FANTOM(specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = NUM_TRACKS
    num_scenes = NUM_SCENES
    include_returns = True
    feedback_channels = [DEFAULT_DRUM_TRANSLATION_CHANNEL]
    playing_feedback_velocity = Rgb.GREEN.midi_value
    recording_feedback_velocity = Rgb.RED.midi_value
    custom_identity_response = sysex.REFRESH_REQUEST
    identity_request = sysex.INITIATE_CONNECTION
    identity_request_delay = 10.0
    goodbye_messages = (sysex.TERMINATE_CONNECTION,)
    create_mappings_function = create_mappings
    parameter_bank_definitions = best_of_banks()
    component_map = {'Mixer': MixerComponent, 'Session': SessionComponent, 'Transport': TransportComponent}

class FANTOM(ControlSurface):

    def setup(self):
        super().setup()
        self.set_can_update_controlled_track(True)