# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Axiom\Transport.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .consts import *

class Transport(object):
    pass

    def __init__(self, parent):
        self.__parent = parent
        self.__ffwd_held = False
        self.__rwd_held = False
        self.__delay_counter = 0

    def build_midi_map(self, script_handle, midi_map_handle):
        for cc_no in AXIOM_TRANSPORT:
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, 15, cc_no)

    def receive_midi_cc(self, cc_no, cc_value):
        if cc_no == AXIOM_STOP:
            if cc_value > 0:
                self.__parent.song().is_playing = False
                return
            else:
                return None
        elif cc_no == AXIOM_PLAY:
            if cc_value > 0:
                self.__parent.song().is_playing = True
                return
            else:
                return None
        elif cc_no == AXIOM_REC:
            if cc_value > 0:
                self.__parent.song().record_mode = not self.__parent.song().record_mode
                return
            else:
                return None
        elif self.__parent.application().view.is_view_visible('Session'):
            if cc_value > 0:
                self.__cc_in_session(cc_no)
                return
            else:
                return None
        else:
            self.__cc_in_arranger(cc_no, cc_value)

    def __cc_in_session(self, cc_no):
        index = list(self.__parent.song().scenes).index(self.__parent.song().view.selected_scene)
        if cc_no == AXIOM_LOOP:
            self.__parent.song().view.selected_scene.fire_as_selected()
        elif cc_no == AXIOM_RWD:
            if index > 0:
                index = index - 1
                self.__parent.song().view.selected_scene = self.__parent.song().scenes[index]
        elif cc_no == AXIOM_FFWD:
            if index < len(self.__parent.song().scenes) - 1:
                index = index + 1
                self.__parent.song().view.selected_scene = self.__parent.song().scenes[index]

    def __cc_in_arranger(self, cc_no, cc_value):
        if cc_no == AXIOM_LOOP:
            if cc_value > 0:
                self.__parent.song().loop = not self.__parent.song().loop
            else:
                return None
        elif cc_no == AXIOM_RWD and (not self.__ffwd_held):
            if cc_value > 0:
                self.__rwd_held = True
                self.__delay_counter = 0
                self.__parent.song().jump_by(-1 * self.__parent.song().signature_denominator)
            else:
                self.__rwd_held = False
        elif cc_no == AXIOM_FFWD and (not self.__rwd_held):
            if cc_value > 0:
                self.__ffwd_held = True
                self.__delay_counter = 0
                self.__parent.song().jump_by(self.__parent.song().signature_denominator)
                return
            else:
                self.__ffwd_held = False
                return

    def refresh_state(self):
        if self.__ffwd_held:
            self.__delay_counter += 1
            if self.__delay_counter % 5 == 0:
                self.__parent.song().jump_by(self.__parent.song().signature_denominator)
        if self.__rwd_held:
            self.__delay_counter += 1
            if self.__delay_counter % 5 == 0:
                self.__parent.song().jump_by(-1 * self.__parent.song().signature_denominator)
                return