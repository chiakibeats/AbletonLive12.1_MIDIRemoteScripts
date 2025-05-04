# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\mappings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.control_surface.mode import LatchingBehaviour

def create_mappings(_):
    mappings = {}
    mappings['Modifier_Background'] = dict(shift='shift_button')
    mappings['Undo_Redo'] = dict(undo_button='stop_button_with_shift')
    mappings['Session_Navigation'] = dict(up_button='up_button_with_shift', down_button='down_button_with_shift')
    mappings['View_Control'] = dict(next_track_button='right_button', prev_track_button='left_button', next_scene_button='down_button', prev_scene_button='up_button')
    mappings['View_Based_Recording'] = dict(record_button='record_button')
    mappings['Transport'] = dict(arrangement_position_encoder='display_encoder', tempo_coarse_encoder='display_encoder_with_shift', play_button='play_button', loop_button='play_button_with_shift', stop_button='stop_button', metronome_button='click_button', capture_midi_button='record_button_with_shift', prev_cue_button='display_left_button', next_cue_button='display_right_button')
    mappings['Lower_Pad_Modes'] = dict(enable=False, cycle_mode_button='minus_button', select=dict(component='Mixer', track_select_buttons='lower_pads'), stop=dict(component='Session', stop_track_clip_buttons='lower_pads'))
    mappings['Main_Modes'] = dict(default_behaviour=LatchingBehaviour(), song_button='song_mode_button', instrument_button='instrument_mode_button', editor_button='editor_mode_button', user_button='user_mode_button', instrument=dict(component='Device', parameter_controls='encoders'), song=dict(component='Lower_Pad_Modes'), editor=dict(component='View_Toggle', main_view_toggle_button='bank_a_button', browser_view_toggle_button='bank_b_button', detail_view_toggle_button='bank_d_button', crossfader_control='bank_h_button'), user=dict(component='Device', prev_button='encoders', next_button='display_buttons_raw[2]'), mappings=dict(component='Device_Navigation', encoders='display_buttons_raw[3]', prev_bank_button='display_buttons_raw[4]', next_bank_button='display_buttons_raw[5]'), Main_Modes=dict(component='Translating_Background', encoders='encoders', channel_selection_buttons='display_buttons'))
    return mappings