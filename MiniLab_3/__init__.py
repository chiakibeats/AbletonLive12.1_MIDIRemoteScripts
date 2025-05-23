# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .analog_lab import AnalogLabComponent
from .colors import Rgb, Skin
from .display import DisplayComponent
from .drum_group import DrumGroupComponent
from .elements import NUM_SCENES, NUM_TRACKS, Elements
from .mappings import create_mappings
from .midi import CONNECTION_MESSAGE, DISCONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE, SYSEX_START
from .transport import TransportComponent

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=7285, product_ids=[8715], model_name=['Minilab3']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), inport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return MiniLab_3(specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    link_session_ring_to_track_selection = True
    link_session_ring_to_scene_selection = True
    num_tracks = NUM_TRACKS
    num_scenes = NUM_SCENES
    identity_response_id_bytes = (0, 32, 107, 2, 0, 4)
    create_mappings_function = create_mappings
    hello_messages = (CONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE)
    goodbye_messages = (DISCONNECTION_MESSAGE,)
    component_map = {'Drum_Group': DrumGroupComponent, 'Transport': TransportComponent}

class MiniLab_3(ControlSurface):

    def setup(self):
        super().setup()
        AnalogLabComponent()
        display = DisplayComponent(self._identification, self.component_map['Transport'])
        display.shift_button.set_control_element(self.elements.shift_button)

    @staticmethod
    def _should_include_element_in_background(element):
        return 'Pad_Bank' not in element.name

    def _do_send_midi(self, midi_event_bytes):
        if midi_event_bytes[0] == SYSEX_START:
            super()._do_send_midi(midi_event_bytes)