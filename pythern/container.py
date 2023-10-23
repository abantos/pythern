"""
"""
import inspect
from collections import namedtuple


_FactoryInfo = namedtuple('FactoryInfo', ['factory', 'is_singleton'])

class Container:
    """ """

    def __init__(self):
        self._factories = {}
        self._instances = {}
        self._types = {}

    def register_factory(self, interface, factory, is_singleton=False):
        self._factories[interface] = _FactoryInfo(factory=factory, is_singleton=is_singleton)

    def register_instance(self, interface, instance):
        """ """
        self._instances[interface] = instance

    def register_type(self, interface, type_class):
        """ """
        self._types[interface] = type_class

    def can_resolve(self, interface):
        """ """
        return (
            interface in self._instances
            or interface in self._types
            or interface in self._factories
            or self._can_resolve_type(interface)
        )

    def resolve(self, interface):
        """ """
        if interface in self._instances:
            return self._instances.get(interface)
        if interface in self._types:
            type_class = self._types.get(interface)
            return self._create_instance(type_class)
        if interface in self._factories:
            return self._create_instance_from_factory(interface)
        return self._create_instance(interface)

    def _create_instance(self, type_class):
        if self.can_resolve(type_class):
            instances = self._collect_type_arguments(type_class, self.resolve)
            return type_class(*instances)

    def _create_instance_from_factory(self, interface):
        factory_info = self._factories.get(interface)
        instance = factory_info.factory(self)
        if factory_info.is_singleton:
            self._instances[interface] = instance
        return instance

    def _can_resolve_type(self, type_class):
        return (
            self._can_arguments_be_resolved(type_class)
            if isinstance(type_class, type)
            else False
        )

    def _can_arguments_be_resolved(self, type_class):
        can_resolve_arguments = self._collect_type_arguments(
            type_class, self.can_resolve
        )
        return False not in can_resolve_arguments

    def _collect_type_arguments(self, type_class, collect_func):
        type_arguments = inspect.getfullargspec(type_class.__init__).args
        return [collect_func(argument) for argument in type_arguments[1:]]
