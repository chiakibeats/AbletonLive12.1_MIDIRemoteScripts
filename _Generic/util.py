# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Generic\util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.SubjectSlot import SlotManager, subject_slot
from _Framework.Util import nop

class DeviceAppointer(SlotManager):

    def __init__(self, song=None, appointed_device_setter=nop, *a, **k):
        super(DeviceAppointer, self).__init__(*a, **k)
        self._set_appointed_device = appointed_device_setter
        self._appointed_device = None
        self._song = song
        self.__on_appointed_device_changed.subject = self._song
        self.__on_selected_track_changed.subject = self._song.view
        self.__on_selected_track_changed()

    @subject_slot('appointed_device')
    def __on_appointed_device_changed(self):
        if self._appointed_device != self._song.appointed_device:
            self._update_appointed_device(self._song.appointed_device)
            return

    @subject_slot('selected_device')
    def __on_selected_device_changed(self):
        song = self._song
        device = song.view.selected_track.view.selected_device
        if device != None:
            self._update_appointed_device(device)

    @subject_slot('selected_track')
    def __on_selected_track_changed(self):
        track_view = self._song.view.selected_track.view
        self.__on_selected_device_changed.subject = track_view
        self._update_appointed_device(track_view.selected_device)

    def _update_appointed_device(self, device):
        if device != None:
            self._appointed_device = device
            self._set_appointed_device(device)
            self._song.appointed_device = device