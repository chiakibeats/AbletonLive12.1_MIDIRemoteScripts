# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from functools import partial
from ableton.v3.base import listens
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import TranslatingBackgroundComponent
from ableton.v3.control_surface.legacy_bank_definitions import banked
from . import midi
from .colors import Rgb
from .display import display_specification
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .launch_and_stop import LaunchAndStopComponent
from .mappings import create_mappings
from .skin import Skin

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479, product_ids=[522], model_name=['ATM SQ']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return ATOMSQ(specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    display_specification = display_specification
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    link_session_ring_to_track_selection = True
    identity_response_id_bytes = midi.PRODUCT_ID_BYTES
    hello_messages = (midi.NATIVE_MODE_ON_MESSAGE,)
    goodbye_messages = (midi.NATIVE_MODE_OFF_MESSAGE,)
    create_mappings_function = create_mappings
    quantized_parameter_sensitivity = 0.3
    parameter_bank_definitions = banked()
    component_map = {'Launch_And_Stop': LaunchAndStopComponent, 'Translating_Background': partial(TranslatingBackgroundComponent, translation_channel=midi.USER_MODE_START_CHANNEL)}

class ATOMSQ(ControlSurface):

    def setup(self):
        super().setup()
        self.__on_main_modes_changed.subject = self.component_map['Main_Modes']
        self._update_firmware()

    def on_identified(self, response_bytes):
        self.schedule_message(1, self._update_firmware)
        super().on_identified(response_bytes)

    @listens('selected_mode')
    def __on_main_modes_changed(self, _):
        self._update_firmware()
        self.elements.track_name_display_command.clear_send_cache()
        self.elements.track_name_display.reset()
        self.elements.device_name_display_command.clear_send_cache()
        self.elements.device_name_display.reset()

    def _update_firmware(self):
        mode = self.component_map['Main_Modes'].selected_mode
        self.elements.lower_firmware_toggle_switch.send_value(bool(mode != 'song'))
        self.elements.upper_firmware_toggle_switch.send_value(bool(mode == 'instrument'))