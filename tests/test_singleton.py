import unittest

from assertpy import assert_that

import pythern.singleton as singleton


class TestSingleton(unittest.TestCase):

    def test_singleton_metaclass_always_returns_same_instance(self):
        first_instance = SingletonType()
        second_instance = SingletonType()
        assert_that(first_instance).is_same_as(second_instance)


class SingletonType(metaclass=singleton.Singleton):
    pass



if __name__=="__main__":
    unittest.main()