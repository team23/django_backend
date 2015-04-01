from django_backend.permissions import ModelBackendPermissions
from .models import PermissionTestModel


ModelBackendPermissions(PermissionTestModel).register()
