import floppyforms.__future__ as forms
from django.utils.translation import ugettext_lazy as _
from django_backend.forms import FilterForm
from django_backend.forms import SearchFilterFormMixin
from django_backend.backend.base.backends import ModelBackend
from django_backend.backend.columns import BackendColumn
from django_backend import Group
from django_backend import site
from .models import Author
from .models import Post


blog = Group('blog')


class PostFilterForm(SearchFilterFormMixin, FilterForm):
    search_fields = ('title', 'text')
    author = forms.ModelChoiceField(
        label=_('Author'),
        queryset=Author.objects.all(),
        required=False)

    def filter_author(self, queryset, author):
        return queryset.filter(author=author)


class PostBackend(ModelBackend):
    filter_form_class = PostFilterForm

    def get_list_columns(self):
        columns = super(PostBackend, self).get_list_columns()
        columns.update({
            'author': BackendColumn(
                _('Author'),
                template_name='blog/django_backend/columns/_author.html',
                position=100
            ),
        })
        return columns


site.register(
    PostBackend,
    model=Post,
    id='post',
    group=blog,
)


# Here is an example of how to simply register a model as a backend by using
# the default model backend.

site.register(
    ModelBackend,
    model=Author,
    id='author',
    group=blog,
)


# We also want to make inline editing of the author possible from the post
# backend. That way we have more flexibility in the post backend to select the
# author, or create new ones from within the post backend.

site.register(
    ModelBackend,
    model=Author,
    registry='inline',
    id='author',
)
