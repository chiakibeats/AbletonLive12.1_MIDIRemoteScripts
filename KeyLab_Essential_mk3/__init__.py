# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ableton.v3.base import listens
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.components import DeviceComponent
from MiniLab_3 import DrumGroupComponent
from .colors import Rgb, Skin
from .device_bank_toggle import DeviceBankToggleComponent
from .display import display_specification
from .elements import Elements
from .mappings import create_mappings
from .midi import CONNECTION_MESSAGE, DAW_PROGRAM_BYTE, DISCONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE
from .mixer import MixerComponent

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=7285, product_ids=[588, 652, 716], model_name=['KL Essential 49 mk3', 'KL Essential 61 mk3', 'KL Essential 88 mk3']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), inport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return KeyLab_Essential_mk3(specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = 4
    num_scenes = 2
    link_session_ring_to_track_selection = True
    link_session_ring_to_scene_selection = True
    identity_response_id_bytes = (0, 32, 107, 2, 0, 5)
    create_mappings_function = create_mappings
    hello_messages = (CONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE)
    goodbye_messages = (DISCONNECTION_MESSAGE,)
    component_map = {'Device': partial(DeviceComponent, bank_size=16, bank_navigation_component_type=DeviceBankToggleComponent), 'Drum_Group': DrumGroupComponent, 'Mixer': MixerComponent}
    display_specification = display_specification

class KeyLab_Essential_mk3(ControlSurface):

    def setup(self):
        super().setup()
        self.__on_firmware_program_changed.subject = self.elements.program_command

    @listens('value')
    def __on_firmware_program_changed(self, value):
        if value[0] == DAW_PROGRAM_BYTE:
            for encoder in self.elements.continuous_controls_raw:
                encoder.realign_value()
            self.elements.encoder_9.realign_value()