# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\event.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
import weakref
from functools import partial, wraps
from itertools import chain, repeat
from .abl_signal import Signal
from .disconnectable import CompoundDisconnectable, Disconnectable
from .live_api_utils import liveobj_valid
from .util import NamedTuple, instance_decorator, monkeypatch, monkeypatch_extend, old_hasattr
__all__ = ('EventObject', 'Event', 'EventError', 'listenable_property', 'listens', 'listens_group', 'Slot', 'SlotGroup', 'MultiSlot', 'has_event', 'validate_event_interface')

class EventError(Exception):
    pass  # postinserted
class Event(NamedTuple):
    pass
    name = None
    pass
    doc = ''
    pass
    signal = Signal
    pass
    override = False

def add_event(cls, event_name_or_event):
    pass
    if isinstance(event_name_or_event, str):
        event = Event(name=event_name_or_event)
    else:  # inserted
        event = event_name_or_event
    signal_attr = '_' + event.name + '_signal'

    def get_signal(self):
        try:
            return getattr(self, signal_attr)
        except AttributeError:
            signal = event.signal(sender=self)
            setattr(self, signal_attr, signal)
            return signal
    kwargs = dict({'doc': event.doc, 'override': event.override})

    @monkeypatch(cls, event.name + '_has_listener', **kwargs)
    def has_method(self, slot):
        return get_signal(self).is_connected(slot)

    @monkeypatch(cls, 'add_' + event.name + '_listener', **kwargs)
    def add_method(self, slot, identify_sender=False, *a, **k):
        sender = self if identify_sender else None
        return get_signal(self).connect(slot, *a, sender=sender, **k)

    @monkeypatch(cls, 'remove_' + event.name + '_listener', **kwargs)
    def remove_method(self, slot):
        return get_signal(self).disconnect(slot)

    @monkeypatch(cls, 'notify_' + event.name, **kwargs)
    def notify_method(self, *a, **k):
        return get_signal(self)(*a, **k)

    @monkeypatch(cls, event.name + '_listener_count', **kwargs)
    def listener_count_method(self):
        return get_signal(self).count

    @monkeypatch_extend(cls)
    def disconnect(self):
        get_signal(self).disconnect_all()

def validate_event_interface(obj, event_name):
    pass
    if not callable(getattr(obj, 'add_' + event_name + '_listener', None)):
        raise EventError('Object %s missing \"add\" method for event: %s' % (obj, event_name))
    else:  # inserted
        if not callable(getattr(obj, 'remove_' + event_name + '_listener', None)):
            raise EventError('Object %s missing \"remove\" method for event: %s' % (obj, event_name))
        else:  # inserted
            if not callable(getattr(obj, event_name + '_has_listener', None)):
                raise EventError('Object %s missing \"has\" method for event: %s' % (obj, event_name))
            else:  # inserted
                return None

def has_event(obj, event_name):
    pass
    return callable(getattr(obj, 'add_' + event_name + '_listener', None)) and callable(getattr(obj, 'remove_' + event_name + '_listener', None)) and callable(getattr(obj, event_name + '_has_listener', None))

class listenable_property_base(object):
    pass

    def set_property_name(self, name):
        pass
        return

class EventObjectMeta(type):
    pass

    @staticmethod
    def collect_listenable_properties(dct):
        return list(filter(lambda item: isinstance(item[1], listenable_property_base), dct.items()))

    def __new__(cls, name, bases, dct):
        listenable_properties = EventObjectMeta.collect_listenable_properties(dct)
        for property_name, obj in listenable_properties:
            obj.set_property_name(property_name)
        events = dct.get('__events__', [])
        property_events = [event_name for event_name, obj in listenable_properties]
        has_events = events or property_events
        if has_events and 'disconnect' not in dct:
            dct['disconnect'] = lambda self: super(cls, self).disconnect()
        cls = super(EventObjectMeta, cls).__new__(cls, name, bases, dct)
        for lst in chain(events, property_events):
            add_event(cls, lst)
        return cls

class EventObject(CompoundDisconnectable, metaclass=EventObjectMeta):
    pass

    def register_slot(self, *a, **k):
        pass
        slot = a[0] if a and isinstance(a[0], Slot) else Slot(*a, **k)
        self.register_disconnectable(slot)
        return slot

