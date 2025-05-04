# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from typing import Optional
from Live.DeviceParameter import ParameterState
from Live.Track import Track
from ableton.v3.control_surface import RelativeInternalParameter
from ableton.v3.control_surface.display import DefaultNotifications, DisplaySpecification, State, view
from ableton.v3.live import display_name, liveobj_name, normalized_parameter_value, parameter_owner, song
from .display_util import AUTOMATION_CHAR, ELLIPSIS_CHAR, Content, HorizontalAlignment, HorizontalListContent, NotificationContent, get_mode_select_notification, on_off_to_title_case, parameter_value_string
from .firmware import ShutDownState
from .note_repeat import REPEAT_RATE_MAP
from .transport import GROOVE_POOL_EMPTY

class Notifications(DefaultNotifications):
    full_velocity = DefaultNotifications.TransformDefaultText(on_off_to_title_case)
    note_repeat = 'Repeat\nOff'
    generic = DefaultNotifications.DefaultText()

    class Element(DefaultNotifications.Element):
        button_lock = DefaultNotifications.TransformDefaultText(lambda text: text.replace(' Button', ''))

    class Clipboard(DefaultNotifications.Clipboard):
        INCLUDE_ALL = True

    class UndoRedo(DefaultNotifications.UndoRedo):
        INCLUDE_ALL = True

    class Transport(DefaultNotifications.Transport):
        metronome = DefaultNotifications.TransformDefaultText(on_off_to_title_case)
        midi_capture = DefaultNotifications.DefaultText()

    class Recording(DefaultNotifications.Recording):
        new = DefaultNotifications.DefaultText()

    class Automation(DefaultNotifications.Automation):
        INCLUDE_ALL = True

    class Scene(DefaultNotifications.Scene):
        INCLUDE_ALL = True

    class Track(DefaultNotifications.Track):
        INCLUDE_ALL = True

    class Clip(DefaultNotifications.Clip):
        INCLUDE_ALL = True
        quantize = '{} {}%\nquantized'.format

    class Device(DefaultNotifications.Device):
        on_off = DefaultNotifications.TransformDefaultText(on_off_to_title_case)
        fold = DefaultNotifications.DefaultText()

    class DrumGroup(DefaultNotifications.DrumGroup):
        INCLUDE_ALL = True

        class Pad(DefaultNotifications.DrumGroup.Pad):
            INCLUDE_ALL = True
            select = ''

    class Simpler(DefaultNotifications.Simpler):
        INCLUDE_ALL = True

    class Notes(DefaultNotifications.Notes):
        INCLUDE_ALL = True

    class Sequence(DefaultNotifications.Sequence):
        INCLUDE_ALL = True

    class Modes(DefaultNotifications.Modes):
        select = lambda _, mode: get_mode_select_notification(mode)

def in_critical_display_state(state):
    return state.active_parameter.parameter is not None or state.firmware.shut_down_state != ShutDownState.none or state.dialog.any_dialog_open

def create_root_view() -> view.View[Optional[Content]]:

    @view.View
    def modifier_view(state: State) -> Optional[Content]:
        if state.track_list.mute_button.is_held:
            return Content.with_loop_overview(state, lines=['Mute...'])
        elif state.track_list.delete_button.is_held:
            return Content.with_loop_overview(state, lines=['Delete...'])
        elif state.session.clipboard.any_clipboard_has_content:
            return Content.with_loop_overview(state, lines=['Paste...'])
        elif state.track_list.duplicate_button.is_held:
            return Content.with_loop_overview(state, lines=['Copy...'])
        else:
            return None

    def menu_view(state: State) -> Optional[Content]:
        if state.menu_modes.menu_content:
            return state.menu_modes.menu_content
        elif state.menu_modes.selected_mode == 'tempo_menu':
            return HorizontalListContent.with_loop_overview(state, lines=['Tempo', state.transport.tempo_string])
        elif state.menu_modes.selected_mode == 'groove_menu':
            return HorizontalListContent.with_loop_overview(state, lines=state.transport.groove_string.split('\n'), draw_border=state.transport.groove_string != GROOVE_POOL_EMPTY)
        elif state.menu_modes.selected_mode == 'loop_menu':
            return HorizontalListContent.with_loop_overview(state, lines=['Loop Length', state.loop_length.length_string], draw_border=state.loop_length.length_string != ELLIPSIS_CHAR)
        elif state.menu_modes.selected_mode == 'note_repeat_menu':
            return HorizontalListContent.with_loop_overview(state, lines=['Repeat Rate', '{}'.format(REPEAT_RATE_MAP[state.note_repeat.model.rate])])
        else:
            return None

    @view.View
    def parameter_view(state: State) -> Optional[Content]:
        active_parameter = state.active_parameter.parameter
        if active_parameter:
            is_relative_internal = isinstance(active_parameter, RelativeInternalParameter)
            if is_relative_internal and active_parameter.name == 'Velocity':
                return Content.with_loop_overview(state, lines=[display_name(active_parameter), str(active_parameter)])
            else:
                owner = parameter_owner(active_parameter)
                if owner == song().master_track:
                    return Content(lines=['Volume', '', ''], horizontal_alignment=HorizontalAlignment.LEFT, value=normalized_parameter_value(active_parameter), fill_value=False, left_meter=song().master_track.output_meter_left, right_meter=song().master_track.output_meter_right)
                else:
                    parameter_name = 'Track Volume' if isinstance(owner, Track) else display_name(active_parameter)
                    value_string = state.parameter_automation.envelope_value_string or parameter_value_string(active_parameter)
                    if active_parameter.state != ParameterState.enabled:
                        return Content(lines=[parameter_name, 'Disabled', value_string], horizontal_alignment=HorizontalAlignment.LEFT)
                    else:
                        return Content(lines=[parameter_name, '', '{}{}'.format(AUTOMATION_CHAR if active_parameter.automation_state == 1 else '', value_string)], horizontal_alignment=HorizontalAlignment.LEFT, value=None if is_relative_internal else normalized_parameter_value(active_parameter, value=state.parameter_automation.envelope_value))

    @view.View
    def main_view(state: State) -> Optional[Content]:
        if state.firmware.shut_down_state == ShutDownState.requested:
            return Content(lines=['Press wheel to', 'shut down'])
        elif state.dialog.any_dialog_open:
            return Content(lines=['Live is showing a dialog that needs your attention.'])
        elif state.note_settings_modes.selected_mode == 'active' and state.note_settings.can_display_duration:
            return HorizontalListContent.with_loop_overview(state, lines=['Note Length', state.note_settings.duration_range_string])
        else:
            return HorizontalListContent.with_loop_overview(state, lines=[liveobj_name(state.target_track.target_track), liveobj_name(state.device.device) or 'No Device'], draw_border=state.device_navigation.scroll_encoder.enabled)
    return view.CompoundView(view.DisconnectedView(), view.NotificationView(lambda state, line: NotificationContent.with_loop_overview(state, lines=[line]), render_condition=lambda state, notification: not in_critical_display_state(state) or 'automation' in notification.lower(), supports_new_line=True), modifier_view, view.View(menu_view, render_condition=lambda state: not in_critical_display_state(state) and state.note_settings_modes.selected_mode != 'active'), parameter_view, main_view)

def protocol(elements):

    def display(content: Optional[Content]):
        elements.display.display_message(content or Content(lines=['']))
    return display
display_specification = DisplaySpecification(create_root_view=create_root_view, protocol=protocol, notifications=Notifications)