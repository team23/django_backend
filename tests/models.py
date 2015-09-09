from django.db import models


class PermissionTestModel(models.Model):
    pass


class OneFieldModel(models.Model):
    chars = models.CharField(max_length=50)
