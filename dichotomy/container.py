"""
"""

class Container(object):
    """
    """
    def __init__(self):
        self._instances = {}
        

    def register_instance(self, interface, instance):
        self._instances[interface] = instance


    def can_resolve(self, interface):
        return interface in self._instances


    def resolve(self, interface):
        return self._instances.get(interface)
