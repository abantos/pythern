"""
This module provides the implementation of a generic object factory. For most
practical cases, the provided interface will be suitable to use as it is, but
there might be some cases in which a derived class might provide a more
intuitive interface that will make the code more readable.

The following shows an example on how to use the :class:`ObjectBuilderFactory`
class as it is:

..  code-block:: python

    # in module accounting.py

    import dichotomy.object_factory as core_factory

    class StandardAccountingService(object):

        def add_invoice(self, invoice):
            # add the invoice


    class StandardAccountingServiceBuilder(object):

        def build(self, *args, **kwargs):
            return StandardAccountingService()


    class QuickBooksOnlineAccountingService(object):

        def __init__(self, qb_url):
            self._url = qb_url

        def add_invoice(self, invoice):
            # add the invoice online


    class QuickBooksOnlineAccountingServiceBuilder(object):

        def build(self, *args, **kwargs):
            url = kwargs.get('url')
            return QuickBooksOnlineAccountingService(url)


    factory = core_factory.ObjectBuilderFactory()

    
    factory.register_type('standard', StandardAccountingServiceBuilder())
    factory.register_type('QuickBooks', QuickBooksOnlineAccountingServiceBuilder())


    def get_accounting_service_factory():
        return factory


In the above code, we create two types of accounting services, and we
implement a builder class for each type that we register with the factory. We
also expose a ``get_accounting_service_factory()`` function to access the factory.
Client can now access the factory to get the correct service.

..  code-block:: python

    # in client.py

    import accounting

    def accounting_entry_point(**kwargs):
        accounting_service_type = kwargs.get('accounting_service_type')
        accounting_service_factory = accounting.get_accounting_service_factory()
        service = factory.create(accounting_service_type, **kwargs)
        invoice = Invoice()
        service.add_invoice(invoice)

The entry point takes some parameters that might differ depending on what service
we are using, but we don't have to deal with that because the builder will take
care of reading the information that needs to initialize the service and create
it. This way, the client code is implemented in the most generic way without
losing any flexibility.

As you can see the interface is self explanatory, but sometimes you may want to
make some improvements. The following example builds on top of what we already
implemented, but we are going to provide a nicer interface for the factory.
The service and builder classes remain the same, but we are going to derive a 
class from object factory:

..  code-block:: python

    # in accounting.py - code above ommitted.

    class AccountingServiceFactory(core_factory.ObjectBuilderFactory):

        def get_accounting_service(self, accounting_service_type):
            return super().create(accounting_service_type)


    factory = core_factory.AccountingServiceFactory()

    
    factory.register_type('standard', StandardAccountingServiceBuilder())
    factory.register_type('QuickBooks', QuickBooksOnlineAccountingServiceBuilder())


    def get_accounting_service_factory():
        return factory

We provide a new method ``get_accounting_service()``, which reads better and
is more specific. Now we can change the client code in the following way:

..  code-block:: python

    # in client.py

    import accounting

    def accounting_entry_point(**kwargs):
        accounting_service_type = kwargs.get('accounting_service_type')
        accounting_service_factory = accounting.get_accounting_service_factory()
        service = factory.get_accounting_service(accounting_service_type, **kwargs)
        invoice = Invoice()
        service.add_invoice(invoice)


The client code is basically the same, but now it reads ``get_accounting_service()``
as opposed to ``create()``, which doesn't really tell us whether a new service is
created or if it already exist, but as far as the client code is concerned, it
shouldn't matter.
"""

class ObjectBuilderFactory(object):
    """
    This class provides a flexible interface to create families of objects based
    on a specified ``type_id`` identifier and using a builder object that knows
    how to create and initialize the desired object.
    """
    def __init__(self):
        self._registered_types = {}
    
    def create(self, type_id, *args, **kwargs):
        """
        Creates a new object instance for the specified ``type_id`` using the
        provided positional and keyword arguments.

        :param str type_id:
            String identifier of the type to be created. This identifier should
            match a string used in :meth:`register_type` during registration.
        :param tuple args:
            Positional arguments to be forwarded to the registered builder.
        :param dict kwargs:
            Keyword arguments to be forwarded to the registered builder.

        :return:
            The object created by the registered builder.

        :raises ObjectTypeNotRegisteredError:
            An exception is raised when the specified type is not registered.
        """
        builder = self._registered_types.get(type_id)
        if not builder: raise ObjectTypeNotRegisteredError(type_id)
        _function = builder if callable(builder) else builder.build
        return _function(*args, **kwargs)


    def is_registered(self, type_id):
        """
        Returns whether the specified ``type_id`` is registered or not.

        :param str type_id:
            String identifier to test for registration.

        :return:
            True if the type is registered or False otherwise.
        """
        return type_id in self._registered_types


    def register_type(self, type_id, builder):
        """
        Registers a new builder under the specified object type, so the factory
        can create new instance of a class. This method does not check if the
        specified ``type_id`` already exists, so clients want to make sure
        the ``type_id`` specified is unique; otherwise, it will overwrite any
        previously registered builder.

        :param str type_id:
            String identifier for the new type.
        :param object builder:
            Builder object that knows how to construct the desired object for
            the specified type.

        The builder can either be an object that implements a ``build(*args, **kwargs)``
        method, or a callable object with the same signature. The following are
        examples of valid builders and their registrations:

        ..  code-block:: python

            class BuildMethodBuilder(object):

                def build(self, *args, **kwargs):
                    # Build and return specified object.

            
            class CallableClassBuilder(object):

                def __call__(self, *args, **kwargs):
                    # Build and return specified object.


            def as_function_builder(*args, **kwargs):
                # Build and return specified object.


            # We can even implement the builder interface in the actual class
            # we want to create.
            class SpecificObject(object):

                def __init__(self, *args, **kwargs):
                    # Initialize the object.


            factory.register_type('build_method', BuildMethodBuilder())
            factory.register_type('callable_class', CallableClassBuilder())
            factory.register_type('as_func', as_function_builder)
            factory.register_type('the_type', SpecificObject)
        """
        self._registered_types[type_id] = builder


    def unregister_type(self, type_id):
        """
        Unregisters a previously registered type. Trying to unregister a type
        that was not previously registered is not considered an error.

        :param str type_id:
            String identifier of the type to unregister.
        """
        return self._registered_types.pop(type_id)





class ObjectTypeNotRegisteredError(ValueError):
    """
    Exception class used to report errors when creating an object types through a
    factory that have not been registered.
    """
    def __init__(self, type_id):
        super().__init__(type_id)
        
