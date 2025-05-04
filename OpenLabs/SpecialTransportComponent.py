# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\OpenLabs\SpecialTransportComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.TransportComponent import TransportComponent

class SpecialTransportComponent(TransportComponent):
    pass

    def __init__(self):
        TransportComponent.__init__(self)
        self._undo_button = None
        self._redo_button = None
        self._bts_button = None

    def disconnect(self):
        TransportComponent.disconnect(self)
        if self._undo_button != None:
            self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = None
        if self._redo_button != None:
            self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = None
        if self._bts_button != None:
            self._bts_button.remove_value_listener(self._bts_value)
            self._bts_button = None
            return

    def set_undo_button(self, undo_button):
        if undo_button != self._undo_button:
            if self._undo_button != None:
                self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = undo_button
            if self._undo_button != None:
                self._undo_button.add_value_listener(self._undo_value)
            self.update()

    def set_redo_button(self, redo_button):
        if redo_button != self._redo_button:
            if self._redo_button != None:
                self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = redo_button
            if self._redo_button != None:
                self._redo_button.add_value_listener(self._redo_value)
            self.update()
            return

    def set_bts_button(self, bts_button):
        if bts_button != self._bts_button:
            if self._bts_button != None:
                self._bts_button.remove_value_listener(self._bts_value)
            self._bts_button = bts_button
            if self._bts_button != None:
                self._bts_button.add_value_listener(self._bts_value)
            self.update()
            return

    def _undo_value(self, value):
        if self.is_enabled():
            if value != 0 or not self._undo_button.is_momentary():
                if self.song().can_undo:
                    self.song().undo()
                    return
                else:
                    return None
            else:
                return None
        else:
            return None

    def _redo_value(self, value):
        if self.is_enabled():
            if value != 0 or not self._redo_button.is_momentary():
                if self.song().can_redo:
                    self.song().redo()
                    return
                else:
                    return None
            else:
                return None
        else:
            return None

    def _bts_value(self, value):
        if self.is_enabled():
            if value != 0 or not self._bts_button.is_momentary():
                self.song().current_song_time = 0.0