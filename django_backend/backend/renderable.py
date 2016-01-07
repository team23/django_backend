from django.template import Context
from django.template.loader import render_to_string

from ..compat import context_flatten


class Renderable(object):
    """
    Interface for an object that can be rendered with the {% render object %}
    template tag. The {% render %} tag will call the Renderable.render() method
    with the current template context as first argument. The result of this
    method will be shown in the template.

    The Renderable uses a template to render itself. It is given with the class
    attribute ``template_name``. ``template_name`` can be a list of templates
    which are tried in order to and the first existing one is used. Also the
    template names can use string formatting to fill in placeholders. See the
    ``RenderableModelInstance`` for an elaborate example.
    """
    template_name = None

    def __init__(self, template_name=None):
        self.template_name = template_name or self.template_name

    def get_template_name_context(self, context):
        """
        ``context`` is the template context that is currently used. This method
        should then return a dictionary which can be used for string formatting
        in template names.
        """
        return {}

    def get_template_name(self, context):
        template_names = self.template_name
        if not isinstance(template_names, (tuple, list)):
            template_names = [template_names]
        name_context = self.get_template_name_context(context)
        return [
            template_name.format(**name_context)
            for template_name in template_names
        ]

    def get_context_data(self, context, **kwargs):
        data = {}
        data.update(kwargs)
        return data

    def render(self, context=None):
        if context is None:
            context = {}
        if isinstance(context, Context):
            context = context_flatten(context)

        context_data = {}
        context_data.update(context)
        context_data.update(self.get_context_data(context))

        # We cannot pass a ``Context`` instance from the Django template
        # language down here directly. This is deprecated! And we had a bug
        # where a ``TemplateDoesNotExist`` error was swallowed during
        # rendering. And that was super annoying since no error at all was spit
        # out.
        return render_to_string(
            self.get_template_name(context),
            context_data)


class RenderableModelInstance(Renderable):
    """
    Example::

        class AdminChangeList(RenderableModelInstance):
            template_name = [
                'admin/{app_label}/{object_name}/change_list.html',
                'admin/{app_label}/change_list.html',
                'admin/change_list.html',
            ]
    """

    def get_template_name_context(self, context):
        name_context = {}
        if 'object' in context:
            instance = context['object']
            name_context.update({
                'app_label': instance._meta.app_label,
                'object_name': instance._meta.object_name.lower(),
            })
        return name_context
