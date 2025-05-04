# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\undo_step_handler.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import liveobj_valid

class UndoStepHandler(object):
    pass

    def __init__(self, song=None):
        self._song = song
        self._clients = set()

    def _begin_step_with_client(self, client):
        if client not in self._clients:
            self._clients.add(client)
            if len(self._clients) == 1:
                self._song.begin_undo_step()
                return

    def _end_step_with_client(self, client):
        if client in self._clients:
            self._clients.remove(client)
            if len(self._clients) == 0:
                self._song.end_undo_step()
                return

    def begin_undo_step(self, client=None):
        if client:
            self._begin_step_with_client(client)
            return
        else:
            self._song.begin_undo_step()

    def end_undo_step(self, client=None):
        if client:
            self._end_step_with_client(client)
            return
        else:
            self._song.end_undo_step()
            if len(self._clients) > 0:
                self._song.begin_undo_step()
                return
            else:
                return None