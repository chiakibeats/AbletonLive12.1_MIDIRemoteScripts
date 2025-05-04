# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\selection.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
import Live

class Selection(object):
    pass

    @property
    def selected_device(self):
        pass
        raise NotImplementedError

    @property
    def selected_object(self):
        pass
        raise NotImplementedError

    @property
    def selected_track(self):
        pass
        raise NotImplementedError

    @property
    def selected_scene(self):
        pass
        raise NotImplementedError

    @property
    def hotswap_target(self):
        pass
        raise NotImplementedError

class PushSelection(Selection):
    pass
    pass

    def __init__(self, application=None, device_component=None, navigation_component=None, *a, **k):
        super(PushSelection, self).__init__(*a, **k)
        self._device_component = device_component
        self._navigation_component = navigation_component
        self._application = application
        self._browser = application.browser

    @property
    def selected_device(self):
        return self._device_component.device()

    def _get_selected_object(self):
        return self._navigation_component.selected_object

    def _set_selected_object(self, lom_object):
        if isinstance(lom_object, Live.DrumPad.DrumPad):
            lom_object.canonical_parent.view.selected_drum_pad = lom_object
        if isinstance(lom_object, Live.Chain.Chain):
            lom_object.canonical_parent.view.selected_chain = lom_object
            return
        else:
            self._application.get_document().view.select_device(lom_object, False)
    selected_object = property(_get_selected_object, _set_selected_object)

    @property
    def selected_track(self):
        return self._application.get_document().view.selected_track

    @property
    def hotswap_target(self):
        pass
        return self._browser.hotswap_target