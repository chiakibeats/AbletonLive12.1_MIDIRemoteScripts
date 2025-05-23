# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\model\declaration.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.builtins import long, unicode
from itertools import count
from ableton.v2.base import old_hasattr

class ModelDeclarationException(Exception):
    pass

class WrongIdPropertyDeclaration(ModelDeclarationException):
    pass

class ViewModelsCantContainRefs(ModelDeclarationException):
    pass

class UndeclaredReferenceClass(ModelDeclarationException):
    pass

class ViewModelCantContainListModels(ModelDeclarationException):
    pass

def is_view_model_property_decl(decl):
    try:
        return issubclass(decl.property_type, ViewModel)
    except TypeError:
        return False

def is_list_property_decl(decl):
    return isinstance(decl.property_type, listof)

def is_list_model_property_decl(decl):
    return isinstance(decl.property_type, listmodel)

def is_binding_property_decl(decl):
    try:
        return issubclass(decl.property_type, Binding)
    except TypeError:
        return False

def is_reference_property_decl(decl):
    return isinstance(decl.property_type, ref)

def is_value_property_type(decl):
    return decl.property_type in (int, long, float, unicode, str, bool)

def is_custom_property(decl):
    return isinstance(decl, custom_property)

class property_declaration(object):
    pass

class view_property(property_declaration):
    sentinel = object()
    GLOBAL_ORDER = count()

    def __init__(self, property_type, default_value=sentinel, depends=(), *a, **k):
        super(view_property, self).__init__(*a, **k)
        self.property_type = property_type
        self.default_value = default_value
        self.order = next(self.GLOBAL_ORDER)
        depends = depends

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.property_type)

    def visit(self, name, visitor):
        if name == 'id':
            raise WrongIdPropertyDeclaration
        else:
            visitor.visit_view_property(name, self)

class custom_property(view_property):

    def __init__(self, property_type, wrapper_class=None, *a, **k):
        super(custom_property, self).__init__(*a, property_type=property_type, **k)
        self.wrapper_class = wrapper_class

    def visit(self, name, visitor):
        if name == 'id':
            raise WrongIdPropertyDeclaration
        else:
            visitor.visit_custom_property(name, self)

class id_property(property_declaration):
    property_type = int
    default_value = -1
    order = -1

    @staticmethod
    def id_attribute_getter(obj):
        if old_hasattr(obj, '__id__'):
            return unicode(obj.__id__)
        elif old_hasattr(obj, '_live_ptr'):
            return unicode(obj._live_ptr)
        else:
            return unicode(id(obj))

    def visit(self, name, visitor):
        if name != 'id':
            raise WrongIdPropertyDeclaration
        else:
            visitor.visit_id_property(name, self)

class listof(object):

    def __init__(self, property_type, *a, **k):
        super(listof, self).__init__(*a, **k)
        self.property_type = property_type

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.property_type)

class listmodel(listof):
    pass

class ModelVisitor(object):

    def visit_class(self, class_):
        if issubclass(class_, Binding):
            self.visit_binding_class(class_)
            return
        else:
            self.visit_viewmodel_class(class_)

    def visit_binding_class(self, class_):
        self.visit_class_declarations(class_)

    def visit_viewmodel_class(self, class_):
        self.visit_class_declarations(class_)

    def visit_class_declarations(self, class_):
        view_properties = ((name, decl) for name, decl in class_.__dict__.items() if isinstance(decl, property_declaration))
        for name, decl in sorted(view_properties, key=lambda item: item[1].order):
            decl.visit(name, self)

    def visit_id_property(self, name, decl):
        return

    def visit_view_property(self, name, decl):
        if is_reference_property_decl(decl):
            self.visit_reference_property(name, decl)
        elif is_binding_property_decl(decl):
            self.visit_binding_property(name, decl)
        elif is_value_property_type(decl):
            self.visit_value_property(name, decl)
            return
        elif is_view_model_property_decl(decl):
            self.visit_view_model_property(name, decl)
            return
        elif is_list_property_decl(decl):
            self.visit_list_property(name, decl)
            return
        else:
            raise Exception('Invalid property declaration')

    def visit_reference_property(self, name, decl):
        return

    def visit_value_property(self, name, decl):
        return

    def visit_binding_property(self, _name, decl):
        self.visit_class(decl.property_type)

    def visit_view_model_property(self, _name, decl):
        self.visit_class(decl.property_type)

    def visit_list_property(self, name, decl):
        if is_reference_property_decl(decl.property_type):
            self.visit_reference_list_property(name, decl, decl.property_type.property_type)
        elif is_value_property_type(decl.property_type):
            self.visit_value_list_property(name, decl, decl.property_type.property_type)
        elif is_list_model_property_decl(decl):
            self.visit_list_model_property(name, decl, decl.property_type.property_type)
            return
        elif is_view_model_property_decl(decl.property_type):
            self.visit_complex_list_property(name, decl, decl.property_type.property_type)
            return
        else:
            raise Exception('Invalid property declaration')

    def visit_value_list_property(self, name, decl, value_type):
        return

    def visit_custom_property(self, name, decl):
        return

    def visit_list_model_property(self, _name, _decl, value_type):
        self.visit_class(value_type)

    def visit_complex_list_property(self, _name, _decl, value_type):
        self.visit_class(value_type)

    def visit_reference_list_property(self, name, decl, reference_name):
        return

class ModelMeta(type):

    def visit(cls, visitor):
        visitor.visit_class(cls)

class ViewModel(metaclass=ModelMeta):
    pass

class Binding(ViewModel):
    pass

class ref(object):

    def __init__(self, class_name, *a, **k):
        super(ref, self).__init__(*a, **k)
        self.class_name = class_name