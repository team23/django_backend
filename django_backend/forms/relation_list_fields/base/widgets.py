from django_backend.forms import InlineFormSetWidget


__all__ = ('BaseRelationListWidget',)


class BaseRelationListWidget(InlineFormSetWidget):
    """
    Base for other widgets that represent the m2m relation between to objects
    via a through model.
    """

    def __init__(self, *args, **kwargs):
        self.related_models = []
        super(BaseRelationListWidget, self).__init__(*args, **kwargs)

    def set_object_id_field_name(self, object_id_field_name):
        self.object_id_field_name = object_id_field_name

    def set_related_models(self, related_models):
        self.related_models = related_models

    def get_context_data(self):
        context_data = super(BaseRelationListWidget, self).get_context_data()
        context_data['related_models'] = self.related_models
        context_data['object_id_field_name'] = self.object_id_field_name
        context_data['relation_attribute'] = self.object_id_field_name
        return context_data