class Slot(Disconnectable):
    pass
    _extra_kws = {}
    _extra_args = []
    pass
    pass
    pass
    pass
    pass
    def __init__(self, subject=None, listener=None, event_name=None, extra_kws=None, extra_args=None, *a, **k):
        super(Slot, self).__init__(*a, **k)
        self._event_name = event_name
        if extra_kws is not None:
            self._extra_kws = extra_kws
        if extra_args is not None:
            self._extra_args = extra_args
        self._subject = None
        self._listener = None
        self.subject = subject
        self.listener = listener

    def subject_valid(self, subject):
        pass
        return liveobj_valid(subject)

    def disconnect(self):
        pass
        self.subject = None
        self.listener = None
        super(Slot, self).disconnect()

    def connect(self):
        pass
        if not self.is_connected and self.subject_valid(self._subject) and (self._listener is not None):
                    add_method = getattr(self._subject, 'add_' + self._event_name + '_listener')
                    all_args = tuple(self._extra_args) + (self._listener,)
                    try:
                        add_method(*all_args, **self._extra_kws)
                    except RuntimeError:
                        return None
                else:  # inserted
                    return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def soft_disconnect(self):
        pass
        if self.is_connected and self.subject_valid(self._subject) and (self._listener is not None):
                    all_args = tuple(self._extra_args) + (self._listener,)
                    remove_method = getattr(self._subject, 'remove_' + self._event_name + '_listener')
                    try:
                        remove_method(*all_args)
                    except RuntimeError:
                        return None
            else:  # inserted
                return

    @property
    def is_connected(self):
        pass
        all_args = tuple(self._extra_args) + (self._listener,)
        connected = False
        try:
            connected = bool(self.subject_valid(self._subject) and self._listener is not None and getattr(self._subject, self._event_name + '_has_listener')(*all_args))
        except RuntimeError:
            pass
        return connected

    @property
    def subject(self):
        pass
        return self._subject

    @subject.setter
    def subject(self, subject):
        if subject!= self._subject:
            if self.subject_valid(subject):
                validate_event_interface(subject, self._event_name)
            self.soft_disconnect()
            self._subject = subject
            self.connect()

    @property
    def listener(self):
        pass
        return self._listener

    @listener.setter
    def listener(self, listener):
        if listener!= self._listener:
            self.soft_disconnect()
            self._listener = listener
            self.connect()

    def __call__(self, *a, **k):
        if self._listener is not None:
            return self._listener(*a, **k)
        else:  # inserted
            return None

class SlotGroup(EventObject):
    pass
    listener = None
    _extra_kws = None
    _extra_args = None
    pass
    def __init__(self, listener=None, event_name=None, extra_kws=None, extra_args=None, *a, **k):
        super(SlotGroup, self).__init__(*a, **k)
        self.listener = listener
        self._event_name = event_name
        if listener is not None:
            self.listener = listener
        if extra_kws is not None:
            self._extra_kws = extra_kws
        if extra_args is not None:
            self._extra_args = extra_args

    def replace_subjects(self, subjects, identifiers=repeat(None)):
        pass
        self.disconnect()
        for subject, identifier in zip(subjects, identifiers):
            self.add_subject(subject, identifier=identifier)

    def add_subject(self, subject, identifier=None):
        pass
        if identifier is None:
            identifier = subject
        listener = self._listener_for_subject(identifier)
        self.register_slot(subject, listener, self._event_name, self._extra_kws, self._extra_args)

    def remove_subject(self, subject):
        pass
        slot = self.find_disconnectable(lambda x: x.subject == subject)
        self.disconnect_disconnectable(slot)

    def has_subject(self, subject):
        pass
        return liveobj_valid(self.find_disconnectable(lambda x: x.subject == subject))

    def _listener_for_subject(self, identifier):
        return lambda *a, **k: self.listener and self.listener(*a + (identifier,), **k)

    def __call__(self, *a, **k):
        return self.listener(*a, **k)

class MultiSlot(EventObject, Slot):
    pass
    pass
    pass
    pass
    pass
    pass
    def __init__(self, subject=None, listener=None, event_name_list=None, extra_kws=None, extra_args=None, *a, **k):
        self._original_listener = listener
        self._slot_subject = None
        self._nested_slot = None
        super(MultiSlot, self).__init__(event_name=event_name_list[0], listener=self._event_fired, subject=subject, extra_kws=extra_kws, extra_args=extra_args)
        if len(event_name_list) > 1:
            self._nested_slot = self.register_disconnectable(MultiSlot(event_name_list=event_name_list[1:], listener=listener, extra_kws=extra_kws, extra_args=extra_args))
            self._update_nested_subject()

    @property
    def subject(self):
        pass
        return super(MultiSlot, self).subject

    @subject.setter
    def subject(self, subject):
        pass  # cflow: irreducible

    def _event_fired(self, *a, **k):
        self._update_nested_subject()
        self._original_listener(*a, **k)

    def _update_nested_subject(self):
        if self._nested_slot is not None:
            self._nested_slot.subject = getattr(self._slot_subject, self._event_name) if self.subject_valid(self._slot_subject) else None

    def __call__(self, *a, **k):
        return self._original_listener(*a, **k)

