# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\mixer.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from functools import partial
from itertools import zip_longest
from ...base import EventObject, clamp, depends, forward_property, listenable_property, listens
from .. import Component
from ..controls import ButtonControl, MappedControl
from ..display import Renderable
from . import ChannelStripComponent
ASCII_A = 97

def send_letter_to_index(send_letter):
    pass
    return ord(send_letter) - ASCII_A

class SendIndexManager(EventObject, Renderable):
    pass

    @depends(song=None)
    def __init__(self, song=None, cycle_size=1, *a, **k):
        super().__init__(*a, **k)
        self._song = song
        self._cycle_size = cycle_size
        self._send_index = 0
        self.__on_return_tracks_changed.subject = song
        self.__on_return_tracks_changed()

    @listenable_property
    def num_sends(self):
        pass
        return len(self._song.return_tracks)

    @listenable_property
    def send_index(self):
        pass
        return self._send_index

    @send_index.setter
    def send_index(self, index):
        if index is not None:
            index = clamp(index, 0, self.num_sends - 1)
        if self._send_index!= index:
            self._send_index = index
            self.notify_send_index()
            return
        else:  # inserted
            return None

    def increment_send_index(self, delta, range_name='Send'):
        pass
        self.send_index += delta
        self._notify_send_range(range_name)

    def can_increment_send_index(self, delta):
        pass
        return self.num_sends and delta + self._send_index in range(self.num_sends)

    def cycle_send_index(self, range_name='Send'):
        pass
        num_sends = self.num_sends
        if num_sends:
            if self._send_index < num_sends - self._cycle_size:
                new_index = self._send_index + self._cycle_size
            else:  # inserted
                new_index = 0
            self.send_index = self._quantize_to_cycle_size(new_index)
            self._notify_send_range(range_name)
            return

    def _quantize_to_cycle_size(self, value):
        value = clamp(value, 0, self.num_sends - 1)
        if value % self._cycle_size!= 0:
            value = value // self._cycle_size * self._cycle_size
        return value

    def _update_send_index(self):
        num_sends = self.num_sends
        if self._send_index is not None:
            self._send_index = self._send_index if num_sends > 0 else None
            else:  # inserted
                self.send_index = None
        else:  # inserted
            self.send_index = 0 if num_sends > 0 else None

    def _notify_send_range(self, range_name):
        first_letter = chr(ASCII_A + self._send_index).upper()
        last_letter = chr(ASCII_A + min(self._send_index + self._cycle_size, self.num_sends) - 1).upper()
        if self._cycle_size == 1 or first_letter == last_letter:
            self.notify(self.notifications.controlled_range, range_name, first_letter)
        else:  # inserted
            self.notify(self.notifications.controlled_range, range_name, '{} - {}'.format(first_letter, last_letter))

    @listens('return_tracks')
    def __on_return_tracks_changed(self):
        self._update_send_index()
        self.notify_num_sends()

