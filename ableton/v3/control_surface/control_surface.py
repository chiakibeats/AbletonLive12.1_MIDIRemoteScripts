# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\control_surface.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from contextlib import contextmanager, nullcontext
from ableton.v2.control_surface import SimpleControlSurface
from ..base import const, find_if, inject, lazy_attribute, listens
from ..live import is_song_recording, is_track_armed, liveobj_valid
from . import CompoundElement, DeviceBankRegistry, NotifyingControlElement
from .components import BackgroundComponent, DrumGroupComponent, SessionComponent, SlicedSimplerComponent, ViewControlComponent
from .consts import M4L_PRIORITY
from .control_surface_mapping import ControlSurfaceMappingMixin
from .display import Display, Renderable, State
from .display.view.util import suppress_notifications
from .identification import IdentificationComponent
from .instrument_finder import InstrumentFinderComponent
from .layer import Layer
from .session_ring_selection_linking import SessionRingSelectionLinking

def create_control_surface(name=None, specification=None, c_instance=None):
    pass
    return type(name, (ControlSurface,), {})(specification, c_instance=c_instance)

class ControlSurface(SimpleControlSurface, ControlSurfaceMappingMixin):
    pass

    def __init__(self, specification=None, *a, **k):
        pass

    def disconnect(self):
        if self.specification.send_goodbye_messages_last:
            super().disconnect()
            self._send_specification_messages(messages_name='goodbye_messages')
        else:
            self._send_specification_messages(messages_name='goodbye_messages')
            super().disconnect()
        self.specification = None
        self.elements = None
        self.device_provider = None
        self.device_bank_registry = None
        self.instrument_finder = None
        self.session_ring_selection_linking = None
        self._drum_group_component = None
        self._sliced_simpler_component = None

    @property
    def renderable_components(self):
        pass
        return tuple((comp for comp in self._components if isinstance(comp, Renderable)))

    @property
    def controls(self):
        pass
        return [control for control in self._controls if not control.is_private]

    def port_settings_changed(self):
        pass
        if self._identification:
            self._identification.request_identity()
            return
        else:
            self._send_specification_messages()
            self.refresh_state()

    def on_identified(self, response_bytes):
        pass
        self._send_specification_messages()
        self.refresh_state()

    def refresh_state(self):
        pass
        super().refresh_state()
        if self.specification.feedback_channels is not None:
            self._c_instance.set_feedback_channels(self.specification.feedback_channels)
        self.__on_target_track_changed()
        self._update_feedback_velocity()

    def can_lock_to_devices(self):
        pass
        return self.device_provider is not None

    def lock_to_device(self, device):
        pass

    def unlock_from_device(self, _):
        pass

    def restore_bank(self, bank_index):
        pass

    def identification_state_changed(self, state):
        return

    def target_track_changed(self, target_track):
        return

    def drum_group_changed(self, drum_group):
        return

    def sliced_simpler_changed(self, sliced_simpler):
        return

    def set_can_update_controlled_track(self, can_update):
        pass
        self._can_update_controlled_track = can_update
        self._update_controlled_track()

    def set_can_auto_arm(self, can_auto_arm):
        pass
        self._can_enable_auto_arm = can_auto_arm
        self._update_auto_arm()

    def update(self):
        super().update()
        if self.display:
            self.display.clear_content_cache()
            return

    def update_display(self):
        super().update_display()
        self._render_and_update_display()

    def react(self, event):
        if self.display:
            self.display.react(event)

    @staticmethod
    def mxd_grab_control_priority():
        pass
        return M4L_PRIORITY

    def _render_and_update_display(self):
        pass

    def _suppress_notifications(self):
        if self.display:
            suppress_notifications(self.display.state)

    @staticmethod
    def _should_include_element_in_background(element):
        pass
        return True

    def _get_additional_dependencies(self):
        return

    def _on_entering_component_guard(self):
        return

    def _send_specification_messages(self, messages_name='hello_messages'):
        for msg in getattr(self.specification, messages_name) or []:
            self._send_midi(msg)
        return None

    @contextmanager
    def _component_guard(self):
        if False:
            yield
        pass

    @staticmethod
    def _create_elements(specification):
        return specification.elements_type()

    def _create_background(self, priority):
        layer_dict = {c.name: c for c in self._controls if isinstance(c, NotifyingControlElement) and (not isinstance(c, CompoundElement)) and self._should_include_element_in_background(c)}
        layer_dict['priority'] = priority
        background = BackgroundComponent(is_enabled=False, layer=Layer(**layer_dict))
        background.set_enabled(True)
        return background

    def _create_identification(self, specification):
        identification = IdentificationComponent(identity_request=specification.identity_request, identity_request_delay=specification.identity_request_delay, identity_response_id_bytes=specification.identity_response_id_bytes, custom_identity_response=specification.custom_identity_response)
        self.__on_is_identified_changed.subject = identification
        return identification

    def _create_instrument_finder(self):
        if self.instrument_finder is None:
            self.instrument_finder = InstrumentFinderComponent()
            self.__on_instrument_changed.subject = self.instrument_finder
        return self.instrument_finder

    @lazy_attribute
    def _create_session_ring(self):
        self._session_ring = self.specification.session_ring_component_type(is_enabled=False, num_tracks=self.specification.num_tracks, num_scenes=self.specification.num_scenes, include_returns=self.specification.include_returns, include_master=self.specification.include_master, right_align_non_player_tracks=self.specification.right_align_non_player_tracks, snap_track_offset=self.specification.snap_track_offset)
        return self._session_ring

    @lazy_attribute
    def _create_device_provider(self):
        self.device_provider = self.register_disconnectable(self.specification.device_provider_type(song=self.song))
        self.device_provider.update_device_selection()
        return self.device_provider

    @lazy_attribute
    def _create_device_bank_registry(self):
        self.device_bank_registry = self.register_disconnectable(DeviceBankRegistry())
        return self.device_bank_registry

    def _create_extended_injector(self):
        inject_dict = {'full_velocity': const(self._c_instance.full_velocity), 'target_track': const(self._target_track), 'session_ring': lambda: self._create_session_ring, 'device_provider': lambda: self._create_device_provider, 'device_bank_registry': lambda: self._create_device_bank_registry, 'toggle_lock': const(self._c_instance.toggle_lock), 'playhead': const(self._c_instance.playhead)}
        inject_dict.update(self._get_additional_dependencies() or {})
        return inject(**inject_dict).everywhere()

    def _create_feedback_related_listeners(self):
        self.register_slot(self.song, self._update_feedback_velocity, 'session_record')
        self.register_slot(self.song, self._update_feedback_velocity, 'record_mode')

    def _register_component(self, component):
        super()._register_component(component)
        if isinstance(component, DrumGroupComponent):
            self._drum_group_component = component
            self._create_instrument_finder()
        if isinstance(component, SlicedSimplerComponent):
            self._sliced_simpler_component = component
            self._create_instrument_finder()
        if isinstance(component, ViewControlComponent):
            link_to_tracks = self.specification.link_session_ring_to_track_selection
            link_to_scenes = self.specification.link_session_ring_to_scene_selection
            if link_to_tracks or link_to_scenes:
                self.session_ring_selection_linking = self.register_disconnectable(SessionRingSelectionLinking(selection_changed_notifier=component, link_to_track_selection=link_to_tracks, link_to_scene_selection=link_to_scenes))
                return
        else:
            return

    def _update_feedback_velocity(self):
        track = self._target_track.target_track
        if is_song_recording() and is_track_armed(track):
            feedback_velocity = self.specification.recording_feedback_velocity
        else:
            feedback_velocity = self.specification.playing_feedback_velocity
        self._c_instance.set_feedback_velocity(int(feedback_velocity))
        self._c_instance.playhead.velocity = int(feedback_velocity)

    def _update_controlled_track(self):
        if self._can_update_controlled_track:
            self.set_controlled_track(self._target_track.target_track)
        else:
            self.release_controlled_track()

    def _update_auto_arm(self):
        if self._auto_arm:
            self._auto_arm.set_enabled(self._identification.is_identified and self._can_enable_auto_arm)

    def _update_instrument_components(self):
        self._update_controlled_track()
        if self._drum_group_component:
            drum_group = self.instrument_finder.drum_group
            self._drum_group_component.set_drum_group_device(drum_group)
            self.drum_group_changed(drum_group)
        if self._sliced_simpler_component:
            sliced_simpler = self.instrument_finder.sliced_simpler
            self._sliced_simpler_component.set_simpler_device(sliced_simpler)
            self.sliced_simpler_changed(sliced_simpler)

    @listens('target_track')
    def __on_target_track_changed(self):
        track = self._target_track.target_track
        self.__on_track_arm_changed.subject = track
        self.__on_track_implicit_arm_changed.subject = track
        self._update_controlled_track()
        self.target_track_changed(track)

    @listens('arm')
    def __on_track_arm_changed(self):
        self._update_feedback_velocity()

    @listens('implicit_arm')
    def __on_track_implicit_arm_changed(self):
        self._update_feedback_velocity()

    @listens('instrument')
    def __on_instrument_changed(self):
        self._update_instrument_components()

    @listens('is_identified')
    def __on_is_identified_changed(self, is_identified):
        if is_identified:
            self.on_identified(self._identification.received_response_bytes)
        if self._can_enable_session_ring:
            self._session_ring.set_enabled(is_identified)
        self._update_auto_arm()
        self.identification_state_changed(self._identification.is_identified)