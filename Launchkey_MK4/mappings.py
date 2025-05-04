# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\mappings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import MOMENTARY_DELAY
from ableton.v3.control_surface.mode import EventDescription, ImmediateBehaviour, ShowDetailClipMode, make_reenter_behaviour, select_mode_on_event_change
from .display import cancel_temp_screens
from .launchkey_modes import LaunchkeyModesComponent
from .midi import SET_RELATIVE_ENCODER_MODE

def activate_note_settings(control_surface):
    pass
    note_editor = control_surface.component_map['Step_Sequence'].note_editor

    def inner(modes, mode_name):
        encoder_modes = control_surface.component_map['Main_Encoder_Modes']

        def on_event(*_):
            if not note_editor.active_steps:
                modes.pop_mode(mode_name)
                return
            else:  # inserted
                if modes.selected_mode!= mode_name and encoder_modes.selected_mode in ['mixer', 'plugin', 'sends', 'transport']:
                        modes.push_mode(mode_name, delay=MOMENTARY_DELAY)
                        return
        modes.register_slot(note_editor, on_event, 'active_steps')
    return inner

def set_playhead_enabled(control_surface, enabled):
    pass
    control_surface.component_map['Step_Sequence'].set_enabled(enabled)

def set_relative_encoder_mode(control_surface):
    pass
    return lambda: control_surface.send_midi(SET_RELATIVE_ENCODER_MODE)

def make_relative_encoder_mode_behavior(control_surface):
    pass
    return make_reenter_behaviour(ImmediateBehaviour, on_reenter=set_relative_encoder_mode(control_surface))

def create_launchkey_common_mappings(control_surface):
    pass
    mappings = {}
    mappings['View_Based_Recording'] = dict(record_button='record_button')
    mappings['Scale'] = dict(scale_type_control='scale_type_element', root_note_control='root_note_element')
    mappings['Keyboard'] = dict(matrix='keyboard')
    mappings['Encoder_Touch'] = dict(touch_controls='encoder_touch_elements')
    mappings['Lower_Pad_Modes'] = dict(enable=False, is_private=True, support_momentary_mode_cycling=False, cycle_mode_button='pad_function_button', clip_launch=None, stop=dict(component='Session', stop_track_clip_buttons='lower_pads'), mute=dict(component='Mixer', mute_buttons='lower_pads'), solo=dict(component='Mixer', solo_buttons='lower_pads'))
    mappings['Sequencer_Modes'] = dict(enable=False, is_private=True, support_momentary_mode_cycling=False, cycle_mode_button='scene_launch_button', default=dict(modes=dict(component='Step_Sequence', step_buttons='main_pads', prev_page_button='pad_up_button', next_page_button='pad_down_button', note_copy_button='pad_function_button', double_button='pad_down_button_with_pad_function'), selector=dict(component='Modifier_Background', pad_function_button='pad_function_button'), default=dict(component='Session_Navigation', up_button='pad_up_button', down_button='pad_down_button'), clip_select=lambda: set_playhead_enabled(control_surface, False), mappings=cancel_temp_screens(control_surface.elements))
    mappings['Daw_Pad_Modes'] = dict(enable=False, is_private=True, clip=dict(modes=[dict(component='Session', clip_launch_buttons='main_pads', scene_0_launch_button='scene_launch_button'), dict(component='Session_Navigation', up_button='pad_up_button', down_button='pad_down_button'), dict(component='Lower_Pad_Modes')]), sequencer=dict(component='Sequencer_Modes'))
    mappings['Main_Pad_Modes'] = dict(modes_component_type=LaunchkeyModesComponent, enable=False, is_private=True, mode_selection_control='pad_mode_element', null_0=None, null_1=None, daw=dict(component='Daw_Pad_Modes', behaviour=make_reenter_behaviour(on_reenter=ImmediateBehaviour, lambda: control_surface.component_map['Daw_Pad_Modes'].cycle_mode())), null_3=None, chord=None, custom_1=None, custom_2=None, custom_3=None, custom_4=None, null_9=None, null_10=None, null_11=None, null_12=None, arp=None, chord_map=None, drum=dict(component='Drum_Group', matrix='drum_pads', scroll_page_up_button='pad_up_button', scroll_page_down_button='pad_down_button'))
    mappings['Mixer_Encoder_Modes'] = dict(enable=False, is_private=True, level_button='encoder_up_button', pan_button='encoder_down_button', level=dict(component='Mixer', volume_controls='encoders'), pan=dict(component='Mixer', pan_controls='encoders'))
    mappings['Main_Encoder_Modes'] = dict(modes_component_type=LaunchkeyModesComponent, enable=False, is_private=True, mode_selection_control='encoder_mode_element', null_0=None, mixer=dict(modes=[dict(component='Mixer_Encoder_Modes'), set_relative_encoder_mode(control_surface)], behaviour=make_relative_encoder_mode_behavior(control_surface)), plugin=dict(modes=[dict(component='Device', parameter_controls='encoders', prev_bank_button='encoder_up_button', next_bank_button='encoder_down_button'), set_relative_encoder_mode(control_surface)], behaviour=make_relative_encoder_mode_behavior(control_surface)), null_3=dict(modes=[dict(component='Transport', arrangement_position_encoder='encoders_raw[0]', loop_start_encoder='encoders_raw[3]', loop_length_encoder='encoders_raw[4]', tempo_coarse_encoder='encoders_raw[7]', set_cue_button='encoder_up_button'), dict(component='Zoom', horizontal_zoom_encoder='encoders_raw[1]', vertical_zoom_encoder='encoders_raw[2]')]), sends=None, transport=None, custom_1=None, custom_2=None, custom_3=None, custom_4=None)
    mappings['Note_Settings_Modes'] = dict(is_private=True, inactive=lambda: control_surface.schedule_message(MOMENTARY_DELAY, cancel_temp_screens, control_surface.elements), active=dict(modes=[dict(component='Step_Sequence', encoders='encoders'), dict(component='Background', bg_encoder_up_button='encoder_up_button', bg_encoder_down_button='encoder_down_button'), ShowDetailClipMode(control_surface.application), lambda: control_surface.schedule_message(0.1, cancel_temp_screens, control_surface.elements)], selector=activate_note_settings(control_surface)))
    return mappings

def create_mappings(control_surface):
    pass
    mappings = create_launchkey_common_mappings(control_surface)
    mappings['Transport'] = dict(play_toggle_button='play_button', play_pause_button='play_button_with_shift', stop_button='stop_button', loop_button='loop_button', metronome_button='metronome_button', capture_midi_button='capture_button')
    mappings['Undo_Redo'] = dict(undo_button='undo_button', redo_button='undo_button_with_shift')
    mappings['Step_Sequence'] = dict(quantize_button='quantise_button')
    mappings['View_Control'] = dict(prev_track_button='track_left_button', next_track_button='track_right_button')
    mappings['Session_Navigation'] = dict(page_left_button='shifted_track_left_button', page_right_button='shifted_track_right_button')
    mappings['Volume_Mixer'] = dict(enable=False, volume_controls='faders', master_track_volume_control='master_fader')
    mappings['Fader_Button_Modes'] = dict(enable=False, is_private=True, support_momentary_mode_cycling=False, cycle_mode_button='fader_button_mode_button', arm=dict(component='Mixer', arm_buttons='fader_buttons'), select=dict(component='Mixer', track_select_buttons='fader_buttons'))
    return mappings