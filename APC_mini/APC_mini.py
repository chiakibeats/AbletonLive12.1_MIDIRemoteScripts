# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_mini\APC_mini.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
from APC_Key_25.APC_Key_25 import APC_Key_25

class APC_mini(APC_Key_25):
    SESSION_HEIGHT = 8
    HAS_TRANSPORT = False

    def __init__(self, *a, **k):
        pass

    def _make_stop_all_button(self):
        return self.make_shifted_button(self._scene_launch_buttons[7])

    def _create_controls(self):
        super(APC_mini, self)._create_controls()
        self._unused_buttons = list(map(self.make_shifted_button, self._scene_launch_buttons[5:7]))
        self._master_volume_control = make_slider(0, 56, name='Master_Volume')

    def _create_mixer(self):
        mixer = super(APC_mini, self)._create_mixer()
        mixer.master_strip().layer = Layer(volume_control=self._master_volume_control)
        return mixer

    def _product_model_id_byte(self):
        return 40