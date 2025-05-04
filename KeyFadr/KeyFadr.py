# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyFadr\KeyFadr.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from KeyPad import KeyPad

class KeyFadr(KeyPad):
    pass
    _encoder_range = list(range(80, 72, -1))
    _product_model_id = 102

    def __init__(self, *a, **k):
        super(KeyFadr, self).__init__(*a, **k)