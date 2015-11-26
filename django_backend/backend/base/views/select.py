from django.contrib.contenttypes.models import ContentType

from .list import BackendListView


class SelectViewMixin(object):
    template_type = 'select'

    # Don't check for permissions in this mixin. This mixin will only be used
    # with BackendListViews which checks for the 'list' permission.

    def get_select_queryset(self, queryset):
        '''
        The returned queryset are the objects that might be selected in the
        list. This might by different to what is listed.

        This is usefull if you want to allow special selections in like in the
        visibility backend.
        '''
        return queryset

    def get_json(self, **kwargs):
        json = super(SelectViewMixin, self).get_json(**kwargs)
        object_id = self.request.POST.get('object_id', None)
        if object_id is not None:
            queryset = self.get_select_queryset(self.object_list)
            queryset = queryset.filter(pk=object_id)
            if queryset.exists():
                self.object = queryset.get()
                json.update({
                    'action': 'select',
                    'object_id': self.object.pk,
                    'content_type_id': ContentType.objects.get_for_model(
                        self.object).pk,
                    'preview': self.get_preview(self.object),
                })
        return json

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class BackendSelectView(SelectViewMixin, BackendListView):
    pass
