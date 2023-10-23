import unittest

from assertpy import assert_that

import pythern.container as container


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.service_interface = "service"
        self.object_type = Manager
        self.type_interface = "manager"
        self.composite_interface = "composite"
        self.composite_type = RegisteredCompositeObject
        self.container = container.Container()
        self.container.register_instance(self.service_interface, self.service)
        self.container.register_type(self.type_interface, self.object_type)
        self.container.register_type(self.composite_interface, self.composite_type)
        self.factory_interface = 'factory'
        self.factory = Factory()
        self.container.register_factory(self.factory_interface, self.factory, is_singleton=False)


    def test_can_register_an_instance(self):
        assert_that(self.container.can_resolve(self.service_interface)).is_true()

    def test_returns_false_if_instance_for_specified_interface_cannot_be_resolved(self):
        assert_that(self.container.can_resolve("inexistent_instance")).is_false()

    def test_can_resolve_specified_instance(self):
        resolved_instance = self.container.resolve(self.service_interface)
        assert_that(resolved_instance).is_same_as(self.service)

    def test_can_register_a_type(self):
        assert_that(self.container.can_resolve(self.type_interface)).is_true()

    def test_can_resolve_type_creating_instance_of_registered_type(self):
        instance = self.container.resolve(self.type_interface)
        assert_that(instance).is_instance_of(Manager)

    def test_resolves_type_dependencies_when_creating_instance(self):
        instance = self.container.resolve(self.composite_interface)
        assert_that(instance).is_instance_of(self.composite_type)
        assert_that(instance.service).is_same_as(self.service)
        assert_that(instance.manager).is_instance_of(self.object_type)

    def test_resolves_instance_of_specified_type_if_can_be_constructed(self):
        instance = self.container.resolve(CompositeObject)
        assert_that(instance).is_instance_of(CompositeObject)
        assert_that(instance.service).is_same_as(self.service)
        assert_that(instance.manager).is_instance_of(self.object_type)

    def test_returns_true_if_an_unregistered_type_can_be_resolved(self):
        assert_that(self.container.can_resolve(CompositeObject)).is_true()

    def test_returns_fals_if_an_unregistered_type_cannot_be_resolved(self):
        assert_that(self.container.can_resolve(UnresolvableObject)).is_false()

    def test_returns_none_if_unregistered_type_cannot_be_resolved(self):
        resolved = self.container.resolve(UnresolvableObject)
        assert_that(resolved).is_none()

    def test_can_register_a_factory(self):
        assert_that(self.container.can_resolve(self.factory_interface)).is_true()

    def test_factory_is_called_when_resolved(self):
        self.container.resolve(self.factory_interface)
        assert_that(self.factory.invoked_container).is_equal_to(self.container)

    def test_new_instance_is_created_if_not_singleton(self):
        instance_1 = self.container.resolve(self.factory_interface)
        instance_2 = self.container.resolve(self.factory_interface)
        assert_that(instance_1).is_not_same_as(instance_2)
        self.assertIsNot(instance_1, instance_2)

    def test_returns_single_instance_if_is_singleton(self):
        self.container.register_factory(self.factory_interface, self.factory, is_singleton=True)
        instance_1 = self.container.resolve(self.factory_interface)
        instance_2 = self.container.resolve(self.factory_interface)
        assert_that(instance_1).is_same_as(instance_2)
        self.assertIs(instance_1, instance_2)


class Service:
    pass


class Manager:
    pass


class RegisteredCompositeObject:
    def __init__(self, service, manager):
        self.service = service
        self.manager = manager


class CompositeObject:
    def __init__(self, service, manager):
        self.service = service
        self.manager = manager


class UnresolvableObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Factory:
    def __init__(self):
        self.invoked_container = None

    def __call__(self, container):
        self.invoked_container = container
        return Manager()



if __name__ == "__main__":
    unittest.main()
