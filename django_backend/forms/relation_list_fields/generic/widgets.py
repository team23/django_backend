from ..base import BaseRelationListWidget


__all__ = ('GenericRelationListWidget',)


class GenericRelationListWidget(BaseRelationListWidget):
    template_name = (
        'django_backend/relation_list_fields/'
        'generic_relation_list_field.html'
    )

    def __init__(self, *args, **kwargs):
        self.content_type_field_name = 'content_type'
        super(GenericRelationListWidget, self).__init__(*args, **kwargs)

    def set_content_type_field_name(self, content_type_field_name):
        self.content_type_field_name = content_type_field_name

    def get_context_data(self):
        context_data = super(GenericRelationListWidget, self).get_context_data()
        context_data['content_type_field_name'] = self.content_type_field_name
        context_data['relation_attribute'] = 'content_object'
        return context_data
