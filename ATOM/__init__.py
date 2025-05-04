# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from functools import partial
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import ArmedTargetTrackComponent, TranslatingBackgroundComponent
from ableton.v3.live import liveobj_valid
from . import midi
from .colors import Rgb
from .drum_group import DrumGroupComponent
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .keyboard import KeyboardComponent
from .mappings import create_mappings
from .skin import Skin

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479, product_ids=[518], model_name=['ATOM']), PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return ATOM(specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    target_track_component_type = ArmedTargetTrackComponent
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    identity_request = midi.NATIVE_MODE_ON_MESSAGE
    custom_identity_response = (191, 127, 127)
    goodbye_messages = (midi.NATIVE_MODE_OFF_MESSAGE,)
    create_mappings_function = create_mappings
    component_map = {'Drum_Group': partial(DrumGroupComponent, translation_channel=midi.DRUM_CHANNEL), 'Keyboard': partial(KeyboardComponent, midi.KEYBOARD_CHANNEL), 'Translating_Background': partial(TranslatingBackgroundComponent, translation_channel=midi.USER_CHANNEL)}

class ATOM(ControlSurface):

    def port_settings_changed(self):
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)
        super().port_settings_changed()

    def drum_group_changed(self, drum_group):
        self.component_map['Note_Modes'].selected_mode = 'drum' if liveobj_valid(drum_group) else 'keyboard'