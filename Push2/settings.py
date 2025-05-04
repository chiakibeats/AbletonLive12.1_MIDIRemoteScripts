# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\settings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from pushbase.setting import OnOffSetting

def create_settings(preferences=None):
    preferences = preferences if preferences is not None else {}
    return {'workflow': OnOffSetting(name='Workflow', value_labels=['Scene', 'Clip'], default_value=True, preferences=preferences), 'aftertouch_mode': OnOffSetting(name='Pressure', value_labels=['Mono', 'Polyphonic'], default_value=True, preferences=preferences)}