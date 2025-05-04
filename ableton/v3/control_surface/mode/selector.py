# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\mode\selector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import Any, NamedTuple, Optional
import Live
from . import pop_last_mode

def select_mode_for_main_view(main_view_name, can_select_now=True):
    pass
    return select_mode_on_event_change(EventDescription(subject=Live.Application.get_application().view, event_name='focused_document_view', event_state=main_view_name), can_select_now=can_select_now)

def select_mode_on_event_change(event_description, can_select_now=False):
    pass
    subject = _get_subject(event_description.subject)
    event_name = event_description.event_name
    event_state = event_description.event_state

    def inner(modes_component, mode_name):

        def on_event_changed(*_):
            if event_state is None or getattr(subject, event_name) == event_state:
                modes_component.selected_mode = mode_name
        modes_component.register_slot(subject, on_event_changed, event_name)
        if can_select_now and event_state is not None:
            on_event_changed()
    return inner
pass

def toggle_mode_on_property_change(event_description, return_to_default=False, can_select_now=False):
    pass
    subject = _get_subject(event_description.subject)
    event_name = event_description.event_name

    def inner(modes_component, mode_name):

        def on_property_changed(state=None):
            if bool(state or getattr(subject, event_name)):
                modes_component.push_mode(mode_name)
                return
            elif return_to_default and modes_component.selected_mode == mode_name:
                modes_component.push_mode(modes_component.modes[0])
                modes_component.pop_unselected_modes()
                return
            else:
                pop_last_mode(modes_component, mode_name)
        modes_component.register_slot(subject, on_property_changed, event_name)
        if can_select_now:
            on_property_changed(getattr(subject, event_name))
    return inner

def _get_subject(subject):
    return subject() if callable(subject) else subject

class EventDescription(NamedTuple):
    pass
    subject: Any
    event_name: str
    event_state: Optional[Any] = None