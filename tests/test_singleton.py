import unittest

import pythern.singleton as singleton


class TestSingleton(unittest.TestCase):

    def test_singleton_metaclass_always_returns_same_instance(self):
        first_instance = SingletonType()
        second_instance = SingletonType()
        self.assertIs(first_instance, second_instance)



class SingletonType(metaclass=singleton.Singleton):
    pass



if __name__=="__main__":
    unittest.main()