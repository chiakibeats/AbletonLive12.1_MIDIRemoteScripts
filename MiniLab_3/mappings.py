# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\mappings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.mode import select_mode_for_main_view
from .midi import PAD_TRANSLATION_CHANNEL

def translate_pad_banks(cs):
    pass
    def inner():
        for pad in cs.elements.pad_bank_a_raw + cs.elements.pad_bank_b_raw:
            pad.set_channel(PAD_TRANSLATION_CHANNEL)
    return inner

def realign_encoder_values(cs):
    pass
    def inner():
        for encoder in cs.elements.encoders_raw:
            encoder.realign_value()
    return inner

def create_mappings(cs):
    return {'View_Based_Recording': dict(record_button='record_button'), 'Transport': dict(loop_button='loop_button', play_button='play_button', stop_button='stop_button', tap_tempo_button='tap_tempo_button'), 'Mixer': dict(target_track_arm_button='shifted_display_encoder_button', target_track_pan_control='pan_fader', target_track_send_a_control='send_a_fader', target_track_send_b_control='send_b_fader', target_track_volume_control='volume_fader'), 'View_Control': dict(modes=dict(component='View_Control', arrangement_position_encoder='display_encoder'), play_toggle_button=dict(component='Session', scene_0_launch_button='display_encoder_button')), 'Display_Modes': dict(modes=dict(component='firmware_element', mode_selection_control=translate_pad_banks(cs), user=dict(component='Session', clip_launch_buttons='pad_bank_a'), main=dict(component='Device', parameter_controls='encoders'))), 'Main_Modes': dict(mode_selection_control=dict(component='Drum_Group', mode_selection_control='pad_bank_b', user=dict(component='matrix', user=dict(component='Device',