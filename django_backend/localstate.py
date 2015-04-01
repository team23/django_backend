# -*- coding: utf-8 -*-
from threading import local


class LocalState(object):
    '''
    Usage::

        >>> language = LocalState()
        # in thread 1
        >>> language.active is None
        True
        >>> language.active = 'de'
        # in thread 2
        >>> language.active
        None
        >>> language.active == 'en'
        >>> language.active
        'en'
        # in thread 1 again
        >>> language.active
        'de'

    Override the ``get_active`` and ``activate`` methods to provide custom
    getter and setter for the ``active`` attribute.
    '''

    def __init__(self, default=None):
        self._local = local()
        self.default = default
        self.data = self._local.__dict__

    def get_active(self):
        if 'active' in self.data:
            return self.data['active']
        return self.get_default()

    def get_default(self):
        if callable(self.default):
            return self.default()
        return self.default

    def activate(self, value):
        self.data['active'] = value

    def active():
        def fget(self):
            return self.get_active()
        def fset(self, value):
            return self.activate(value)
        def fdel(self):
            if 'active' in self.data:
                del self.data['active']
        return fget, fset, fdel
    active = property(*active())
