# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\Profile.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial, wraps
ENABLE_PROFILING = False
if ENABLE_PROFILING:
    import cProfile
    PROFILER = cProfile.Profile()

def profile(fn):
    pass
    if ENABLE_PROFILING:

        @wraps(fn)
        def wrapper(self, *a, **k):
            if PROFILER:
                return PROFILER.runcall(partial(fn, self, *a, **k))
            else:
                print('Can not profile (%s), it is probably reloaded' % fn.__name__)
                return fn(*a, **k)
        return wrapper
    else:
        return fn

def dump(name='default'):
    import pstats
    fname = name + '.profile'
    PROFILER.dump_stats(fname)

    def save_human_data(sort):
        s = pstats.Stats(fname, stream=open('%s.%s.txt' % (fname, sort), 'w'))
        s.sort_stats(sort)
        s.print_stats()
    save_human_data('time')
    save_human_data('cumulative')