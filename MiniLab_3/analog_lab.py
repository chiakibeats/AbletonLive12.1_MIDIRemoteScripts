# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\analog_lab.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
import Live
from Live.Track import Track
from ableton.v3.base import SlotGroup, depends, listens
from ableton.v3.control_surface import Component, find_instrument_devices, find_instrument_meeting_requirement
from ableton.v3.live import is_track_armed, liveobj_valid
from .midi import ARTURIA_PROGRAM_CLEAR_SCREEN_MESSAGE, ARTURIA_PROGRAM_GENERIC_PARAMETER_FEEDBACK_MESSAGE
ANALOG_LAB_NAME_PREFIX = 'Analog Lab'

def tracks_with_analog_lab(song):
    return [track for track in song.tracks if has_analog_lab_instance(track)]

def has_analog_lab_instance(track):
    instance = find_instrument_meeting_requirement(lambda d: isinstance(d, Live.PluginDevice.PluginDevice) and d.name.startswith(ANALOG_LAB_NAME_PREFIX), track)
    return liveobj_valid(instance)

def track_can_receive_midi(track):
    return track.has_midi_input and (is_track_armed(track) or (track.current_monitoring_state == Track.monitoring_states.IN and (not track.is_frozen) and (track.current_monitoring_state != Track.monitoring_states.OFF)))

class AnalogLabComponent(Component):
    pass

    @depends(send_midi=None)
    def __init__(self, *a, send_midi=None, **k):
        super().__init__(*a, **k)
        self._send_midi = send_midi
        self.__on_tracks_changed.subject = self.song
        self._init_slot_groups()
        self._analog_lab_connected = False
        self.update()

    def _init_slot_groups(self):
        self._track_slot_groups = []
        for event in ['arm', 'implicit_arm', 'input_routing_type', 'current_monitoring_state', 'is_frozen']:
            self._track_slot_groups.append(self.register_disconnectable(SlotGroup(self.update, event)))
        self._rack_slot_group = self.register_disconnectable(SlotGroup(self.update, 'chains'))
        self._chain_slot_group = self.register_disconnectable(SlotGroup(self.update, 'devices'))

    @listens('tracks')
    def __on_tracks_changed(self):
        self.update()

    def update(self, *_):
        super().update()
        analog_lab_tracks = tracks_with_analog_lab(self.song)
        self._update_analog_lab_connected(analog_lab_tracks)
        self._update_listeners(analog_lab_tracks)

    def _update_listeners(self, analog_lab_tracks):
        pass
        for slot_group in self._track_slot_groups:
            slot_group.replace_subjects(analog_lab_tracks)
        racks, chains = ([], [])
        for track in analog_lab_tracks:
            devices = list(find_instrument_devices(track))
            racks.extend((d for d in devices if d.can_have_chains))
            chains.extend(chain([track], *[d.chains for d in racks]))
        self._rack_slot_group.replace_subjects(racks)
        self._chain_slot_group.replace_subjects(chains)

    def _update_analog_lab_connected(self, analog_lab_tracks):
        pass
        if analog_lab_tracks and any((track_can_receive_midi(t) for t in analog_lab_tracks)):
            self._analog_lab_connected = True
            return
        elif self._analog_lab_connected:
            self._analog_lab_connected = False
            self._disconnect_analog_lab()
            return

    def _disconnect_analog_lab(self):
        self._send_midi(ARTURIA_PROGRAM_CLEAR_SCREEN_MESSAGE)
        self._send_midi(ARTURIA_PROGRAM_GENERIC_PARAMETER_FEEDBACK_MESSAGE)