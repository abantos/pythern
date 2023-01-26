import unittest
import pythern.container as container



class TestContainer(unittest.TestCase):

    def setUp(self):
        self.service = Service()
        self.service_interface = 'service'
        self.object_type = Manager
        self.type_interface = 'manager'
        self.composite_interface = 'composite'
        self.composite_type = RegisteredCompositeObject
        self.container = container.Container()
        self.container.register_instance(self.service_interface, self.service)
        self.container.register_type(self.type_interface, self.object_type)
        self.container.register_type(self.composite_interface, self.composite_type)


    def test_can_register_an_instance(self):
        self.assertTrue(self.container.can_resolve(self.service_interface))


    def test_returns_false_if_instance_for_specified_interface_cannot_be_resolved(self):
        self.assertFalse(self.container.can_resolve('inexistent_instance'))


    def test_can_resolve_specified_instance(self):
        resolved_instance = self.container.resolve(self.service_interface)
        self.assertIs(resolved_instance, self.service)


    def test_can_register_a_type(self):
        self.assertTrue(self.container.can_resolve(self.type_interface))


    def test_can_resolve_type_creating_instance_of_registered_type(self):
        instance = self.container.resolve(self.type_interface)
        self.assertIsInstance(instance, Manager)


    def test_resolves_type_dependencies_when_creating_instance(self):
        instance = self.container.resolve(self.composite_interface)
        self.assertIsInstance(instance, self.composite_type)
        self.assertIs(instance.service, self.service)
        self.assertIsInstance(instance.manager, self.object_type)


    def test_resolves_instance_of_specified_type_if_can_be_constructed(self):
        instance = self.container.resolve(CompositeObject)
        self.assertIsInstance(instance, CompositeObject)
        self.assertIs(instance.service, self.service)
        self.assertIsInstance(instance.manager, self.object_type)


    def test_returns_true_if_an_unregistered_type_can_be_resolved(self):
        self.assertTrue(self.container.can_resolve(CompositeObject))


    def test_returns_fals_if_an_unregistered_type_cannot_be_resolved(self):
        self.assertFalse(self.container.can_resolve(UnresolvableObject))


    def test_returns_none_if_unregistered_type_cannot_be_resolved(self):
        resolved = self.container.resolve(UnresolvableObject)
        self.assertIsNone(resolved)



class Service(object):
    pass


class Manager(object):
    pass


class RegisteredCompositeObject(object):
    def __init__(self, service, manager):
        self.service = service
        self.manager = manager



class CompositeObject(object):
    def __init__(self, service, manager):
        self.service = service
        self.manager = manager



class UnresolvableObject(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
        



if __name__=="__main__":
    unittest.main()