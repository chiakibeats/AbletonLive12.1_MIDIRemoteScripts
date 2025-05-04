# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\isclose.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

pass
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    pass
    if a == b:
        return True
    elif rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('error tolerances must be non-negative')
    elif math.isinf(abs(a)) or math.isinf(abs(b)):
        return False
    else:
        diff = abs(b - a)
        return diff <= abs(rel_tol * b) or diff <= abs(rel_tol * a) or diff <= abs_tol