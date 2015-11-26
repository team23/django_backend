from django_backend.forms import InlineFormSetWidget


__all__ = ('GenericRelationListWidget',)


class GenericRelationListWidget(InlineFormSetWidget):
    template_name = (
        'django_backend/generic_relation_list_field/'
        'generic_relation_list_field.html'
    )

    def __init__(self, *args, **kwargs):
        self.related_models = []
        super(GenericRelationListWidget, self).__init__(*args, **kwargs)

    def set_related_models(self, related_models):
        self.related_models = related_models

    def get_context_data(self):
        context_data = super(GenericRelationListWidget, self).get_context_data()
        context_data['related_models'] = self.related_models
        return context_data
