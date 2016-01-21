from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
import floppyforms.__future__ as forms
import operator


__all__ = ('FilterForm', 'SearchFilterFormMixin',)


class FilterForm(forms.Form):
    """
    Use as base class for filter forms in backends. Define new search fields in
    subclasses and write the corresponding ``filter_queryset_{field_name}``
    methods in order to filter the given queryset by the chosen value.
    """

    def filter_queryset(self, queryset):
        for field_name in self.fields:
            filter_method_name = 'filter_queryset_%s' % field_name
            filter_method = getattr(self, filter_method_name, None)
            if filter_method is not None:
                data = self.cleaned_data.get(field_name)
                queryset = filter_method(queryset, data)
        return queryset


class SearchFilterFormMixin(forms.Form):
    search_fields = None

    search = forms.CharField(label=_('Search'), required=False)

    def filter_queryset_search(self, queryset, search):
        assert self.search_fields is not None, (
            "`search_fields` not defined on {form}".format(self=self))
        if search:
            queryset = queryset.filter(
                reduce(operator.or_, (
                    Q(**{'{}__icontains'.format(field): search})
                    for field in self.search_fields)))
        return queryset
