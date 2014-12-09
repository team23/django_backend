# -*- coding: utf-8 -*-
from django import template

register = template.Library()


class PageSlicesNode(template.Node):
    def __init__(self, page, varname, slice_length, edge_length):
        self.page = page
        self.varname = varname
        self.slice_length = slice_length
        self.edge_length = edge_length

    def render(self, context):
        try:
            page_obj = self.page.resolve(context)
            if isinstance(self.slice_length, int):
                slice_length = self.slice_length
            else:
                slice_length = self.slice_length.resolve(context)
            if isinstance(self.edge_length, int):
                edge_length = self.edge_length
            else:
                edge_length = self.edge_length.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        pages = page_obj.paginator.num_pages
        page = page_obj.number
        page_slices = []
        start_slice_lower = 1
        start_slice_upper = min(edge_length + 1, pages + 1)
        middle_slice_lower = max(page - (slice_length // 2), 1)
        middle_slice_upper = min(middle_slice_lower + slice_length, pages + 1)
        end_slice_lower = max(pages - edge_length + 1, 1)
        end_slice_upper = pages + 1
        if start_slice_upper + 1 >= middle_slice_lower:
            if middle_slice_upper + 1 >= end_slice_lower:
                page_slices.append(range(start_slice_lower, end_slice_upper))
            else:
                page_slices.append(range(start_slice_lower, middle_slice_upper))
                page_slices.append(range(end_slice_lower, end_slice_upper))
        elif middle_slice_upper + 1 >= end_slice_lower:
            page_slices.append(range(start_slice_lower, start_slice_upper))
            page_slices.append(range(middle_slice_lower, end_slice_upper))
        else:
            page_slices.append(range(start_slice_lower, start_slice_upper))
            page_slices.append(range(middle_slice_lower, middle_slice_upper))
            page_slices.append(range(end_slice_lower, end_slice_upper))
        context[self.varname] = page_slices
        return ''


@register.tag
def page_slices(parser, token):
    '''
    {% page_slices page as slices %}
    {% page_slices page as slices by 5 %}
    {% page_slices page as slices by 5 3 %}
    '''
    tokens = token.split_contents()
    tag_name = tokens[0]
    values = tokens[1:]
    if not len(values) in (3, 5, 6):
        raise template.TemplateSyntaxError("%r tag requires three, five or six arguments" % tag_name)
    page = parser.compile_filter(values[0])
    if not values[1] == 'as':
        raise template.TemplateSyntaxError("%r tag requires second argument to be 'as'" % tag_name)
    varname = values[2]
    if len(values) in (5, 6):
        if not values[3] == 'by':
            raise template.TemplateSyntaxError("%r tag requires fourth argument to be 'by'" % tag_name)
        slice_length = parser.compile_filter(values[4])
        if len(values) == 6:
            edge_length = parser.compile_filter(values[5])
        else:
            edge_length = 3
    else:
        slice_length = 5
        edge_length = 3
    return PageSlicesNode(page, varname, slice_length, edge_length)

