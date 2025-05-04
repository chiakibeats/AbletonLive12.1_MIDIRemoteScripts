# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\Util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
from contextlib import contextmanager
from functools import partial, reduce, wraps
from itertools import chain, zip_longest
from numbers import Number
from ableton.v2.base import old_hasattr

def clamp(val, minv, maxv):
    return max(minv, min(val, maxv))

def linear(minv, maxv, val):
    return minv + (maxv - minv) * val

def nop(*a, **k):
    if a:
        return a[0]
    else:
        return None

def negate(value):
    return not value

def const(value):
    return lambda *a, **k: value

def in_range(value, lower_bound, upper_open_bound):
    if not isinstance(value, Number):
        return False
    else:
        return value >= lower_bound and value < upper_open_bound

def sign(value):
    return 1.0 if value >= 0.0 else -1.0

def to_slice(obj):
    return obj if isinstance(obj, slice) else slice(obj, obj + 1) if obj != -1 else slice(obj, None)

def slice_size(slice, width):
    return len(list(range(width))[slice])

def maybe(fn):
    return lambda x: fn(x) if x is not None else None

def memoize(function):
    pass
    memoized = {}

    @wraps(function)
    def wrapper(*args):
        try:
            ret = memoized[args]
        except KeyError:
            ret = memoized[args] = function(*args)
        return ret
    return wrapper

@memoize
def mixin(*args):
    pass
    if len(args) == 1:
        return args[0]
    else:
        name = 'Mixin_%s' % '_'.join((cls.__name__ for cls in args))
        return type(str(name), args, {})

def monkeypatch(target, name=None, override=False, doc=None):
    pass

    def patcher(func):
        patchname = func.__name__ if name is None else name
        if not override and old_hasattr(target, patchname):
            raise TypeError('Class %s already has method %s' % (target.__name__, patchname))
        else:
            setattr(target, patchname, func)
            try:
                func.__name__ = str(patchname)
            except AttributeError:
                pass
            if doc is not None:
                func.__doc__ = doc
            return func
    return patcher

def monkeypatch_extend(target, name=None):
    pass

    def patcher(func):
        newfunc = func
        patchname = func.__name__ if name is None else name
        if old_hasattr(target, patchname):
            oldfunc = getattr(target, patchname)
            if not callable(oldfunc):
                raise TypeError('Can not extend non callable attribute')
            else:

                @wraps(oldfunc)
                def extended(*a, **k):
                    ret = oldfunc(*a, **k)
                    func(*a, **k)
                    return ret
                newfunc = extended
        setattr(target, patchname, newfunc)
        return func
    return patcher

def instance_decorator(decorator):
    pass

    class Decorator(object):

        def __init__(self, func=nop, *args, **kws):
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
            self._data_name = '%s_%d_decorated_instance' % (func.__name__, id(self))
            self._func = func
            self._args = args
            self._kws = kws

        def __get__(self, obj, cls=None):
            if obj is None:
                return
            else:
                data_name = self._data_name
                try:
                    return obj.__dict__[data_name]
                except KeyError:
                    decorated = decorator(obj, self._func, *self._args, **self._kws)
                    obj.__dict__[data_name] = decorated
                    return decorated
    return Decorator

def forward_property(member):
    pass

    class Descriptor(object):

        def __init__(self, func_or_name):
            self._property_name = func_or_name.__name__ if callable(func_or_name) else func_or_name

        def __get__(self, obj, cls=None):
            return getattr(getattr(obj, member), self._property_name)

        def __set__(self, obj, value):
            return setattr(getattr(obj, member), self._property_name, value)
    return Descriptor

class lazy_attribute(object):
    pass

    def __init__(self, func, name=None):
        wraps(func)(self)
        self._func = func
        if name:
            self.__name__ = name

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        else:
            result = obj.__dict__[self.__name__] = self._func(obj)
            return result

def remove_if(predicate, lst):
    pass
    return [elem for elem in lst if not predicate(elem)]

def flatten(list):
    pass
    return chain(*list)

def group(lst, n):
    pass
    return list(zip_longest(*[lst[i::n] for i in range(n)]))

def find_if(predicate, seq):
    pass
    for x in seq:
        if predicate(x):
            return x
        else:
            continue
    return None

def index_if(predicate, seq):
    pass
    idx = 0
    for x in seq:
        if predicate(x):
            return idx
        else:
            idx += 1
            continue
    return idx

def union(a, b):
    pass
    a = dict(a)
    a.update(b)
    return a

def product(iter_a, iter_b):
    if False:
        pass
    for a in iter_a:
        for b in iter_b:
            yield (a, b)
        continue

def next(iter):
    pass
    return iter.__next__()

def is_iterable(value):
    pass
    try:
        it = iter(value)
        return bool(it)
    except TypeError:
        return False

def recursive_map(fn, element, sequence_type=None):
    pass
    if sequence_type is None:
        return recursive_map(fn, element, type(element))
    elif isinstance(element, sequence_type):
        return [recursive_map(fn, x, sequence_type) for x in element]
    else:
        return fn(element)

def chain_from_iterable(iterables):
    if False:
        pass
    for it in iterables:
        for element in it:
            yield element
        continue