def listens(event_path, *a, **k):
    pass
    @instance_decorator
    def decorator(self, method):
        event_name_list = event_path.split('.')
        if len(event_name_list) > 1:
            slot = wraps(method)(MultiSlot(event_name_list=event_name_list, extra_kws=k, extra_args=a, listener=partial(method, self)))
        else:  # inserted
            slot = wraps(method)(Slot(event_name=event_path, extra_kws=k, extra_args=a, listener=partial(method, self)))
        self.register_slot(slot)
        return slot
    return decorator

def listens_group(event_name, *a, **k):
    pass
    @instance_decorator
    def decorator(self, method):
        slot = wraps(method)(SlotGroup(event_name=event_name, extra_kws=k, extra_args=a, listener=partial(method, self)))
        self.register_disconnectable(slot)
        return slot
    return decorator

class listenable_property(listenable_property_base, property):
    pass

    @classmethod
    def managed(cls, default_value):
        pass
        return _managed_listenable_property(default_value=default_value)

class _managed_listenable_property(listenable_property_base):
    def __init__(self, default_value=None, *a, **k):
        super(_managed_listenable_property, self).__init__(*a, **k)
        self._default_value = default_value
        self._property_name = None
        self._member_name = None

    def set_property_name(self, property_name):
        self._property_name = property_name
        self._member_name = '__listenable_property_%s' % property_name

    def _get_value(self, obj):
        return getattr(obj, self._member_name, self._default_value)

    def __get__(self, obj, owner):
        return self._get_value(obj)

    def __set__(self, obj, value):
        if value!= self._get_value(obj):
            setattr(obj, self._member_name, value)
            getattr(obj, 'notify_%s' % self._property_name)(value)

class SerializableListenablePropertiesMeta(EventObjectMeta):
    def __new__(cls, name, bases, dct):
        listenable_properties = EventObjectMeta.collect_listenable_properties(dct)

        def getstate(self):
            data = super(generated_class, self).__getstate__()
            data.update(dict(((property_name, getattr(self, property_name)) for property_name, _ in listenable_properties)))
            return data

        def setstate(self, data):
            for k, v in data.items():
                setattr(self, k, v)
        dct['__getstate__'] = getstate
        dct['__setstate__'] = setstate
        generated_class = super(SerializableListenablePropertiesMeta, cls).__new__(cls, name, bases, dct)
        return generated_class

class SerializableListenablePropertiesBase(Disconnectable):
    def __getstate__(self):
        return dict()

    def __setstate__(self, data):
        return

class SerializableListenableProperties(SerializableListenablePropertiesBase, metaclass=SerializableListenablePropertiesMeta):
    pass  # postinserted
class ObservablePropertyAlias(EventObject):
    pass
    pass
    pass
    pass
    def __init__(self, alias_host, property_host=None, property_name='', alias_name=None, getter=None, *a, **k):
        super(ObservablePropertyAlias, self).__init__(*a, **k)
        self._alias_host = weakref.ref(alias_host)
        self._alias_name = alias_name or property_name
        self._property_host = property_host
        self._property_name = property_name
        self._property_slot = None
        self._setup_alias(getter)

    def _get_property_host(self):
        return self._property_host

    def _set_property_host(self, host):
        self._property_host = host
        self._property_slot.subject = host
    property_host = property(_get_property_host, _set_property_host)

    def _setup_alias(self, getter):
        aliased_prop = property(getter or self._get_property)
        alias_host = self._alias_host()
        if alias_host:
            setattr(alias_host.__class__, self._alias_name, aliased_prop)
            notifier = getattr(alias_host, 'notify_' + self._alias_name)
            self._property_slot = self.register_slot(Slot(self.property_host, notifier, self._property_name))

    def _get_property(self, _):
        return getattr(self.property_host, self._property_name, None)