# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Keystage\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import BasicColors, ControlSurface, ControlSurfaceSpecification, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START
from .display import display_specification
from .elements import Elements
from .mappings import create_mappings

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2372, product_ids=[537], model_name=['Keystage']), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return Keystage(specification=Specification, c_instance=c_instance)

def make_sysex_header(response_bytes):
    return (SYSEX_START, 66, 64 + response_bytes[0], 0, 1, 105, response_bytes[6])

def make_connection_message(connect=True):
    return (2, 0, 0, 111, int(connect), SYSEX_END)

class Skin:

    class Transport:
        StopOn = BasicColors.OFF
        StopPressed = BasicColors.ON

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin)
    identity_response_id_bytes = (66, 105, 1)
    create_mappings_function = create_mappings
    include_auto_arming = True
    display_specification = display_specification

class Keystage(ControlSurface):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._sysex_header = None
        self.set_can_auto_arm(True)

    def disconnect(self):
        if self._sysex_header:
            self._send_midi(self._sysex_header + make_connection_message(connect=False))
        super().disconnect()

    def on_identified(self, response_bytes):
        super().on_identified(response_bytes)
        self._sysex_header = make_sysex_header(response_bytes)
        self._send_midi(self._sysex_header + make_connection_message())
        if not hasattr(self.elements, 'main_display_lines'):
            self.elements.add_display_lines(self._sysex_header)