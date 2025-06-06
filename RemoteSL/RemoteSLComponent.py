# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL\RemoteSLComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .consts import *

class RemoteSLComponent(object):
    pass

    def __init__(self, remote_sl_parent):
        self.__parent = remote_sl_parent
        self.__support_mkII = False

    def application(self):
        return self.__parent.application()

    def song(self):
        return self.__parent.song()

    def send_midi(self, midi_event_bytes):
        self.__parent.send_midi(midi_event_bytes)

    def request_rebuild_midi_map(self):
        self.__parent.request_rebuild_midi_map()

    def disconnect(self):
        return

    def build_midi_map(self, script_handle, midi_map_handle):
        return

    def refresh_state(self):
        return

    def update_display(self):
        return

    def cc_status_byte(self):
        return CC_STATUS + SL_MIDI_CHANNEL

    def support_mkII(self):
        return self.__support_mkII

    def set_support_mkII(self, support_mkII):
        self.__support_mkII = support_mkII