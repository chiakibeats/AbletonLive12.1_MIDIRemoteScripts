# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV2_LX2_LC2_LD2\LV2TransportController.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .consts import *
from .FaderfoxTransportController import FaderfoxTransportController

class LV2TransportController(FaderfoxTransportController):
    __module__ = __name__
    'Class representing the transport section of LV2 controllers'
    __filter_funcs__ = ['update_display', 'log']
    __use_slot_led__ = True

    def __init__(self, parent):
        LV2TransportController.realinit(self, parent)

    def realinit(self, parent):
        FaderfoxTransportController.realinit(self, parent)
        if self.__use_slot_led__:
            self.tracks_with_listener = []
            self.slots_with_listener = []
            self.clips_with_listener = []
            self.slot_callbacks = []
            self.clip_callbacks = []
        self.first = 2

    def trigger_track_clip(self, track_idx, clip_idx):
        if self.helper.trigger_track_clip(track_idx, clip_idx) == 0:
            self.set_slot_launch_led(track_idx, clip_idx, False)

    def stop_track(self, track_idx):
        track_idx, clip_idx = self.helper.stop_track(track_idx)
        if track_idx and clip_idx:
            self.set_slot_launch_led(track_idx, clip_idx, False)

    def build_midi_map(self, script_handle, midi_map_handle):
        FaderfoxTransportController.build_midi_map(self, script_handle, midi_map_handle)
        if self.__use_slot_led__:
            self.remove_clip_listeners()
            self.add_clip_listeners()
            self.update_track_playing_status()
        if self.first > 0:
            self.first -= 1
            self.clear_all_leds()
            return

    def clear_all_leds(self):
        for track_idx in range(0, 12):
            for clip_idx in range(0, 12):
                self.set_slot_launch_led(track_idx, clip_idx, False)
            continue

    def set_slot_launch_led(self, track_idx, clip_idx, playing):
        self.log('set slot launch led %s %s %s' % (track_idx, clip_idx, playing))
        channel = AUX_CHANNEL_SETUP2
        note_no = 0
        if clip_idx > 7:
            channel = CHANNEL_SETUP2
        if clip_idx < 6:
            note_no = SLOT_LAUNCH_NOTES1[track_idx][clip_idx]
        else:
            note_no = SLOT_LAUNCH_NOTES2[track_idx][clip_idx - 6]
        if playing:
            self.parent.send_midi((NOTEON_STATUS + channel, note_no, 127))
            return
        else:
            self.parent.send_midi((NOTEOFF_STATUS + channel, note_no, 0))

    def on_slot_clip_changed(self, slot, track_idx, slot_idx):
        if slot.has_clip and slot.clip.is_playing:
            self.set_slot_launch_led(track_idx, slot_idx, True)
        else:
            self.set_slot_launch_led(track_idx, slot_idx, False)
        self.remove_clip_listeners()
        self.add_clip_listeners()

    def on_clip_playing_changed(self, clip, track_idx, clip_idx):
        if not clip.is_triggered:
            self.set_slot_launch_led(track_idx, clip_idx, clip.is_playing)
            self.update_track_playing_status()
            return

    def update_track_playing_status(self):
        i = 0
        for track in self.parent.song().tracks:
            if i > 11:
                return
            else:
                if self.helper.is_track_playing(track):
                    self.parent.send_midi((NOTEON_STATUS + TRACK_CHANNEL_SETUP2, LAUNCH_NOTES[i], 127))
                else:
                    self.parent.send_midi((NOTEOFF_STATUS + TRACK_CHANNEL_SETUP2, LAUNCH_NOTES[i], 0))
                i += 1
                continue
        return None

    def clip_add_callback(self, clip, track_idx, clip_idx):
        callback = lambda: self.on_clip_playing_changed(clip, track_idx, clip_idx)
        clip.add_playing_status_listener(callback)
        self.clips_with_listener += [clip]
        self.clip_callbacks += [callback]

    def slot_add_callback(self, slot, track_idx, slot_idx):
        callback = lambda: self.on_slot_clip_changed(slot, track_idx, slot_idx)
        slot.add_has_clip_listener(callback)
        self.slots_with_listener += [slot]
        self.slot_callbacks += [callback]

    def add_clip_listeners(self):
        i = 0
        for track in self.parent.song().tracks:
            if i > 11:
                return
            else:
                sloti = 0
                for slot in track.clip_slots:
                    if slot.has_clip:
                        self.slot_add_callback(slot, i, sloti)
                        self.clip_add_callback(slot.clip, i, sloti)
                    sloti += 1
                    continue
                i += 1
                continue

    def remove_slot_listeners(self):
        for i in range(0, len(self.slots_with_listener)):
            slot = self.slots_with_listener[i]
            callback = self.slot_callbacks[i]
            try:
                if slot.has_clip_has_listener(callback):
                    slot.remove_has_clip_listener(callback)
            except:
                continue
            else:
                continue
        self.slots_with_listener = []
        self.slot_callbacks = []

    def remove_clip_listeners(self):
        self.remove_slot_listeners()
        for i in range(0, len(self.clips_with_listener)):
            clip = self.clips_with_listener[i]
            callback = self.clip_callbacks[i]
            try:
                if clip.playing_status_has_listener(callback):
                    clip.remove_playing_status_listener(callback)
            except:
                continue
            else:
                continue
        self.clips_with_listener = []
        self.clip_callbacks = []

    def disconnect(self):
        if self.__use_slot_led__:
            self.remove_clip_listeners()