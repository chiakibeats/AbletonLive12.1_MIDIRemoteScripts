# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\drum_group.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase

class DrumGroupComponent(DrumGroupComponentBase):

    def set_matrix(self, matrix):
        if matrix is None and self.matrix.control_elements is not None:
            for button in self.matrix.control_elements:
                button.clear_send_cache()
                button.reset()
        super().set_matrix(matrix)