# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MPDMkIIBase\MPDMkIIBase.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.DrumRackComponent import DrumRackComponent
from _Framework.InputControlElement import MIDI_NOTE_TYPE
from _Framework.Layer import Layer
from _Framework.MixerComponent import MixerComponent
from _Framework.TransportComponent import TransportComponent

class MPDMkIIBase(ControlSurface):

    def __init__(self, pad_ids=None, pad_channel=None, *a, **k):
        pass

    def _create_controls(self):
        pass
        self._create_pads()

    def _create_pads(self):
        self._pads = ButtonMatrixElement(rows=[ButtonElement(True, MIDI_NOTE_TYPE, self._pad_channel, pad_id, name='Pad_%d_%d' % (col_index, row_index)) for row_index, row in enumerate(row)])

    def _create_drums(self):
        self._drums = DrumRackComponent(is_enabled=True, name='Drums')
        self._drums.layer = Layer(pads=self._pads)

    def _create_device(self):
        self._device = DeviceComponent(is_enabled=True, name='Device', device_selection_follows_track_selection=True)
        self._device.layer = Layer(parameter_controls=self._encoders)
        self.set_device_component(self._device)

    def _create_transport(self):
        self._transport = TransportComponent(is_enabled=True, name='Transport')
        self._transport.layer = Layer(play_button=self._play_button, stop_button=self._stop_button, record_button=self._record_button)

    def _create_mixer(self):
        self._mixer = MixerComponent(is_enabled=True, num_tracks=len(self._sliders), invert_mute_feedback=True, name='Mixer')
        self._mixer.layer = Layer(volume_controls=self._sliders)