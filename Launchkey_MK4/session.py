# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\session.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import depends
from ableton.v3.control_surface.components import ClipSlotComponent as ClipSlotComponentBase
from ableton.v3.control_surface.components import SessionComponent as SessionComponentBase
from ableton.v3.control_surface.components import create_sequencer_clip
from ableton.v3.live import action, find_parent_track, liveobj_valid

def get_clip_for_slot(slot):
    pass
    if liveobj_valid(slot):
        track = find_parent_track(slot)
        if track.has_midi_input:
            return slot.clip if slot.has_clip else create_sequencer_clip(track, slot=slot)
    return None

class ClipSlotComponent(ClipSlotComponentBase):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.is_selecting = False

    def _on_launch_button_pressed(self):
        if self.is_selecting:
            self.parent.parent.select_slot(self._clip_slot)
            return
        else:
            super()._on_launch_button_pressed()

    def _feedback_value(self, track, slot_or_clip):
        value = super()._feedback_value(track, slot_or_clip)
        if self.is_selecting:
            is_midi = find_parent_track(slot_or_clip).has_midi_input
            if self._has_clip() or getattr(slot_or_clip, 'controls_other_clips', False):
                value = 'Session.SequencerClip' if is_midi else 'Session.ClipStopped'
            else:
                value = 'Session.SequencerSlot' if is_midi else 'Session.Slot'
        return value

class SessionComponent(SessionComponentBase):
    pass
    __events__ = ('clip_selected',)

    @depends(sequencer_clip=None)
    def __init__(self, sequencer_clip=None, *a, **k):
        super().__init__(*a, clip_slot_component_type=ClipSlotComponent, **k)
        self._sequencer_clip = sequencer_clip

    def set_clip_select_buttons(self, buttons):
        is_selecting = bool(buttons)
        for scene in self._scenes:
            for x in range(self._session_ring.num_tracks):
                scene.clip_slot(x).is_selecting = is_selecting
            continue
        super().set_clip_launch_buttons(buttons)

    def select_slot(self, slot):
        clip = get_clip_for_slot(slot)
        self._sequencer_clip.set_clip(clip)
        if clip:
            action.select(slot)
            self.notify_clip_selected()
        else:
            return None