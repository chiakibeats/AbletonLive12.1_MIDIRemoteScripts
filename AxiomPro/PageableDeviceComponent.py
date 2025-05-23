# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\PageableDeviceComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Generic.Devices import *
from _Framework.ButtonElement import ButtonElement
from _Framework.DeviceComponent import DeviceComponent
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.EncoderElement import EncoderElement
SPECIAL_NAME_DICT = {'InstrumentImpulse': (('Pad1', 'Pad2'), ('Pad3', 'Pad4'), ('Pad5', 'Pad6'), ('Pad7', 'Pad8')), 'Operator': (('OscA', 'OscB', 'OscC', 'OscD'), ('LFO', 'Fltr'), ('Pitch',), ('Glob.',)), 'MultiSampler': (('Vol.', 'Pitch'), ('Fltr', 'FEnv'), ('LFO1', 'LFO2', 'LFO3'), ('Osc',)), 'UltraAnalog': (('Osc',), ('Fltr', 'FEnv', 'FMod'), ('VEnv', 'Mix'), ('Out',)), 'LoungeLizard': (('Ma&Ti',), ('To&Da',), ('Pick', 'Mod'),
SPECIAL_DEVICE_DICT = {'InstrumentImpulse': [(IMP_BANK1, IMP_BANK2), (IMP_BANK3, IMP_BANK4), (IMP_BANK5, IMP_BANK6), (IMP_BANK7, IMP_BANK8)], 'Operator': [(OPR_BANK1, OPR_BANK2, OPR_BANK3, OPR_BANK4), (OPR_BANK5, OPR_BANK6), (OPR_BANK7,), (OPR_BANK8,)], 'MultiSampler': [(SAM_BANK1, SAM_BANK8), (SAM_BANK2, SAM_BANK3), (SAM_BANK4, SAM_BANK5, SAM_BANK6), (SAM_BANK7,)], 'UltraAnalog': [(ALG_BANK1,), (ALG_BANK2, ALG_BANK3, ALG_BANK4), (ALG_BANK5, ALG_BANK6), (ALG_BANK7,)], 'LoungeLizard': [(ELC_BANK1,), (TNS_BANK3, TNS_BANK4), (TNS_BANK6, TNS_BANK7), (TNS_BANK8, TNS_BANK5)], 'StringStudio': [(EQ8_BANK1, EQ8_BANK7), (EQ8_BANK2, EQ8_BANK3), (EQ8_BANK4, EQ8_BANK5), (EQ8_BANK6,)]}

class PageableDeviceComponent(DeviceComponent):
    pass

    def __init__(self, *a, **k):
        super(PageableDeviceComponent, self).__init__(*a, **k)
        self._parameter_value_data_source = DisplayDataSource()
        self._parameter_name_data_sources = []
        self._page_name_data_sources = []
        self._page_index = [0, 0, 0, 0]
        for new_index in range(8):
            self._parameter_name_data_sources.append(DisplayDataSource())
            self._page_name_data_sources.append(DisplayDataSource())
            self._parameter_name_data_sources[(-1)].set_display_string(' - ')
            self._page_name_data_sources[(-1)].set_display_string(' - ')

    def disconnect(self):
        self._parameter_value_data_source = None
        self._parameter_name_data_sources = None
        self._page_name_data_sources = None
        DeviceComponent.disconnect(self)

    def set_device(self, device):
        DeviceComponent.set_device(self, device)
        if self._device == None:
            for source in self._parameter_name_data_sources:
                source.set_display_string(' - ')
            for source in self._page_name_data_sources:
                source.set_display_string(' - ')
        else:  # inserted
            return

    def set_bank_buttons(self, buttons):
        DeviceComponent.set_bank_buttons(self, buttons)

    def set_parameter_controls(self, controls):
        if self._parameter_controls!= None:
            for control in self._parameter_controls:
                if self._device!= None:
                    control.release_parameter()
                continue
        self._parameter_controls = controls
        if self._parameter_controls!= None:
            for control in self._parameter_controls:
                pass  # postinserted
        self.update()

    def parameter_value_data_source(self):
        return self._parameter_value_data_source

    def parameter_name_data_source(self, index):
        return self._parameter_name_data_sources[index]

    def page_name_data_source(self, index):
        return self._page_name_data_sources[index]

    def _bank_value(self, value, button):
        if self.is_enabled():
            if not button.is_momentary() or value!= 0:
                bank = list(self._bank_buttons).index(button)
                if self._device!= None and bank!= self._bank_index:
                        self._bank_index = bank
                    else:  # inserted
                        self._page_index[bank] += 1
                    self.update()

    def _assign_parameters(self):
        if self._device.class_name in list(SPECIAL_DEVICE_DICT.keys()):
            self.__assign_parameters_special()
        else:  # inserted
            if self._device.class_name in list(DEVICE_DICT.keys()):
                self.__assign_parameters_normal()
            else:  # inserted
                self.__assign_parameters_plugin()
        self._parameter_value_data_source.set_display_string('')
        for index in range(len(self._parameter_controls)):
            if self._parameter_controls[index].mapped_parameter()!= None:
                self._parameter_name_data_sources[index].set_display_string(self._parameter_controls[index].mapped_parameter().name)
                continue
            else:  # inserted
                self._parameter_name_data_sources[index].set_display_string(' - ')
                continue

    def __assign_parameters_special(self):
        pass
        banks = SPECIAL_DEVICE_DICT[self._device.class_name]
        bank_names = SPECIAL_NAME_DICT[self._device.class_name]
        pages = banks[self._bank_index]
        self._page_index[self._bank_index] %= len(pages)
        self._bank_name = bank_names[self._bank_index][self._page_index[self._bank_index]]
        page = pages[self._page_index[self._bank_index]]
        for index in range(len(self._parameter_controls)):
            parameter = get_parameter_by_name(self._device, page[index])
            if parameter!= None:
                self._parameter_controls[index].connect_to(parameter)
                continue
            else:  # inserted
                self._parameter_controls[index].release_parameter()
                continue
        for index in range(len(self._page_name_data_sources)):
            if index < len(bank_names):
                page_names = bank_names[index]
                if index == self._bank_index:
                    self._page_name_data_sources[index].set_display_string(page_names[(self._page_index[index] + 1) % len(page_names)])
                    continue
                else:  # inserted
                    self._page_name_data_sources[index].set_display_string(page_names[self._page_index[index] % len(page_names)])
                    continue
            else:  # inserted
                self._page_name_data_sources[index].set_display_string(' - ')
                continue

    def __assign_parameters_normal(self):
        pass
        self._page_index[self._bank_index] = 0
        banks = DEVICE_DICT[self._device.class_name]
        bank_names = []
        if len(banks) > self._bank_index:
            if self._device.class_name in list(BANK_NAME_DICT.keys()) and len(BANK_NAME_DICT[self._device.class_name]) > 1:
                bank_names = BANK_NAME_DICT[self._device.class_name]
            bank = banks[self._bank_index]
            if self._bank_index in range(len(bank_names)):
                self._bank_name = bank_names[self._bank_index]
            else:  # inserted
                self._bank_name = 'Bank ' + str(self._bank_index + 1)
            for index in range(len(self._parameter_controls)):
                parameter = get_parameter_by_name(self._device, bank[index])
                if parameter!= None:
                    self._parameter_controls[index].connect_to(parameter)
                    continue
                else:  # inserted
                    self._parameter_controls[index].release_parameter()
                    continue
        for index in range(len(self._page_name_data_sources)):
            if index < len(bank_names):
                self._page_name_data_sources[index].set_display_string(bank_names[index])
                continue
            else:  # inserted
                self._page_name_data_sources[index].set_display_string(' - ')
                continue

    def __assign_parameters_plugin(self):
        pass
        num_controls = len(self._parameter_controls)
        num_banks = min(8, number_of_parameter_banks(self._device))
        num_double_pages = 0
        num_double_pages_before = 0
        parameters_to_use = self._device.parameters[1:]
        self._bank_name = 'Bank ' + str(self._bank_index + 1)
        if num_banks > 4:
            num_double_pages = num_banks - 4
        if self._bank_index < num_double_pages:
            self._page_index[self._bank_index] %= 2
            num_double_pages_before = self._bank_index
        else:  # inserted
            self._page_index[self._bank_index] = 0
            num_double_pages_before = num_double_pages
        if self._bank_index + num_double_pages_before < num_banks:
            bank_offset = (self._bank_index + num_double_pages_before) * num_controls
            page_offset = bank_offset + self._page_index[self._bank_index] * num_controls
            for control in self._parameter_controls:
                if page_offset < len(parameters_to_use):
                    control.connect_to(parameters_to_use[page_offset])
                else:  # inserted
                    control.release_parameter()
                page_offset += 1
                continue
            bank_names = []
            parameter_offset = 0
            for index in range(4):
                display_string = ' - '
                if index < num_banks:
                    if index < num_double_pages:
                        add_offset_before = index == self._bank_index and (self._page_index[index] == 0 or (index!= self._bank_index and self._page_index[index]!= 0))
                        if add_offset_before:
                            parameter_offset += num_controls
                        display_string = str(parameter_offset + 1).rjust(2) + '-' + str(parameter_offset + num_controls).rjust(2)
                        if not add_offset_before:
                            parameter_offset += num_controls
                        pass
                    else:  # inserted
                        display_string = str(parameter_offset + 1).rjust(2) + '-' + str(parameter_offset + num_controls).rjust(2)
                self._page_name_data_sources[index].set_display_string(display_string)
                parameter_offset += num_controls
                continue