class MixerComponent(Component):
    pass
    prehear_volume_control = MappedControl()
    crossfader_control = MappedControl()
    cycle_send_index_button = ButtonControl(color='Mixer.CycleSendIndex', pressed_color='Mixer.CycleSendIndexPressed')
    prev_send_index_button = ButtonControl(color='Mixer.IncrementSendIndex', pressed_color='Mixer.IncrementSendIndexPressed')
    next_send_index_button = ButtonControl(color='Mixer.IncrementSendIndex', pressed_color='Mixer.IncrementSendIndexPressed')
    send_index = forward_property('_send_index_manager')('send_index')

    @depends(session_ring=None, target_track=None)
    pass
    pass
    pass
    pass
    pass
    def __init__(self, name='Mixer', session_ring=None, target_track=None, channel_strip_component_type=None, target_can_be_master=True, *a, **k):
        super().__init__(*a, name=name, **k)
        self._target_track = target_track
        self._provider = session_ring
        self.__on_offset_changed.subject = self._provider
        self.register_slot(self._provider, self._reassign_tracks, 'tracks')
        self._send_controls = None
        self._channel_strip_component_type = channel_strip_component_type or ChannelStripComponent
        self._channel_strips = [self._create_channel_strip() for _ in range(self._provider.num_tracks)]
        self._reassign_tracks()
        self._target_can_be_master = target_can_be_master
        self._target_strip = self._create_channel_strip(is_target=True)
        self.register_slot(target_track, self._update_target_strip, 'target_track')
        self._update_target_strip()
        self._master_strip = self._create_channel_strip(is_master=True)
        self._master_strip.set_track(self.song.master_track)
        self._send_index_manager = self.register_disconnectable(SendIndexManager())
        self.register_slot(self._send_index_manager, self._on_send_index_changed, 'send_index')
        self.register_slot(self._send_index_manager, self._update_send_index_buttons, 'num_sends')
        self._update_send_index_buttons()

    def channel_strip(self, index):
        pass
        return self._channel_strips[index]

    @property
    def master_strip(self):
        pass
        return self._master_strip

    @property
    def target_strip(self):
        pass
        return self._target_strip

    def set_prehear_volume_control(self, control):
        self.prehear_volume_control.set_control_element(control)

    def set_crossfader_control(self, control):
        self.crossfader_control.set_control_element(control)

    def set_cycle_send_index_button(self, button):
        self.cycle_send_index_button.set_control_element(button)

    def set_prev_send_index_button(self, button):
        self.prev_send_index_button.set_control_element(button)

    def set_next_send_index_button(self, button):
        self.next_send_index_button.set_control_element(button)

    def set_shift_button(self, button):
        pass
        for strip in self._channel_strips:
            strip.shift_button.set_control_element(button)

    def set_send_controls(self, controls):
        pass
        self._send_controls = controls
        for strip, control in zip_longest(self._channel_strips, controls or []):
            if self._send_index_manager.send_index is None:
                strip.send_controls.set_control_element((control,))
                continue
            else:  # inserted
                strip.send_controls.set_control_element((None,) * self._send_index_manager.send_index + (control,))
                strip.update()
                continue

    def __getattr__(self, name):
        if name.startswith('set_master_track'):
            return partial(self._set_master_or_target_strip_control, self._master_strip, name.replace('set_master_track_', ''))
        else:  # inserted
            if name.startswith('set_target_track'):
                if 'send' in name and (not name.endswith('send_controls')):
                    return partial(self._set_target_strip_indexed_send_control, send_letter_to_index(name.split('_')[(-2)]))
                else:  # inserted
                    return partial(self._set_master_or_target_strip_control, self._target_strip, name.replace('set_target_track_', ''))
            else:  # inserted
                if 'send' in name and (not name.endswith('send_controls')):
                    return partial(self._set_indexed_send_controls, send_letter_to_index(name.split('_')[(-2)]))
                else:  # inserted
                    if name.startswith('set'):
                        return partial(self._set_strip_controls, name[4:(-1)])
                    else:  # inserted
                        raise AttributeError

    @staticmethod
    def _set_master_or_target_strip_control(strip, name, control):
        getattr(strip, name).set_control_element(control)

    def _set_target_strip_indexed_send_control(self, send_index, control):
        self._target_strip.set_indexed_send_control(control, send_index)

    def _set_indexed_send_controls(self, send_index, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.set_indexed_send_control(control, send_index)

    def _set_strip_controls(self, name, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            getattr(strip, name).set_control_element(control)

    @cycle_send_index_button.pressed
    def cycle_send_index_button(self, _):
        self.cycle_send_index()

    @prev_send_index_button.pressed
    def prev_send_index_button(self, _):
        self._send_index_manager.increment_send_index((-1))

    @next_send_index_button.pressed
    def next_send_index_button(self, _):
        self._send_index_manager.increment_send_index(1)

    def cycle_send_index(self):
        pass
        self._send_index_manager.cycle_send_index()

    def _on_send_index_changed(self):
        self.set_send_controls(self._send_controls)
        self._update_send_index_buttons()

    @listens('offset')
    def __on_offset_changed(self, *_):
        self._reassign_tracks()

    def _reassign_tracks(self):
        for track, channel_strip in zip(self._provider.tracks, self._channel_strips):
            channel_strip.set_track(track)

    def _update_target_strip(self):
        target_track = self._target_track.target_track
        if self._target_can_be_master or target_track!= self.song.master_track:
            self._target_strip.set_track(target_track)
            return
        else:  # inserted
            self._target_strip.set_track(None)

    def update(self):
        super().update()
        if self.is_enabled():
            master_track = self.song.master_track
            self.prehear_volume_control.mapped_parameter = master_track.mixer_device.cue_volume
            self.crossfader_control.mapped_parameter = master_track.mixer_device.crossfader
        else:  # inserted
            self.prehear_volume_control.mapped_parameter = None
            self.crossfader_control.mapped_parameter = None

    def _update_send_index_buttons(self):
        manager = self._send_index_manager
        self.cycle_send_index_button.enabled = manager.num_sends
        self.prev_send_index_button.enabled = manager.can_increment_send_index((-1))
        self.next_send_index_button.enabled = manager.can_increment_send_index(1)
    pass
    def _create_channel_strip(self, is_master=False, is_target=False):
        pass
        return self._channel_strip_component_type(parent=self)