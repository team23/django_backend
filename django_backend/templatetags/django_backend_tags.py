# -*- coding: utf-8 -*-
from django import template
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.base import token_kwargs
from django.template.loader import render_to_string
from django.template.defaultfilters import unordered_list
from django.utils.encoding import force_text
from django.core.urlresolvers import NoReverseMatch, reverse
import sys
import traceback

import django_backend
from ..backend import DEFAULT_REGISTRY


register = template.Library()


@register.filter
def model_opts(value):
    if hasattr(value, '_meta'):
        return value._meta
    return None


@register.filter
def normalize_space(value):
    import re
    return re.sub('\s+', ' ', value)


@register.filter
def choice_label(bound_field):
    field_value = force_text(bound_field.value())
    for value, label in bound_field.field.choices:
        if force_text(value) == field_value:
            return label
    return ''


@register.tag
def backend_url(parser, token):
    from django.template.base import kwarg_re
    from django.template.defaulttags import URLNode
    from django_backend import state

    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise template.TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    kwargs.setdefault('site', template.Variable('"%s"' % Site.objects.get_current().pk))
    kwargs.setdefault('language', template.Variable('"%s"' % state.language.active))

    return URLNode(viewname, args, kwargs, asvar)


@register.filter
def backend_url(obj, view_name):
    from django_backend import state

    registries = [
        'default',
        'pages',
        'components',
        'media',
        'structure',
        'utils',
        'admin',
    ]
    model = obj.__class__
    base_backend = django_backend.site.base

    for registry in registries:
        try:
            backend = base_backend.find(model=model, registry=registry)
            break
        except ValueError:
            pass
    # No backend was found.
    else:
        return ''

    try:
        urlname = backend.urlnames['views'][view_name].name
    except ValueError:
        # Cannot find view_name.
        return ''

    kwargs = {
        'site': Site.objects.get_current().pk,
        'language': getattr(obj, 'language', state.language.active),
    }
    try:
        return reverse(urlname, kwargs=kwargs)
    except NoReverseMatch:
        kwargs['pk'] = obj.pk
        return reverse(urlname, kwargs=kwargs)


class RandomIdNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        import random
        context[self.var_name] = str(random.randint(100000000, 999999999))
        return ''

    @classmethod
    def parse(cls, parser, tokens):
        '''
        {% randid as var %}
        '''
        bits = tokens.split_contents()
        tag_name = bits[0]
        values = bits[1:]
        if len(values) != 2:
            raise template.TemplateSyntaxError("%r tag requires two arguments ('as var')" % tag_name)
        if values[0] != 'as':
            raise template.TemplateSyntaxError("%r tag first argument must be 'as'" % tag_name)
        var_name = values[1]
        return cls(var_name)
register.tag('randid', RandomIdNode.parse)


class RenderNode(template.Node):
    def __init__(self, renderable, with_variables):
        self.renderable = renderable
        self.with_variables = with_variables

    def render(self, context):
        try:
            renderable = self.renderable.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if not hasattr(renderable, 'render'):
            return ''

        try:
            extra_context = dict([
                (name, var.resolve(context))
                for name, var in self.with_variables.items()])
            context.update(extra_context)

            return renderable.render(context)
        except Exception as exception:
            # Change in Renderable.render might have fixed this issue and we
            # might be able to remove this. But test first really hard that
            # really no errors are made silent.
            sys.stderr.write(
                "Exception during rendering renderable {renderable!r}: "
                "{type}: {exception}\n".format(
                    renderable=renderable,
                    type=type(exception).__name__,
                    exception=exception))
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info, **{'file': sys.stderr})
            sys.stderr.write('\n')
            raise
        finally:
            context.pop()

    @classmethod
    def parse(cls, parser, tokens):
        '''
        Renders a object in the current context. ::

            {% render object %} calls object.render(context)

        You can set some extra context with the 'with' argument::

            {% render object with value=1 %}
        '''
        bits = tokens.split_contents()
        tag_name = bits.pop(0)
        if not bits or bits[0] == 'with':
            raise template.TemplateSyntaxError(
                u'%r tag requires at least one argument' % tag_name)
        renderable = parser.compile_filter(bits.pop(0))

        if bits and bits[0] == 'with':
            bits.pop(0)
            arguments = token_kwargs(bits, parser, support_legacy=False)
            if not arguments:
                raise template.TemplateSyntaxError(
                    '"with" in %s tag needs at least one keyword argument.' %
                    tag_name)
            with_variables = arguments
        else:
            with_variables = {}

        return cls(renderable, with_variables)

