# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\ControlSurfaceWrapper.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

import weakref
import Live
from ableton.v2.base import EventObject, old_hasattr
from ableton.v2.control_surface import MessageScheduler, defaults

def is_real_control_surface(lom_object):
    return is_local_control_surface(lom_object) or isinstance(lom_object, Live.Application.ControlSurfaceProxy)

def is_local_control_surface(lom_object):
    from _Framework.ControlSurface import ControlSurface
    from ableton.v2.control_surface import SimpleControlSurface as ControlSurface2
    from ableton.v3.control_surface import ControlSurface as ControlSurface3
    return isinstance(lom_object, (ControlSurface, ControlSurface2, ControlSurface3))

def wrap(control_surface):
    if is_local_control_surface(control_surface):
        return LocalControlSurfaceWrapper(control_surface=control_surface)
    elif isinstance(control_surface, Live.Application.ControlSurfaceProxy):
        return RemoteControlSurfaceWrapper(proxy=control_surface)
    else:
        return None

class WrapperRegistry:

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._wrapper_registry = {}

    def wrap(self, obj):
        if is_real_control_surface(obj):
            try:
                return self._wrapper_registry[obj]
            except KeyError:
                wrapped = wrap(obj)
                self._wrapper_registry[obj] = wrapped
                try:
                    obj.add_disconnect_listener(self.__on_control_surface_disconnected)
                except AttributeError:
                    pass
                return wrapped
        else:
            return obj

    def clear(self):
        for wrapper in self._wrapper_registry.values():
            wrapper.disconnect()
        self._wrapper_registry = {}

    def __on_control_surface_disconnected(self, unwrapped_cs):
        try:
            unwrapped_cs.remove_disconnect_listener(self.__on_control_surface_disconnected)
            self._wrapper_registry[unwrapped_cs].disconnect()
            del self._wrapper_registry[unwrapped_cs]
        except KeyError:
            return None

class ControlSurfaceWrapper:
    pass

    def disconnect(self):
        raise NotImplementedError

    @property
    def canonical_parent(self):
        return

    @property
    def type_name(self):
        raise NotImplementedError

    @property
    def control_names(self):
        raise NotImplementedError

    def has_control(self, control):
        raise NotImplementedError

    def get_control_by_name(self, control_name):
        raise NotImplementedError

    def grab_control(self, control):
        raise NotImplementedError

    def release_control(self, control):
        raise NotImplementedError

class LocalControlSurfaceWrapper(ControlSurfaceWrapper):
    pass

    def __init__(self, control_surface=None, *a, **k):
        super().__init__(*a, **k)
        self._control_surface = control_surface
        self._grabbed_controls = []

    @property
    def __doc__(self):
        return self._control_surface.__doc__

    def set_control_element(self, control, grabbed):
        pass
        if old_hasattr(control, 'release_parameter'):
            control.release_parameter()
        control.reset()

    def disconnect(self):
        pass

    def __getattr__(self, name):
        return getattr(self._control_surface, name)

    def __setattr__(self, name, value):
        if name not in ['_control_surface', '_grabbed_controls']:
            setattr(self._control_surface, name, value)
            return
        else:
            super().__setattr__(name, value)

    def __eq__(self, other):
        return self._control_surface == other

    def __hash__(self):
        return hash(self._control_surface)

    @property
    def type_name(self):
        return self._control_surface.__class__.__name__

    @property
    def control_names(self):
        return [control.name for control in self._control_surface.controls if old_hasattr(control, 'name') and control.name]

    def has_control(self, control):
        return control in self._control_surface.controls

    def get_control_by_name(self, control_name):
        for control in self._control_surface.controls:
            if old_hasattr(control, 'name') and control.name == control_name:
                return control
            else:
                continue
        return None

    def grab_control(self, control):
        pass

    def release_control(self, control):
        pass

class ControlProxyBase(EventObject):
    pass
    __events__ = ('value',)

