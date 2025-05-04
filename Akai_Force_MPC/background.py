# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\background.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.control_surface.components import BackgroundComponent

class LightingBackgroundComponent(BackgroundComponent):

    def _clear_control(self, name, control):
        super(LightingBackgroundComponent, self)._clear_control(name, control)
        if control:
            control.set_light('Background.On')