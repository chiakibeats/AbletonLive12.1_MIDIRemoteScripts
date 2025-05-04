# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Generic\SelectChanStripComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ChannelStripComponent import ChannelStripComponent

class SelectChanStripComponent(ChannelStripComponent):
    pass

    def __init__(self):
        ChannelStripComponent.__init__(self)

    def _arm_value(self, value):
        if self.is_enabled():
            track_was_armed = False
            if self._track != None and self._track.can_be_armed:
                track_was_armed = self._track.arm
            ChannelStripComponent._arm_value(self, value)
            if self._track != None and self._track.can_be_armed and self._track.arm and (not track_was_armed) and self._track.view.select_instrument():
                self.song().view.selected_track = self._track