# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\capabilities.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

GENERIC_SCRIPT_KEY = 'generic_script'
PORTS_KEY = 'ports'
CONTROLLER_ID_KEY = 'controller_id'
TYPE_KEY = 'surface_type'
FIRMWARE_KEY = 'firmware_version'
AUTO_LOAD_KEY = 'auto_load'
SUGGESTED_PORT_NAMES_KEY = 'suggested_port_names'
VENDORID = 'vendor_id'
PRODUCTIDS = 'product_ids'
MODEL_NAMES = 'model_names'
DIRECTIONKEY = 'direction'
PORTNAMEKEY = 'name'
MACNAMEKEY = 'mac_name'
PROPSKEY = 'props'
HIDDEN = 'hidden'
SYNC = 'sync'
SCRIPT = 'script'
NOTES_CC = 'notes_cc'
REMOTE = 'remote'
PLAIN_OLD_MIDI = 'plain_old_midi'

def __create_port_dict(direction, port_name, mac_name, props):
    if props:
        for prop in props:
            pass
    capabilities = {DIRECTIONKEY: direction, PORTNAMEKEY: port_name, PROPSKEY: props}
    if mac_name:
        capabilities[MACNAMEKEY] = mac_name
    return capabilities

def inport(port_name='', props=[], mac_name=None):
    pass
    return __create_port_dict('in', port_name, mac_name, props)

def outport(port_name='', props=[], mac_name=None):
    pass
    return __create_port_dict('out', port_name, mac_name, props)

def controller_id(vendor_id, product_ids, model_name):
    pass
    for product_id in product_ids:
        pass
    model_names = model_name if type(model_name) is list else [model_name]
    return {VENDORID: vendor_id, PRODUCTIDS: product_ids, MODEL_NAMES: model_names}