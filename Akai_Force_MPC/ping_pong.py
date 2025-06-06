# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\ping_pong.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.base import task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.control import InputControl
PING_PERIOD = 3

class PingPongComponent(Component):
    pong = InputControl()

    def __init__(self, on_pong_callback=None, on_ping_timeout=None, *a, **k):
        super(PingPongComponent, self).__init__(*a, **k)
        self._on_pong_callback = on_pong_callback
        self._on_ping_timeout = on_ping_timeout
        self._ping = None
        self._pong_received = False
        self._keepalive_task = self._tasks.add(task.sequence(task.run(self._send_ping), task.wait(PING_PERIOD), task.run(self._check_pong_received)))
        self._keepalive_task.kill()
        self._keepalive_starter_task = self._tasks.add(task.run(self._keepalive_task.restart))
        self._keepalive_starter_task.kill()

    @pong.value
    def pong(self, value, _):
        self._pong_received = True
        if not self._keepalive_task.is_running:
            self._keepalive_starter_task.restart()
        self._on_pong_callback(value)

    def set_ping(self, button):
        self._ping = button
        self._keepalive_starter_task.restart()

    def _send_ping(self):
        if self._ping and self.is_enabled():
            self._pong_received = False
            self._ping.send_value(0)

    def _check_pong_received(self):
        if not self._pong_received:
            self._keepalive_task.kill()
            self._on_ping_timeout()
            return
        else:
            self._keepalive_starter_task.restart()