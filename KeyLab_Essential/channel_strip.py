# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\channel_strip.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from .ringed_mapped_encoder_control import RingedMappedEncoderControl

class ChannelStripComponent(ChannelStripComponentBase):
    pan_control = RingedMappedEncoderControl()

    def set_pan_control(self, control):
        self.pan_control.set_control_element(control)
        self.update()

    def _connect_parameters(self):
        super(ChannelStripComponent, self)._connect_parameters()
        self.pan_control.mapped_parameter = self.track.mixer_device.panning

    def _disconnect_parameters(self):
        self.pan_control.mapped_parameter = None
        super(ChannelStripComponent, self)._disconnect_parameters()