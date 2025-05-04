# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.midi import CC_STATUS
from .display import display_specification
from .elements import Elements
from .focus_follow import FocusFollowComponent
from .launch_and_stop import LaunchAndStopComponent
from .mappings import create_mappings
from .midi import MIDI_CHANNEL
from .session_navigation import SessionNavigationComponent
from .skin import Skin
from .transport import TransportComponent
from .view_control import ViewControlComponent

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6092, product_ids=[8448], model_name=['KONTROL S49 MK3']), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return Komplete_Kontrol_S_Mk3(c_instance=c_instance, specification=Specification)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin)
    create_mappings_function = create_mappings
    display_specification = display_specification
    include_returns = True
    include_master = True
    snap_track_offset = True
    include_auto_arming = True
    identity_request = (MIDI_CHANNEL + CC_STATUS, 1, 0)
    custom_identity_response = (MIDI_CHANNEL + CC_STATUS, 1)
    goodbye_messages = ((MIDI_CHANNEL + CC_STATUS, 2, 0),)
    send_goodbye_messages_last = False
    component_map = {'Focus_Follow': FocusFollowComponent, 'Launch_And_Stop': LaunchAndStopComponent, 'Session_Navigation': SessionNavigationComponent, 'Transport': TransportComponent, 'View_Control': ViewControlComponent}

class Komplete_Kontrol_S_Mk3(ControlSurface):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.set_can_auto_arm(True)

    def identification_state_changed(self, state):
        self._set_mixer_enabled_state(state)

    def _set_mixer_enabled_state(self, enabled):
        pass