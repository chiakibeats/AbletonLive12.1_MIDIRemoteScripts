# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\EncoderMixerModeSelector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from .NotifyingMixerComponent import NotifyingMixerComponent

class EncoderMixerModeSelector(ModeSelectorComponent):
    pass

    def __init__(self, mixer):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._controls = None
        self._page_names = ('Vol', 'Pan', 'SendA', 'SendB', 'SendC')
        self._page_name_sources = None
        self._current_page_data_source = DisplayDataSource()
        self._parameter_sources = [DisplayDataSource() for index in range(8)]
        self._show_volume_page = False
        self._mixer.set_update_callback(self._mixer_assignments_changed)

    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)
        self._mixer = None
        self._controls = None
        self._page_names = None
        self._page_name_sources = None
        self._current_page_data_source = None
        self._parameter_sources = None
        ModeSelectorComponent.disconnect(self)

    def set_modes_buttons(self, buttons):
        identify_sender = True
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)
        self._modes_buttons = []
        if buttons!= None:
            for button in buttons:
                self._modes_buttons.append(button)
                button.add_value_listener(self._mode_value, identify_sender)
        self.set_mode(0)
        self.update()

    def set_controls(self, controls):
        self._controls = controls
        self.set_mode(0)
        self.update()

    def set_show_volume_page(self, show):
        if show!= self._show_volume_page:
            self._show_volume_page = show
            if self._page_name_sources!= None:
                offset = 0
                if not self._show_volume_page:
                    offset = 1
                for idx in range(4):
                    self._page_name_sources[idx].set_display_string(self._page_names[idx + offset])
            self.update()

    def page_name_data_source(self, index):
        if self._page_name_sources == None:
            self._page_name_sources = []
            offset = 0
            if not self._show_volume_page:
                offset = 1
            for idx in range(4):
                self._page_name_sources.append(DisplayDataSource())
                self._page_name_sources[idx].set_display_string(self._page_names[idx + offset])
        return self._page_name_sources[index]

    def parameter_data_source(self, index):
        return self._mixer.channel_strip(index).track_name_data_source()

    def current_page_data_source(self):
        return self._current_page_data_source

    def number_of_modes(self):
        return 4

    def update(self):
        super(EncoderMixerModeSelector, self).update()
        if not self.is_enabled() or self._controls!= None:
                mode = self._mode_index
                if not self._show_volume_page:
                    mode += 1
                self._current_page_data_source.set_display_string(self._page_names[mode])
                for index in range(len(self._controls)):
                    self._controls[index].release_parameter()
                    self._mixer.channel_strip(index).track_name_data_source().update()
                    self._mixer.channel_strip(index).set_pan_control(None)
                    self._mixer.channel_strip(index).set_send_controls((None, None, None))
                    if self._show_volume_page:
                        self._mixer.channel_strip(index).set_volume_control(None)
                    if mode == 0:
                        self._mixer.channel_strip(index).set_volume_control(self._controls[index])
                        continue
                    else:  # inserted
                        if mode == 1:
                            self._mixer.channel_strip(index).set_pan_control(self._controls[index])
                            continue
                        else:  # inserted
                            if mode == 2:
                                self._mixer.channel_strip(index).set_send_controls((self._controls[index], None, None))
                                continue
                            else:  # inserted
                                if mode == 3:
                                    self._mixer.channel_strip(index).set_send_controls((None, self._controls[index], None))
                                    continue
                                else:  # inserted
                                    if mode == 4:
                                        self._mixer.channel_strip(index).set_send_controls((None, None, self._controls[index]))
                                        continue
                                    else:  # inserted
                                        print('Invalid mode index')
                                        continue
                return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _mixer_assignments_changed(self):
        self.update()