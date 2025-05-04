# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\lockable_combo.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.elements import ComboElement

class LockableComboElement(ComboElement):
    pass

    def _modifier_is_valid(self, mod):
        return self.owns_control_element(mod) and (mod.is_pressed or (hasattr(mod, 'is_locked') and mod.is_locked))