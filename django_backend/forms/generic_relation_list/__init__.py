"""
The "generic_relation_list" module shall give a simple way to manage a list of
data that is associated with a m2m through model that holds a generic foreign
key. For example:

::

    class ListOfStuff(models.Model):
        pass

    class ListItem(models.Model):
        list = models.ForeignKey(ListOfStuff)
        position = models.IntegerField(default=0)

        content_type = models.ForeignKey(ContentType)
        object_id = models.PositiveIntegerField()
        content_object = GenericForeignKey('content_type', 'object_id')

That means that ``ListOfStuff`` can take multiple ``ListItem`` where a
``ListItem`` holds a generic foreign key to an arbitrary model instance. That
way you can assemble a list of random things. The GenericRelationListField
provides an easy to use form field that let's you add new items and edit the
existing ones in place.
"""

from .fields import *  # noqa
from .widgets import *  # noqa
