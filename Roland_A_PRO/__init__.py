# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_A_PRO\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .Roland_A_PRO import Roland_A_PRO

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410, product_ids=[271], model_name='A-PRO'), PORTS_KEY: [inport(props=[]), inport(props=[NOTES_CC, REMOTE]), inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[]), outport(props=[SCRIPT])]}

def create_instance(c_instance):
    return Roland_A_PRO(c_instance)