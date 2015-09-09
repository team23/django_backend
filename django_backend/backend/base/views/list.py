from django.http import HttpResponseRedirect
from django.views.generic import ListView
from ...views import BackendModelViewMixin


class ActionFormMixin(BackendModelViewMixin):
    def pre_dispatch(self, request, *args, **kwargs):
        self.action_form = self.get_action_form()
        return super(ActionFormMixin, self).pre_dispatch(request, *args,
                                                         **kwargs)

    def post(self, request, *args, **kwargs):
        if self.action_form is None:
            return self.http_method_not_allowed(request, *args, **kwargs)

        if self.action_form.is_valid():
            self.action_form.perform_action(self.backend, request)
            return HttpResponseRedirect(request.path)
        return self.get(request, *args, **kwargs)

    def get_action_form_class(self):
        return self.backend.get_action_form_class()

    def get_action_form(self):
        actions = self.backend.get_available_list_actions(self.request.user)
        if actions:
            kwargs = {
                'actions': actions,
                'queryset': self.get_queryset(),
            }
            action_form_class = self.get_action_form_class()
            if self.request.method == 'POST':
                return action_form_class(self.request.POST, **kwargs)
            else:
                return action_form_class(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs['action_form'] = self.action_form
        return super(ActionFormMixin, self).get_context_data(**kwargs)


class BackendListView(ActionFormMixin, BackendModelViewMixin, ListView):
    template_type = 'list'

    def get_required_permissions(self):
        return super(BackendListView, self).get_required_permissions() + ['list']

    def init_dispatch(self, request, *args, **kwargs):
        self.filter_form = self.get_filter_form()
        self.sort_form = self.get_sort_form()
        super(BackendListView, self).init_dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        return self.backend.paginate_by

    def get_filter_form_class(self):
        return self.backend.get_filter_form_class()

    def get_filter_form(self):
        filter_form_class = self.get_filter_form_class()
        if filter_form_class is None:
            return
        return filter_form_class(self.request.GET)

    def get_sort_form_class(self):
        return self.backend.get_sort_form_class()

    def get_sort_form(self, list_columns=None):
        sort_form_class = self.get_sort_form_class()
        if sort_form_class is None:
            return
        # TODO: Support self.backend.order_by tuple?
        sort_form_data = {
            'order_by': self.backend.order_by,
        }
        if 'order_by' in self.request.GET:
            sort_form_data['order_by'] = self.request.GET['order_by']
        if list_columns is None:
            list_columns = self.backend.list_columns
        return sort_form_class(
            sort_form_data,
            list_columns=list_columns)

    def get_context_data(self, **kwargs):
        kwargs['filter_form'] = self.filter_form
        kwargs['sort_form'] = self.sort_form
        return super(BackendListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        queryset = super(BackendListView, self).get_queryset()

        # Filter the queryset.
        if self.filter_form and self.filter_form.is_valid():
            queryset = self.filter_form.filter_queryset(queryset)

        # Apply backend order_by
        if self.backend.order_by:
            order_by = self.backend.order_by
            if not isinstance(order_by, (list, tuple)):
                order_by = (order_by,)
            queryset = queryset.order_by(*order_by)

        # Sort the queryset.
        if self.sort_form and self.sort_form.is_valid():
            queryset = self.sort_form.sort_queryset(queryset)

        return queryset
