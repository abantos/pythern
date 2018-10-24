import unittest
import dichotomy.container as container



class TestContainer(unittest.TestCase):

    def test_can_register_an_instance(self):
        self.container = container.Container()
        self.container.register_instance('service_double', ServiceDouble())
        self.assertTrue(self.container.can_create('service_double'))


class ServiceDouble(object):
    pass



if __name__=="__main__":
    unittest.main()