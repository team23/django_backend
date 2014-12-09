from django import template
from django.utils.datastructures import MultiValueDict
from django.utils.html import conditional_escape as escape
from django.utils.encoding import smart_unicode, smart_str
from django.template.base import token_kwargs
import urllib

register = template.Library()


class QueryStringNode(template.Node):
    def __init__(self, variables, extends, varname):
        self.variables = variables
        self.extends = extends
        self.varname = varname

    def render(self, context):
        varname = self.varname
        try:
            extends = None
            if self.extends:
                extends = self.extends.resolve(context)
            variables = MultiValueDict()
            if self.variables:
                for key in self.variables:
                    for value in self.variables.getlist(key):
                        resolved_value = value.resolve(context)
                        if isinstance(resolved_value, (list, tuple, set)):
                            variables.setlist(key, resolved_value)
                        else:
                            variables.setlist(key, [resolved_value])
        except template.VariableDoesNotExist:
            return ''
        result = MultiValueDict()
        if extends:
            if isinstance(extends, MultiValueDict):
                result = extends.copy()
            else:
                for key in extends:
                    result[key] = extends[key]
        if variables:
            for key in variables:
                value = variables.getlist(key)
                if value == [None]:
                    if key in result:
                        del result[key]
                else:
                    result.setlist(key, variables.getlist(key))
        def _result_to_tuples():
            for key in result:
                for value in result.getlist(key):
                    yield (key, value)
        result = smart_unicode(
            urllib.urlencode([(smart_str(k), smart_str(v)) for k, v in _result_to_tuples()]))
        if varname:
            context[varname] = result
            return ''
        return escape(result)


@register.tag
def query_string(parser, token):
    '''
    {% query_string foo='bar' %}
    {% query_string foo='bar' extends request.GET %}
    {% query_string foo='bar' extends request.GET as query %}
    {% query_string foo='bar' extends request.GET as query dict %}
    {% query_string extends request.GET %}
    {% query_string foo='bar' as query dict %}
    {% query_string foo='bar' as query extends request.GET %}
    '''
    tokens = token.split_contents()
    tag_name = tokens[0]
    values = tokens[1:]
    variables = MultiValueDict()
    extends = None
    varname = None
    variables_finished = False
    try:
        i = 0
        num_values = len(values)
        while i < num_values:
            if values[i] == 'extends':
                variables_finished = True
                extends = parser.compile_filter(values[i + 1])
                i += 2
                continue
            if values[i] == 'as':
                variables_finished = True
                varname = values[i + 1]
                i += 2
                continue
            if variables_finished:
                raise template.TemplateSyntaxError(u'%r\'s parameters seem to be messed up, you mixed extra variables into the remainder.' % tag_name)
            parsed_variable = token_kwargs([values[i]], parser)
            if not parsed_variable:
                raise template.TemplateSyntaxError(u'%r\'s parameters seem to be messed up, some variable could not be parsed.' % tag_name)
            for k, v in parsed_variable.iteritems():
                variables.appendlist(k, v)
            i += 1
    except IndexError:
        raise template.TemplateSyntaxError(u'%r\'s parameters seem to be messed up, really bad.' % tag_name)
    return QueryStringNode(variables, extends, varname)


@register.filter
def append_to_params(params, value):
    return [v for v in params] + [value]


@register.filter
def remove_from_params(params, value):
    return [v for v in params if v != value]


@register.filter
def remove_param(params, key):
    '''
    {% query_string extends request.GET|remove_param:"page" %}
    '''
    # If it's an empty object (like None or ''), return it unaltered.
    if not params:
        return params
    params = params.copy()
    if key in params:
        del params[key]
    return params
