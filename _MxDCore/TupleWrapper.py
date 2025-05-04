# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\TupleWrapper.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import old_hasattr

class TupleWrapper:
    pass
    _tuple_wrapper_registry = {}

    @staticmethod
    def forget_tuple_wrapper_instances():
        TupleWrapper._tuple_wrapper_registry = {}

    @staticmethod
    def get_tuple_wrapper(parent, attribute, element_filter=None, element_transform=None):
        if (parent, attribute) not in TupleWrapper._tuple_wrapper_registry:
            TupleWrapper._tuple_wrapper_registry[parent, attribute] = TupleWrapper(parent, attribute, element_filter, element_transform)
        return TupleWrapper._tuple_wrapper_registry[parent, attribute]

    def __init__(self, parent, attribute, element_filter=None, element_transform=None):
        self._parent = parent
        self._attribute = attribute
        self._element_filter = element_filter
        self._element_transform = element_transform

    def get_list(self):
        result = ()
        parent = self._parent
        if isinstance(parent, dict):
            if self._attribute in list(parent.keys()):
                result = parent[self._attribute]
            pass
        else:  # inserted
            if old_hasattr(parent, self._attribute):
                result = getattr(parent, self._attribute)
        <mask_6> = [e if self._element_filter(e) else None for e in result] if self._element_filter else [filtered_result for filtered_result in result]
        return list(map(self._element_transform, filtered_result)) if self._element_transform else filtered_result