register.tag('render', RenderNode.parse)


@register.filter
def resolve_form_field(form, fieldname):
    return form[fieldname]


@register.filter
def display_language(language_id):
    for id, name in settings.LANGUAGES:
        if id == language_id:
            return name
    return language_id


# TODO: There should be a nicer way to do this
@register.filter
def find_inline_backend_by_model(backend, model):
    if not callable(model):  # hack: Django calls objects it resolves in template context
        model = model.__class__
    return backend.find(model=model, registry='inline')


@register.filter
def find_backend(model, registries=DEFAULT_REGISTRY):
    # hack: Django calls objects it resolves in template context
    if not callable(model):
        model = model.__class__

    backend = django_backend.site.base

    for registry in registries.split(','):
        try:
            return backend.find(model=model, registry=registry)
        except ValueError:
            pass
    return None


@register.filter
def backend_has_list_permission(backend, user):
    # This was called with a set of backends, so we will check if we have any
    # permissions for those.
    if isinstance(backend, list):
        return any(
            backend_has_list_permission(single_backend, user)
            for single_backend in backend)

    return backend.has_perm(user, 'list')


@register.filter
def format_unordered_list(object_list, template_name):
    """
    Use django's `unordered_list` filter but use a template to render the
    items. The items are expected to be dicts and will be passed as context
    into the template.
    """
    def reformat_list(nested_list):
        new_list = []
        for item in nested_list:
            if isinstance(item, (list, tuple)):
                item = reformat_list(item)
            else:
                item = render_to_string(template_name, item)
            new_list.append(item)
        return new_list
    object_list = reformat_list(object_list)
    return unordered_list(object_list)


@register.filter('getattr')
def getattr_filter(object, attr):
    return getattr(object, attr)


@register.filter
def getattr_or_none(object, attr):
    return getattr(object, attr, None)


@register.filter
def backend_preview(object, backend):
    return backend.get_preview(object)


class PermissionHelper(object):
    def __init__(self, backend, user=None, perm=None, obj=None):
        self.backend = backend
        self.user = user
        self.perm = perm
        self.obj = obj

    def clone(self, **kwargs):
        cloned = self.__class__(
            self.backend,
            self.user,
            self.perm,
            self.obj)
        cloned.__dict__.update(kwargs)
        return cloned

    def __nonzero__(self):
        # These three things need to be set to actually test for a permission.
        if not self.backend or not self.user or not self.perm:
            return False
        return self.backend.has_perm(
            self.user,
            self.perm,
            self.obj)

    def __repr__(self):
        return '<{class_name}: {granted} backend={backend} user={user} perm={perm} obj={obj}>'.format(
            class_name=self.__class__.__name__,
            granted=self.__nonzero__(),
            **dict((key, repr(value)) for key, value in self.__dict__.items()))


@register.filter
def has_perm(backend, perm):
    '''
    This filter only makes sense with the for_user and for_object filter.
    It returns a helper which then must at least be passed to the for_user
    filter as well to get a truthy result. For checks.

    Examples:

        {% if backend|has_perm:"add"|for_user:user %}
            <a href="">Add new</a>
        {% endif %}

        {% if backend|has_perm:"change"|for_user:user|for_object:object %}
            <a href="">Change {{ object }}</a>
        {% endif %}

    There are a few shortcuts defined below, they can be used like this:

    Examples:

        {% if backend|has_add_permission:user %}
            <a href="">Add new</a>
        {% endif %}

        {% if backend|has_change_permission:user|for_object:object %}
            <a href="">Change {{ object }}</a>
        {% endif %}
    '''
    return PermissionHelper(backend, perm=perm)


@register.filter
def for_user(helper, user):
    return helper.clone(user=user)


@register.filter
def for_object(helper, obj):
    return helper.clone(obj=obj)


def create_permission_helper(perm):
    @register.filter('has_{perm}_permission'.format(perm=perm))
    def check(backend, user):
        return PermissionHelper(backend, user=user, perm=perm)
    return check


create_permission_helper('list')
create_permission_helper('read')
create_permission_helper('add')
create_permission_helper('change')
create_permission_helper('delete')
create_permission_helper('translate')
create_permission_helper('publish')
