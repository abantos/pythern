"""
This module contains an implementation of the `Singleton <https://en.wikipedia.org/wiki/Singleton_pattern>`_
pattern, which allows any type to be implemented as a Singleton.

One of the many problems with Singletons is that, in most naive implementations,
they violate the single responsibility principle because not only they provide
an interface to use the singleton instance, but they also need to handle the
lifetime of the object. On top of that, they make classes less reusable because
a type in a particular application might need to be a Singleton, but in the
context of another application the same type might not.

With this implementation, we try to avoid that problem by separating the concern
of managing the lifetime and instantiation of the object from the interface and
implementation. This doesn't strictly prevent other instances from being created
but provides a good idiom to communicate the intentions that there should only
be one instance. The following is an example on how this class should be used:

..  code-block:: python

    import dichotomy.singleton as core_singleton

    class RatingService(metaclass=core_singleton.Singleton):

        def __init__(self):
            self._instance = _RatingServiceImp()


        def instance(self):
            return self._instance


    
    class _RatingServiceImp:


        def rate(self, shipment_id):
            # rate the shipment

        
        def get_quote(self, shipment_id):
            # get quote for shipment


    RatingService().instance.rate(ship_id)
    RatingService().instance.get_quote(ship_id)


By declaring our ``RatingService`` class as having a metaclass of :class:`Singleton`,
we are insuring that every time we use the new object syntax as in ``RatingService()``
the call is forwarded to the :class:`Singleton` metaclass, which manages the
instantiation of the object if it has not been done before or returns the
existing object.

Then, we separate the implementation into a different class, ``_RatingServiceImp``
in our case, which allows us in the context of our application to use it as a
singleton, but nothing prevents us from using it as a normal class in other
applications.

If the implementation class is not suitable for reuse in other applications, like
the example above, it is recommended to make the class internal.

Alternatively, you can implement the full interface in the public class, in our
example ``RatingService``, but doing so it makes the class a Singleton in
any context or application where the class is used.
"""


class Singleton(type):
    """
    Metaclass that insures only one instance of a type is ever created. This
    class is intended to be used to declare Singleton types.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
