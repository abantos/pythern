import unittest

from assertpy import assert_that
import pytest

import pythern.object_factory as core_factory


class TestObjectBuilderFactory(unittest.TestCase):
    def setUp(self):
        super(TestObjectBuilderFactory, self).setUp()
        self.type_id = "the_id"
        self.test_builder = BuilderDouble()
        self.factory = core_factory.ObjectBuilderFactory()

    def test_raises_exception_creating_object_when_nothing_registered(self):
        with pytest.raises(core_factory.ObjectTypeNotRegisteredError):
            self.factory.create(self.type_id)

    def test_returns_true_if_type_is_registered(self):
        self.factory.register_type(self.type_id, self.test_builder)
        assert_that(self.factory.is_registered(self.type_id)).is_true()

    def test_returns_false_if_type_is_not_registered(self):
        assert_that(self.factory.is_registered("not_registered")).is_false()

    def test_can_unregister_a_previously_registered_type(self):
        self.factory.register_type(self.type_id, self.test_builder)
        self.factory.unregister_type(self.type_id)
        assert_that(self.factory.is_registered(self.type_id)).is_false()

    def test_can_create_registered_type(self):
        self.test_builder.object_to_build = 1
        self.factory.register_type(self.type_id, self.test_builder)
        new_object = self.factory.create(self.type_id)
        assert_that(new_object).is_same_as(1)

    def test_can_provide_positional_arguments_to_create_object(self):
        self.factory.register_type(self.type_id, self.test_builder)
        self.factory.create(self.type_id, 1, 2, 3)
        assert_that(self.test_builder.args).is_equal_to((1, 2, 3))

    def test_can_provide_keword_arguments_to_create_object(self):
        self.factory.register_type(self.type_id, self.test_builder)
        self.factory.create(self.type_id, a=1, b=2, c=3)
        assert_that(self.test_builder.kwargs).is_equal_to({"a": 1, "b": 2, "c": 3})

    def test_can_register_a_callable_as_a_builder(self):
        self.callable_method_called = False
        self.factory.register_type(self.type_id, self.callable_method)
        self.factory.create(self.type_id)
        assert_that(self.callable_method_called).is_true()

    def callable_method(self, *args, **kwargs):
        self.callable_method_called = True


class BuilderDouble:
    def __init__(self):
        self.object_to_build = None

    def build(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self.object_to_build


if __name__ == "__main__":
    unittest.main()
