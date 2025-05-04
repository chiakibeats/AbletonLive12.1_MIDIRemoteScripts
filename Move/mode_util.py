# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\mode_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.components import create_sequencer_clip
from ableton.v3.control_surface.mode import EventDescription, ModeButtonBehaviour, toggle_mode_on_property_change
from ableton.v3.live import liveobj_valid

def create_clip(control_surface):
    pass
    track = control_surface.component_map['Target_Track'].target_track
    clip = control_surface.component_map['Target_Track'].target_clip
    if liveobj_valid(clip) or track.has_midi_input:
        create_sequencer_clip(track)

def close_menus(control_surface):
    pass

    def inner(modes_comp, mode_name):

        def on_event(*_):
            modes_comp.selected_mode = mode_name

        def on_clip_changed():
            if modes_comp.selected_mode == 'loop_menu' and (not liveobj_valid(control_surface.component_map['Target_Track'].target_clip)):
                modes_comp.selected_mode = mode_name
        modes_comp.register_slot(control_surface.component_map['Main_Modes'], on_event, 'selected_mode')
        modes_comp.register_slot(control_surface.song.view, on_event, 'selected_track')
        modes_comp.register_slot(control_surface.component_map['Track_List'], on_event, 'track_reselected')
        modes_comp.register_slot(control_surface.component_map['Target_Track'], on_clip_changed, 'target_clip')
    return inner

def activate_note_settings(control_surface):
    pass
    note_editor = control_surface.component_map['Step_Sequence'].note_editor

    def inner(modes, mode_name):

        def on_event(*_):
            if not note_editor.active_steps:
                modes.pop_mode(mode_name)
                return
            elif modes.selected_mode != mode_name:
                modes.push_mode(mode_name)
                return
            else:
                return None
        modes.register_slot(note_editor, on_event, 'active_steps')
    return inner

def toggle_shut_down_mode(control_surface):
    pass
    return toggle_mode_on_property_change(EventDescription(subject=control_surface.component_map['Firmware'], event_name='shut_down_state'), return_to_default=True)

def toggle_dialog_mode(control_surface):
    pass
    return toggle_mode_on_property_change(EventDescription(subject=control_surface.component_map['Dialog'], event_name='any_dialog_open'), return_to_default=True)

def toggle_notification_suppression_mode(control_surface):
    pass
    return toggle_mode_on_property_change(EventDescription(subject=control_surface.display_state, event_name='notification_visible'), return_to_default=True)

def toggle_note_repeat_menu(control_surface):
    pass
    return toggle_mode_on_property_change(EventDescription(subject=control_surface.component_map['Note_Repeat'], event_name='enabled_state_toggled_by_button'), return_to_default=True)

class MenuBehaviour(ModeButtonBehaviour):
    pass

    def press_immediate(self, component, mode):
        if component.selected_mode == mode:
            component.go_back(to_top=True)
            return
        else:
            component.push_mode(mode)

class MenuWithLatchingBehavior(MenuBehaviour):
    pass

    def release_delayed(self, component, _):
        component.push_mode(component.modes[0])
        component.pop_unselected_modes()