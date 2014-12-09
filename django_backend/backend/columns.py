from django.template.loader import render_to_string


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
        return render_to_string(self.template_name, {
            'column': self,
        }, context)
