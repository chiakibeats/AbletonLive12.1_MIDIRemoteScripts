# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Keystage\mappings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

def create_mappings(_):
    mappings = {}
    mappings['Transport'] = dict(play_button='play_button', stop_button='stop_button', loop_button='loop_button', tap_tempo_button='tempo_button', metronome_button='metronome_button', rewind_button='rewind_button', fastforward_button='fastforward_button')
    mappings['View_Based_Recording'] = dict(record_button='record_button')
    mappings['Undo_Redo'] = dict(undo_button='undo_button')
    mappings['View_Control'] = dict(prev_track_button='up_button', next_track_button='down_button')
    mappings['Device'] = dict(parameter_controls='knobs')
    return mappings