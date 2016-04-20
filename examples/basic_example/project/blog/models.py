from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __unicode__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('Author', related_name='posts')
    title = models.CharField(max_length=50)
    text = models.TextField()

    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        return self.title
