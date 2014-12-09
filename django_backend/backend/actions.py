from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.translation import ungettext


class Action(object):
    name = None

    def __init__(self, name=None, position=0):
        self.name = name or self.name
        self.position = position

    def get_required_permissions(self):
        return []

    def check_permission(self, backend, user, obj=None):
        '''
        Return ``True`` if the action can be performed by the given user.

        ``obj`` will be ``None`` if the check is performed in the list view,
        wether to actually offer this action in the list.

        ``obj`` is given when the action is actually going to be performed on
        an individual object.
        '''
        return all(
            backend.has_perm(user, perm, obj)
            for perm in self.get_required_permissions())

    def perform(self, backend, request, queryset):
        raise NotImplementedError(
            'Actions need to implement the `perform` method.')


class ObjectActionException(Exception):
    pass