class ControlProxy(ControlProxyBase):

    def __init__(self, name='', id=None, proxy=None, parent=None, *a, **k):
        super().__init__(*a, **k)
        self._name = name
        self._id = id
        self._proxy = proxy
        self._parent = parent

    @property
    def canonical_parent(self):
        return self._parent

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    def send_value(self, *a):
        self._proxy.send_value((self._id, a))

    def receive_value(self, value):
        self.notify_value(*value)

    def add_value_listener(self, listener):
        original_count = self.value_listener_count()
        super().add_value_listener(listener)
        if original_count == 0 and self.value_listener_count() > 0:
            self._proxy.subscribe_to_control(self._id)

    def remove_value_listener(self, listener):
        original_count = self.value_listener_count()
        super().remove_value_listener(listener)
        if self._proxy and original_count > 0 and (self.value_listener_count() == 0):
            self._proxy.unsubscribe_from_control(self._id)

class RemoteControlSurfaceWrapper(ControlSurfaceWrapper):

    def __init__(self, proxy=None, *a, **k):
        super().__init__(*a, **k)
        self._proxy = proxy
        self._control_proxies = {desc.name: ControlProxy(name=desc.name, id=desc.id, proxy=self._proxy, parent=self) for desc in proxy.control_descriptions}
        self._control_proxies_by_id = {p.id: p for p in self._control_proxies.values()}
        proxy.add_control_values_arrived_listener(self.__on_control_values_arrived)
        proxy.add_midi_received_listener(self.__on_midi_received)

        class Timer:
            MS_PER_TICK = defaults.TIMER_DELAY * 1000

            def __init__(self):
                self._timer_instance = None

            def start(self, timeout, callback):
                self_ref = weakref.ref(self)

                def callback_wrapper():
                    callback()
                    if self_ref:
                        self_ref().cancel()
                self._timer_instance = Live.Base.Timer(callback=callback_wrapper, interval=int((timeout + 1) * self.MS_PER_TICK), start=True)

            def cancel(self):
                try:
                    self._timer_instance.stop()
                except AttributeError:
                    pass
                self._timer_instance = None

            def disconnect(self):
                self.cancel()
        self._timer = Timer()
        self.mxd_midi_scheduler = MessageScheduler(send_message_callback=self._proxy.send_midi, timer=self._timer, on_state_changed_callback=self._on_mxd_midi_scheduler_state_changed)

    @property
    def timer_instance(self):
        return self._timer._timer_instance

    def disconnect(self):
        self._timer.disconnect()
        self._proxy.enable_receive_midi(False)
        self._proxy.remove_control_values_arrived_listener(self.__on_control_values_arrived)
        self._proxy.remove_midi_received_listener(self.__on_midi_received)

    def __eq__(self, other):
        return self._proxy == other

    def __hash__(self):
        return hash(self._proxy)

    @property
    def type_name(self):
        return self._proxy.type_name

    @property
    def control_names(self):
        return tuple((c.name for c in self._proxy.control_descriptions))

    def _on_mxd_midi_scheduler_state_changed(self, new_state):
        self._proxy.enable_receive_midi(new_state in ['grabbed', 'wait', 'grabbed_wait'])

    def __on_control_values_arrived(self):
        for control_id, value in self._proxy.fetch_received_values():
            try:
                self._control_proxies_by_id[control_id].receive_value(value)
            except KeyError:
                continue
            else:
                continue

    def __on_midi_received(self):
        for message in self._proxy.fetch_received_midi_messages():
            self.mxd_midi_scheduler.handle_message(message)

    def has_control(self, control):
        return control in self._control_proxies.values()

    def get_control_by_name(self, control_name):
        return self._control_proxies.get(control_name)

    def grab_control(self, control):
        if control.id in self._control_proxies_by_id:
            self._proxy.grab_control(control.id)
            return
        else:
            return None

    def release_control(self, control):
        if control.id in self._control_proxies_by_id:
            self._proxy.release_control(control.id)
            return
        else:
            return None