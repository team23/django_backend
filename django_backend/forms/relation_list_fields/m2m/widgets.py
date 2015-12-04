from ..base import BaseRelationListWidget


__all__ = ('M2MListWidget',)


class M2MListWidget(BaseRelationListWidget):
    template_name = (
        'django_backend/relation_list_fields/'
        'm2m_list_field.html'
    )