def is_matrix(iterable):
    pass
    if is_iterable(iterable) and len(iterable) > 0:
        return all(map(lambda x: is_iterable(x) and len(iterable[0]) == len(x) and (len(x) > 0), iterable))
    else:
        return False

def first(seq):
    return seq[0]

def second(seq):
    return seq[1]

def third(seq):
    return seq[2]

def compose(*funcs):
    pass
    return lambda x: reduce(lambda x, f: f(x), funcs[::-1], x)

def is_contextmanager(value):
    return callable(getattr(value, '__enter__', None)) and callable(getattr(value, '__exit__', None))

def infinite_context_manager(generator):
    pass
    make_context_manager = contextmanager(generator)

    class InfiniteContextManager(object):

        def __enter__(self):
            self._delegate = make_context_manager()
            self._delegate.__enter__()

        def __exit__(self, type, err, trace):
            self._delegate.__exit__(type, err, trace)
            del self._delegate
    return InfiniteContextManager

class BooleanContext(object):
    pass
    default_value = False

    def __init__(self, default_value=None, *a, **k):
        super(BooleanContext, self).__init__(*a, **k)
        if default_value is not None:
            self.default_value = default_value
        self._current_value = self.default_value

    def __bool__(self):
        return bool(self._current_value)

    def __call__(self, update_value=None):
        pass
        return self.Manager(self, update_value)

    @property
    def value(self):
        return self._current_value

    class Manager(object):

        def __init__(self, managed=None, update_value=None, *a, **k):
            super(BooleanContext.Manager, self).__init__(*a, **k)
            self._managed = managed
            self._update_value = update_value if update_value is not None else not managed.default_value

        def __enter__(self):
            managed = self._managed
            self._old_value = managed._current_value
            managed._current_value = self._update_value
            return self

        def __exit__(self, *a, **k):
            self._managed._current_value = self._old_value

def dict_diff(left, right):
    pass
    dummy = object()
    return dict([k_v for k_v in iter(right.items()) if left.get(k_v[0], dummy) != k_v[1]])

class NamedTuple(object):
    pass

    def __init__(self, *others, **k):
        super(NamedTuple, self).__init__()
        for other in others:
            diff = dict_diff(self._eq_dict, other._eq_dict)
            self._eq_dict.update(diff)
            self.__dict__.update(diff)
        self.__dict__.update(k)
        if '_eq_dict' in self.__dict__:
            self._eq_dict.update(k)

    def __setattr__(self, name, value):
        raise AttributeError('Named tuple is constant')

    def __delattr__(self, name):
        raise AttributeError('Named tuple is constant')

    def __getitem__(self, name):
        return self.__dict__[name]

    @lazy_attribute
    def _eq_dict(self):

        def public(objdict):
            return dict([k__ for k__ in iter(objdict.items()) if not k__[0].startswith('_')])
        return reduce(lambda a, b: union(b, a), [public(c.__dict__) for c in self.__class__.__mro__], public(self.__dict__))

    def __eq__(self, other):
        return isinstance(other, NamedTuple) and self._eq_dict == other._eq_dict

    def __hash__(self):
        return hash(id(self))

    def __getstate__(self):
        res = dict(self.__dict__)
        try:
            del res['_eq_dict']
        except KeyError:
            pass
        return res

class Slicer(object):
    pass

    def __init__(self, dimensions=1, extractor=nop, keys=tuple(), *a, **k):
        super(Slicer, self).__init__(*a, **k)
        self._keys = keys
        self._dimensions = dimensions
        self._extractor = extractor

    def __getitem__(self, key):
        new = key if isinstance(key, tuple) else (key,)
        keys = self._keys + new
        if len(keys) == self._dimensions:
            return self._extractor(*keys)
        else:
            return Slicer(dimensions=self._dimensions, extractor=self._extractor, keys=keys)

    def __call__(self):
        return self
get_slice = Slicer()

def slicer(dimensions):
    pass

    def decorator(extractor):

        @wraps(extractor)
        def make_slicer(*a, **k):
            return Slicer(dimensions=dimensions, extractor=partial(extractor, *a, **k))
        return make_slicer
    return decorator

def print_message(*messages):
    print(' '.join(map(str, messages)))

class overlaymap(object):
    pass

    def __init__(self, *maps):
        self._maps = maps

    def __getitem__(self, key):
        for m in self._maps:
            if key in m:
                return m[key]
            else:
                pass
                continue
        raise KeyError(key)

    def keys(self):
        res = set()
        for key in chain_from_iterable(self._maps):
            res.add(key)
        return list(res)

    def values(self):
        return [self[key] for key in list(self.keys())]

    def items(self):
        for key in list(self.keys()):
            yield (key, self[key])

def trace_value(value, msg='Value: '):
    pass
    print(msg, value)
    return value

class Bindable(object):
    pass
    _bound_instances = None

    def __get__(self, obj, cls=None):
        import weakref
        if obj is None:
            return self
        else:
            if self._bound_instances is None:
                self._bound_instances = weakref.WeakKeyDictionary()
            bound_dict = self._bound_instances.setdefault(obj, weakref.WeakKeyDictionary())
            try:
                bound = bound_dict[self]
            except KeyError:
                bound = self.bind(weakref.proxy(obj))
                bound_dict[self] = bound
            return bound

    def bind(self, bind_to_object):
        raise NotImplementedError