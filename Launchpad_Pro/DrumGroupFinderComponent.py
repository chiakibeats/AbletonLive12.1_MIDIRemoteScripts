# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\DrumGroupFinderComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import Subject, subject_slot, subject_slot_group
from _Framework.Util import find_if

class DrumGroupFinderComponent(ControlSurfaceComponent, Subject):
    pass
    __subject_events__ = ('drum_group',)
    _drum_group = None

    def __init__(self, target_track_component, layer=None, is_enabled=True, *a, **k):
        super(DrumGroupFinderComponent, self).__init__(*a, **k)
        self._target_track_component = target_track_component
        self._on_track_changed.subject = self._target_track_component
        self.update()

    @property
    def drum_group(self):
        pass
        return self._drum_group

    @property
    def root(self):
        pass
        return self._target_track_component.target_track

    @subject_slot_group('devices')
    def _on_devices_changed(self, chain):
        self.update()

    @subject_slot_group('chains')
    def _on_chains_changed(self, chain):
        self.update()

    @subject_slot('target_track')
    def _on_track_changed(self):
        self.update()

    def update(self):
        super(DrumGroupFinderComponent, self).update()
        if self.is_enabled():
            self._update_listeners()
            self._update_drum_group()

    def _update_listeners(self):
        root = self.root
        devices = list(find_instrument_devices(root))
        chains = list(chain([root], *[d.chains for d in devices]))
        self._on_chains_changed.replace_subjects(devices)
        self._on_devices_changed.replace_subjects(chains)

    def _update_drum_group(self):
        drum_group = find_drum_group_device(self.root)
        if type(drum_group) != type(self._drum_group) or drum_group != self._drum_group:
            self._drum_group = drum_group
        self.notify_drum_group()

def find_instrument_devices(track_or_chain):
    pass
    instrument = find_if(lambda d: d.type == Live.Device.DeviceType.instrument, track_or_chain.devices)
    if instrument and (not instrument.can_have_drum_pads) and instrument.can_have_chains:
        return chain([instrument], *map(find_instrument_devices, instrument.chains))
    else:
        return []

def find_drum_group_device(track_or_chain):
    pass
    instrument = find_if(lambda d: d.type == Live.Device.DeviceType.instrument, track_or_chain.devices)
    if instrument:
        if instrument.can_have_drum_pads:
            return instrument
        elif instrument.can_have_chains:
            return find_if(bool, map(find_drum_group_device, instrument.chains))
    return None