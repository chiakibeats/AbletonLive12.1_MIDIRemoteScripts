# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_mini_mk2\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.base import listens
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, HIDDEN, NOTES_CC, PORTS_KEY, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import DEFAULT_DRUM_TRANSLATION_CHANNEL
from .colors import Rgb, Skin
from .elements import PAD_MODE_HEADER, SYSEX_END, Elements
from .mappings import create_mappings

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[79], model_name=['APC mini mk2']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), inport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT, SYNC, HIDDEN]), outport(props=[NOTES_CC])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return APC_mini_mk2(specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = 8
    num_scenes = 8
    include_returns = True
    feedback_channels = [DEFAULT_DRUM_TRANSLATION_CHANNEL]
    playing_feedback_velocity = Rgb.GREEN.midi_value
    recording_feedback_velocity = Rgb.RED.midi_value
    identity_response_id_bytes = (71, 79, 0, 25)
    goodbye_messages = (PAD_MODE_HEADER + (0, SYSEX_END),)
    create_mappings_function = create_mappings

class APC_mini_mk2(ControlSurface):

    def setup(self):
        super().setup()
        self.__on_pad_mode_changed.subject = self.component_map['Pad_Modes']

    @staticmethod
    def _should_include_element_in_background(element):
        return 'Drum_Pad' not in element.name

    @listens('selected_mode')
    def __on_pad_mode_changed(self, selected_mode):
        is_drum_mode = selected_mode == 'drum'
        self.set_can_update_controlled_track(is_drum_mode)
        if is_drum_mode:
            self.refresh_state()