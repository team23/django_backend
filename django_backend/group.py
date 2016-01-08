from django.forms.forms import pretty_name
from django.template import Context
from django.template.loader import render_to_string

from .compat import context_flatten


class Group(list):
    """
    A simplistic representation of backends that are related and should be
    displayed as one "group" in the backend (e.g. as one box in the sidebar).
    """

    template_name = 'django_backend/_group.html'

    def __init__(self, id, name=None, position=0, template_name=None):
        self.id = id
        if name is None:
            name = pretty_name(id)
        self.template_name = template_name or self.template_name
        self.name = name
        self.position = position
        super(Group, self).__init__()

    @property
    def backends(self):
        return list(self)

    def get_context_data(self, context, **kwargs):
        data = {
            'group': self,
        }
        data.update(kwargs)
        return data

    def get_template_name(self):
        return self.template_name

    def render(self, context):
        context_data = {}
        if isinstance(context, Context):
            context_data.update(context_flatten(context))
        context_data = self.get_context_data(context, **context_data)
        return render_to_string(self.get_template_name(), context_data)
