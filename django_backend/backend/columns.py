from django.template import Context
from django.template.loader import render_to_string

from ..compat import context_flatten


class BackendColumn(object):
    def __init__(self, name, template_name, position=0, sort_field=None):
        self.name = name
        self.template_name = template_name
        self.position = position
        self.sort_field = sort_field

    @property
    def reverse_sort_field(self):
        if self.sort_field is not None:
            return '-{0}'.format(self.sort_field)

    def render(self, context):
        context_data = {}
        if isinstance(context, Context):
            context = context_flatten(context)
        context_data.update(context)
        context_data.update({
            'column': self,
        })
        return render_to_string(self.template_name, context_data)
