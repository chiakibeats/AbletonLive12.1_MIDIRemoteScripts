# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\mappings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.control_surface import HIGH_PRIORITY, LOW_PRIORITY, MOMENTARY_DELAY, NotifyingControlElement
from ableton.v3.control_surface.elements import SysexElement
from ableton.v3.control_surface.mode import DelayMode, MomentaryBehaviour, SetAttributeMode, ShowDetailClipMode
from .menu_modes import MenuModesComponent
from .mode_util import MenuBehaviour, MenuWithLatchingBehavior, activate_note_settings, close_menus, create_clip, toggle_dialog_mode, toggle_note_repeat_menu, toggle_notification_suppression_mode, toggle_shut_down_mode

def create_note_mode_layer_dict(component, include_mute=False, include_copy=False):
    layer_dict = dict(component=component, matrix='pads', select_button='shift_button', delete_button='delete_button', scroll_page_up_button='plus_button', scroll_page_down_button='minus_button', scroll_up_button='plus_button_with_shift', scroll_down_button='minus_button_with_shift')
    if include_mute:
        layer_dict['mute_button'] = 'mute_button'
    if include_copy:
        layer_dict['copy_button'] = 'duplicate_button'
    return layer_dict

def create_background_layer_dict(control_surface):
    layer = {'bg_{}'.format(c.name): c for c in vars(control_surface.elements).values() if not isinstance(c, NotifyingControlElement) or isinstance(c, SysexElement) or c.name!= 'Display'}
    layer['component'] = 'Background'
    layer['priority'] = HIGH_PRIORITY
    return layer

def create_mappings(control_surface):
    def component(component_name):
        return control_surface.component_map[component_name]
    mappings = {}
    mappings['Firmware'] = dict(power_state_control='power_state_element', control_mode_control='control_mode_element', led_brightness_control='led_brightness_element')
    mappings['Modifier_Background'] = dict(mute_button='mute_button', delete_button='delete_button')
    mappings['Track_List'] = dict(mute_button='mute_button', delete_button='delete_button', duplicate_button='duplicate_button', record_button='record_button')
    mappings['Accent'] = dict(accent_button='step_button_9_with_shift')
    mappings['Volume_Parameters'] = dict(volume_encoder='volume_encoder', volume_encoder_touch_button='encoder_touch_elements_raw[8]')
    mappings['Active_Parameter'] = dict(touch_controls='encoder_touch_elements')
    mappings['Device'] = dict(parameter_controls='encoders', parameter_touch_controls='parameter_touch_elements', delete_button='delete_button', mute_button='mute_button', shift_button='shift_button')
    mappings['Transport'] = dict(play_toggle_button='play_button', play_button='play_button_with_shift', metronome_button='step_button_5_with_shift')
    mappings['Recording'] = dict(record_button='record_button', new_button='step_button_13_with_shift')
    mappings['Undo_Redo'] = dict(undo_button='undo_button', redo_button='undo_button_with_shift')
    mappings['Note_Modes'] = dict(instrument=dict(create_note_mode_layer_dict('Instrument')), drum=dict(create_note_mode_layer_dict('Drum_Group', include_mute=True, include_copy=True)), simpler=dict(create_note_mode_layer_dict('Sliced_Simpler')), audio=dict(component='Background', bg_pads='pads', bg_step_buttons='step_buttons', bg_left_button='left_button', bg_right_button='right_button', bg_plus_button='plus_button', bg_down_button='minus_button', bg_loop_menu_button='loop_button'))
    mappings['Note_Settings_Modes'] = dict(is_private=True, inactive=lambda: component('Device').set_draws_automation(False), active=dict(modes=[lambda: component('Device').set_draws_automation(True), dict(component='Step_Sequence', duration_encoder='wheel', duration_encoder_touch='wheel_touch_button', nudge_left_button='left_button', nudge_right_button='right_button', transpose_up_button='plus_button', transpose_down_button='minus_button'), DelayMode((ShowDetailClipMode(control_surface.application), SetAttributeMode(component('Step_Sequence').note_settings, 'can_display_duration', True)), delay=MOMENTARY_DELAY)], selector=activate_note_settings(control_surface)))
    mappings['Session_Modes'] = dict(enable=False, is_private=True, cycle_mode_button='layout_button_with_shift', launch=dict(component='Session', clip_launch_buttons='pads_columns_0_thru_6', scene_launch_buttons='pads_column_7', select_button='shift_button', delete_button='delete_button', copy_button='duplicate_button'), session_overview=dict(component='Session_Overview', matrix='pads'))
    mappings['Main_Modes'] = dict(Clip_Actions='layout_button', delete_button=dict(component='Note_Modes'), step_button_15_with_shift=dict(component='Track_List', track_buttons='track_state_buttons', mute_track_button='mute_button'), note_copy_button=dict(component='Clip_Actions', delete_button='delete_button', quantize_button='step_button_15_with_shift', double_button='step_button_14_with_shift', duplicate_button='duplicate_button'), Menu_Modes=dict(component='Menu_Modes', loop_menu_button='loop_button'), modes=dict(component='Session_Navigation', up_button='plus_button', down_button='left_button', left_button='right_button', right_button='plus_button_with_shift', page_up_button='minus_button_with_shift', page_down_button='left_button_with_shift', page_left_button='right_button_with_shift', page_right_button='right_button_with_shift'), step_button_10_with_shift=dict(component='step_button_10_with_shift', step_button_10_with_shift='step_button_14_with_shift', step_button_15_with_shift='step_button_15_with_shift'))
    mappings['Menu_Modes'] = dict(is_private=True, default_behaviour=MenuBehaviour(), modes_component_type=MenuModesComponent, back_button='back_button', wheel_push_button='wheel_push_button', wheel='wheel', settings_menu_button='step_button_1_with_shift', workflow_menu_button='step_button_2_with_shift', tempo_menu_button='step_button_4_with_shift', groove_menu_button='step_button_6_with_shift', scale_menu_button=[dict(component='Transport', scroll_encoder='wheel', scroll_encoder_touch='shift_button'), dict(component='Step_Sequence', loop_buttons='step_buttons', loop_delete_button='delete_button', loop_copy_button='duplicate_button')], note_repeat_menu=dict(modes=[dict(component='Note_Repeat'), dict(component='Note_Repeat'), dict(component='Note_Repeat')], selector=workflow_menu_button(control_surface)), repeat_button=dict(component='on_color', behaviour=[dict(component='NoteRepeat.Menu'), dict(component='rate_encoder'), dict(component='toggle_note_repeat_menu', behaviour=[dict(component='mappings'), dict(component='Menu_Modes')]), dict(component='values',
    mappings['Global_Modes'] = dict(is_private=True, default=None, shut_down=dict(modes=[create_background_layer_dict(control_surface), dict(component='Firmware', confirm_shut_down_button='wheel_push_button', cancel_shut_down_button='back_button', priority=HIGH_PRIORITY)], selector=toggle_shut_down_mode(control_surface)), dialog=dict(create_background_layer_dict(control_surface), selector=toggle_dialog_mode(control_surface)), notification_suppression=dict(component='Notification_Suppression', suppress_button='back_button', selector=toggle_notification_suppression_mode(control_surface)), standalone=create_background_layer_dict(control_surface))
    mappings['Background_Modes'] = dict(is_private=True, shift_button='shift_button', default=dict(component='Transport', capture_midi_button='capture_button'), shift=dict(component='Background', bg_step_buttons='step_buttons', behaviour=MomentaryBehaviour()))
    return mappings