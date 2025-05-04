# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\UserMatrixComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

def _disable_control(control):
    for button in control:
        button.set_enabled(False)

class UserMatrixComponent(ControlSurfaceComponent):
    pass

    def __getattr__(self, name):
        if len(name) > 4 and name[:4] == 'set_':
            return _disable_control
        else:
            raise AttributeError(name)