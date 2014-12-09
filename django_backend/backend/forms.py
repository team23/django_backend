# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
import floppyforms.__future__ as forms


class ActionForm(forms.Form):
    action = forms.ChoiceField(label=_('Action'), choices=())
    objects = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.MultipleHiddenInput,
        required=False)

    def __init__(self, *args, **kwargs):
        self.actions = kwargs.pop('actions')
        self.queryset = kwargs.pop('queryset')
        super(ActionForm, self).__init__(*args, **kwargs)
        self.fields['action'].choices = self.get_action_choices()
        self.fields['objects'].queryset = self.queryset

    def get_action_choices(self):
        return [('', _(u'Select an action …'))] + [
            (key, action.name)
            for key, action in self.actions.items()]

    def get_selected_queryset(self):
        return self.cleaned_data['objects']

    def perform_action(self, backend, request):
        action_slug = self.cleaned_data['action']
        action = self.actions[action_slug]
        queryset = self.get_selected_queryset()
        action.perform(backend, request, queryset)


class SortForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.list_columns = kwargs.pop('list_columns')
        super(SortForm, self).__init__(*args, **kwargs)
        self.fields['order_by'] = forms.ChoiceField(
            choices=self.get_order_by_choices(),
            widget=forms.HiddenInput)

    def get_order_by_choices(self):
        choices = []
        for column in self.list_columns.values():
            if column.sort_field:
                choices.append((
                    column.sort_field,
                    column.name,
                ))
                choices.append((
                    column.reverse_sort_field,
                    column.name,
                ))
        return choices

    def sort_queryset(self, queryset):
        if self.is_valid():
            order_by = self.cleaned_data.get('order_by')
            if order_by:
                queryset = queryset.order_by(order_by)
        return queryset
