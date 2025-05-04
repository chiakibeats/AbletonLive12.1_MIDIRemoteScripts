# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_A\komplete_kontrol_a.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Komplete_Kontrol.komplete_kontrol_base import KompleteKontrolBase, Layer, create_button, create_encoder
from .view_control_component import ViewControlComponent

class Komplete_Kontrol_A(KompleteKontrolBase):

    def _create_controls(self):
        super(Komplete_Kontrol_A, self)._create_controls()
        self._mute_button = create_button(67, 'Mute_Button')
        self._solo_button = create_button(68, 'Solo_Button')
        self._vertical_encoder = create_encoder(48, 'Vertical_Encoder')
        self._horizontal_encoder = create_encoder(50, 'Horizontal_Encoder')

    def _create_components(self):
        super(Komplete_Kontrol_A, self)._create_components()
        self._create_view_control()

    def _create_view_control(self):
        self._view_control = ViewControlComponent(name='View_Control', is_enabled=False, layer=Layer(vertical_encoder=self._vertical_encoder, horizontal_encoder=self._horizontal_encoder))

    def _create_mixer_component_layer(self):
        return super(Komplete_Kontrol_A, self)._create_mixer_component_layer() + Layer(mute_button=self._mute_button, solo_button=self._solo_button)