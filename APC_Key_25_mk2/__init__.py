# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_Key_25_mk2\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.control_surface import ControlSurfaceSpecification, create_control_surface, create_skin
from ableton.v3.control_surface.capabilities import AUTO_LOAD_KEY, CONTROLLER_ID_KEY, HIDDEN, NOTES_CC, PORTS_KEY, SCRIPT, SYNC, controller_id, inport, outport
from .colors import Rgb, Skin
from .elements import Elements
from .mappings import create_mappings

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[78], model_name=['APC Key 25 mk2']), PORTS_KEY: [inport(props=[NOTES_CC]), inport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC]), outport(props=[NOTES_CC, SCRIPT, SYNC, HIDDEN])], AUTO_LOAD_KEY: True}

def create_instance(c_instance):
    return create_control_surface(name='APC_Key_25_mk2', specification=Specification, c_instance=c_instance)

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = 8
    num_scenes = 5
    include_returns = True
    identity_response_id_bytes = (71, 78, 0, 25)
    create_mappings_function = create_mappings