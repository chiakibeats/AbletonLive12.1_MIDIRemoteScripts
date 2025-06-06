# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MIDI_Mix\MIDI_Mix.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from _Framework.ButtonElement import Color
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.Dependency import inject
from _Framework.Layer import Layer
from _Framework.Skin import Skin
from _Framework.Util import const
from _APC.APC import APC
from .ControlElementUtils import make_button, make_button_row, make_encoder, make_slider
from .MixerComponent import MixerComponent
NUM_TRACKS = 8
SEND_IDS = ((16, 20, 24, 28, 46, 50, 54, 58), (17, 21, 25, 29, 47, 51, 55, 59))

class Colors(object):

    class DefaultButton(object):
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)

class MIDI_Mix(APC, OptimizedControlSurface):

    def __init__(self, *a, **k):
        pass

    def _create_controls(self):
        self._sliders = make_button_row(chain(range(19, 32, 4), range(49, 62, 4)), make_slider, 'Volume_Slider')
        self._rec_arm_buttons = make_button_row(range(3, 25, 3), make_button, 'Record_Arm_Button')
        self._mute_buttons = make_button_row(range(1, 23, 3), make_button, 'Mute_Button')
        self._solo_buttons = make_button_row(range(2, 24, 3), make_button, 'Solo_Button')
        self._send_encoders = ButtonMatrixElement(rows=[[make_encoder(id, 'Send_Encoder_%d' % (id_index + row_index * NUM_TRACKS)) for id_index, id in enumerate(row)] for row_index, row in enumerate(SEND_IDS)])
        self._pan_encoders = make_button_row(chain(range(18, 31, 4), range(48, 61, 4)), make_encoder, 'Pan_Encoder')
        self._bank_left_button = make_button(25, 'Bank_Left_Button')
        self._bank_right_button = make_button(26, 'Bank_Right_Button')
        self._solo_mode_button = make_button(27, 'Solo_Mode_Button')
        self._master_slider = make_slider(62, 'Master_Slider')

    def _create_mixer(self):
        self._mixer = MixerComponent(num_tracks=NUM_TRACKS, is_enabled=False, invert_mute_feedback=True, layer=Layer(volume_controls=self._sliders, pan_controls=self._pan_encoders, send_controls=self._send_encoders, bank_down_button=self._bank_left_button, bank_up_button=self._bank_right_button, arm_buttons=self._rec_arm_buttons, solo_buttons=self._solo_buttons, mute_buttons=self._mute_buttons))
        self._mixer.master_strip().layer = Layer(volume_control=self._master_slider)

    def _enable_components(self):
        pass

    def _on_identity_response(self, midi_bytes):
        super(MIDI_Mix, self)._on_identity_response(midi_bytes)
        self._enable_components()

    def _on_handshake_successful(self):
        return

    def _product_model_id_byte(self):
        return 49

    def _send_dongle_challenge(self):
        return