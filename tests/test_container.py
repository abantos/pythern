import unittest
import dichotomy.container as container



class TestContainer(unittest.TestCase):

    def setUp(self):
        self.service = ServiceDouble()
        self.service_interface = 'service_double'
        self.container = container.Container()
        self.container.register_instance(self.service_interface, self.service)


    def test_can_register_an_instance(self):
        self.assertTrue(self.container.can_resolve(self.service_interface))


    def test_returns_false_if_instance_for_specified_interface_cannot_be_resolved(self):
        self.assertFalse(self.container.can_resolve('inexistent_instance'))


    def test_can_resolve_specified_instance(self):
        resolved_instance = self.container.resolve(self.service_interface)
        self.assertIs(resolved_instance, self.service)



class ServiceDouble(object):
    pass



if __name__=="__main__":
    unittest.main()