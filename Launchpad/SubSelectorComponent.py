# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad\SubSelectorComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.SessionComponent import SessionComponent
from .PreciseButtonSliderElement import *
from .SpecialMixerComponent import SpecialMixerComponent
LED_OFF = 4
RED_FULL = 7
RED_HALF = 6
RED_THIRD = 5
RED_BLINK = 11
GREEN_FULL = 52
GREEN_HALF = 36
GREEN_THIRD = 20
GREEN_BLINK = 56
AMBER_FULL = RED_FULL + GREEN_FULL - 4
AMBER_HALF = RED_HALF + GREEN_HALF - 4
AMBER_THIRD = RED_THIRD + GREEN_THIRD - 4
AMBER_BLINK = AMBER_FULL - 4 + 8
PAN_VALUE_MAP = (-1.0, -0.634921, -0.31746, 0.0, 0.0, 0.31746, 0.634921, 1.0)
VOL_VALUE_MAP = (0.0, 0.142882, 0.302414, 0.4, 0.55, 0.7, 0.85, 1.0)
SEND_VALUE_MAP = (0.0, 0.103536, 0.164219, 0.238439, 0.343664, 0.55, 0.774942, 1.0)

class SubSelectorComponent(ModeSelectorComponent):
    pass

    def __init__(self, matrix, side_buttons, session):
        ModeSelectorComponent.__init__(self)
        self._session = session
        self._mixer = SpecialMixerComponent(matrix.width())
        self._matrix = matrix
        self._sliders = []
        self._mixer.name = 'Mixer'
        self._mixer.master_strip().name = 'Master_Channel_strip'
        self._mixer.selected_strip().name = 'Selected_Channel_strip'
        for column in range(matrix.width()):
            self._mixer.channel_strip(column).name = 'Channel_Strip_' + str(column)
            self._sliders.append(PreciseButtonSliderElement(tuple([matrix.get_button(column, 7 - row) for row in range(8)])))
            self._sliders[-1].name = 'Button_Slider_' + str(column)
        self._side_buttons = side_buttons[4:]
        self._update_callback = None
        self._session.set_mixer(self._mixer)
        self.set_modes_buttons(side_buttons[:4])

    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)
        self._session = None
        self._mixer = None
        for slider in self._sliders:
            slider.release_parameter()
            slider.set_disabled(True)
        self._sliders = None
        self._matrix = None
        self._side_buttons = None
        self._update_callback = None
        ModeSelectorComponent.disconnect(self)

    def set_update_callback(self, callback):
        self._update_callback = callback

    def set_modes_buttons(self, buttons):
        identify_sender = True
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)
        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                self._modes_buttons.append(button)
                button.add_value_listener(self._mode_value, identify_sender)

    def set_mode(self, mode):
        if self._mode_index != mode or mode == -1:
            self._mode_index = mode
            self.update()

    def mode(self):
        result = 0
        if self.is_enabled():
            result = self._mode_index + 1
        return result

    def number_of_modes(self):
        return 4

    def on_enabled_changed(self):
        enabled = self.is_enabled()
        for index in range(self._matrix.width()):
            self._sliders[index].set_disabled(not enabled)
        self._mixer.set_enabled(enabled)
        self.set_mode(-1)

    def release_controls(self):
        for track in range(self._matrix.width()):
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(127, LED_OFF)
            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None, None, None, None)
            strip.set_mute_button(None)
            strip.set_solo_button(None)
            strip.set_arm_button(None)
            strip.set_send_controls((None, None))
            strip.set_pan_control(None)
            strip.set_volume_control(None)
            continue
        self._session.set_stop_track_clip_buttons(None)
        self._mixer.set_global_buttons(None, None, None)
        self._session.set_stop_all_clips_button(None)

    def update(self):
        super(SubSelectorComponent, self).update()
        if self.is_enabled():
            if self._modes_buttons != None:
                for index in range(len(self._modes_buttons)):
                    self._modes_buttons[index].set_on_off_values(GREEN_FULL, GREEN_THIRD)
                    if index == self._mode_index:
                        self._modes_buttons[index].turn_on()
                        continue
                    else:
                        self._modes_buttons[index].turn_off()
                        continue
            for button in self._side_buttons:
                button.set_on_off_values(127, LED_OFF)
                button.turn_off()
            for index in range(self._matrix.width()):
                self._sliders[index].set_disabled(self._mode_index == -1)
            self._mixer.set_allow_update(False)
            self._session.set_allow_update(False)
            if self._mode_index == -1:
                self._setup_mixer_overview()
            elif self._mode_index == 0:
                self._setup_volume_mode()
            elif self._mode_index == 1:
                self._setup_pan_mode()
            elif self._mode_index == 2:
                self._setup_send1_mode()
            elif self._mode_index == 3:
                self._setup_send2_mode()
            if self._update_callback != None:
                self._update_callback()
            self._mixer.set_allow_update(True)
            self._session.set_allow_update(True)
            return
        else:
            self.release_controls()

    def _setup_mixer_overview(self):
        trkon_index = 5
        stop_buttons = []
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_send_controls((None, None))
            strip.set_pan_control(None)
            strip.set_volume_control(None)
            self._sliders[track].release_parameter()
            for row in range(self._matrix.height()):
                full_value = GREEN_THIRD
                third_value = GREEN_FULL
                if row == trkon_index:
                    full_value = AMBER_FULL
                    third_value = AMBER_THIRD
                elif row > 3:
                    full_value = RED_FULL
                    third_value = RED_THIRD
                self._matrix.get_button(track, row).set_on_off_values(full_value, third_value)
                continue
            strip.set_default_buttons(self._matrix.get_button(track, 0), self._matrix.get_button(track, 1), self._matrix.get_button(track, 2), self._matrix.get_button(track, 3))
            stop_buttons.append(self._matrix.get_button(track, 4))
            strip.set_mute_button(self._matrix.get_button(track, 5))
            strip.set_solo_button(self._matrix.get_button(track, 6))
            strip.set_arm_button(self._matrix.get_button(track, 7))
            continue
        for button in self._side_buttons:
            if list(self._side_buttons).index(button) == trkon_index - 4:
                button.set_on_off_values(AMBER_FULL, AMBER_THIRD)
            else:
                button.set_on_off_values(RED_FULL, RED_THIRD)
            button.set_force_next_value()
            button.turn_off()
            continue
        self._session.set_stop_track_clip_buttons(tuple(stop_buttons))
        self._session.set_stop_all_clips_button(self._side_buttons[0])
        self._mixer.set_global_buttons(self._side_buttons[3], self._side_buttons[2], self._side_buttons[1])

    def _setup_volume_mode(self):
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None, None, None, None)
            strip.set_mute_button(None)
            strip.set_solo_button(None)
            strip.set_arm_button(None)
            strip.set_send_controls((None, None))
            strip.set_pan_control(None)
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(GREEN_FULL, LED_OFF)
            self._sliders[track].set_mode(SLIDER_MODE_VOLUME)
            self._sliders[track].set_value_map(VOL_VALUE_MAP)
            strip.set_volume_control(self._sliders[track])
            continue
        self._session.set_stop_track_clip_buttons(None)
        self._session.set_stop_all_clips_button(None)
        self._mixer.set_global_buttons(None, None, None)

    def _setup_pan_mode(self):
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None, None, None, None)
            strip.set_mute_button(None)
            strip.set_solo_button(None)
            strip.set_arm_button(None)
            strip.set_send_controls((None, None))
            strip.set_volume_control(None)
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(AMBER_FULL, LED_OFF)
            self._sliders[track].set_mode(SLIDER_MODE_PAN)
            self._sliders[track].set_value_map(PAN_VALUE_MAP)
            strip.set_pan_control(self._sliders[track])
            continue
        self._session.set_stop_track_clip_buttons(None)
        self._session.set_stop_all_clips_button(None)
        self._mixer.set_global_buttons(None, None, None)

    def _setup_send1_mode(self):
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None, None, None, None)
            strip.set_mute_button(None)
            strip.set_solo_button(None)
            strip.set_arm_button(None)
            strip.set_volume_control(None)
            strip.set_pan_control(None)
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(RED_FULL, LED_OFF)
            self._sliders[track].set_mode(SLIDER_MODE_VOLUME)
            self._sliders[track].set_value_map(SEND_VALUE_MAP)
            strip.set_send_controls((self._sliders[track], None))
            continue
        self._session.set_stop_track_clip_buttons(None)
        self._session.set_stop_all_clips_button(None)
        self._mixer.set_global_buttons(None, None, None)

    def _setup_send2_mode(self):
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None, None, None, None)
            strip.set_mute_button(None)
            strip.set_solo_button(None)
            strip.set_arm_button(None)
            strip.set_volume_control(None)
            strip.set_pan_control(None)
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(RED_FULL, LED_OFF)
            self._sliders[track].set_mode(SLIDER_MODE_VOLUME)
            self._sliders[track].set_value_map(SEND_VALUE_MAP)
            strip.set_send_controls((None, self._sliders[track]))
            continue
        self._session.set_stop_track_clip_buttons(None)
        self._session.set_stop_all_clips_button(None)
        self._mixer.set_global_buttons(None, None, None)