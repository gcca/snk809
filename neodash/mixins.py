# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import Iterator, List, Optional

from django.contrib.auth import models as auth_models
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Model

__all__ = ("PermissionsAppMixin", "PermissionsModelMixin")


class UserAppPermissionsMixinBase(UserPassesTestMixin):
    app_label: Optional[str] = None

    def _user_permissions(self) -> List[str]:
        if self.app_label is None:
            raise AttributeError(
                f"You need to define the `app_label` member in {self}"
            )
        return [
            permission
            for permission in self.request.user.get_all_permissions()
            if permission.startswith(self.app_label)
        ]

    def _model_permissions(self, **kwargs) -> Iterator[str]:
        return (
            ".".join(values)
            for values in auth_models.Permission.objects.filter(
                content_type__app_label=self.app_label, **kwargs
            ).values_list("content_type__app_label", "codename")
        )


class PermissionsAppMixin(UserAppPermissionsMixinBase):
    """Verify that the current user has the app permissions.

    Temporal use. Apply until decide permissions per view or actions.
    """

    app_label: Optional[str] = None

    def test_func(self):
        if self.app_label is None:
            raise AttributeError(
                f"You need to define the `app_label` member in {self}"
            )
        user_permissions = self._user_permissions()
        return self.request.user.is_active and all(
            permission in user_permissions
            for permission in self._model_permissions()
        )


class PermissionsModelMixin(UserAppPermissionsMixinBase):
    app_label: Optional[str] = None
    model: Optional[Model] = None

    def __init__(self, *args, **kwargs):
        if self.model is None:
            raise AttributeError(
                f"You need to define the `model` member in {self}"
            )
        if not self.app_label:
            self.app_label = self.model._meta.app_label
        super().__init__()

    def test_func(self):
        user_permissions = self._user_permissions()
        return self.request.user.is_active and all(
            permission in user_permissions
            for permission in self._model_permissions(
                content_type__model=self.model._meta.model_name
            )
        )


class PermissionsModelsMixin(UserAppPermissionsMixinBase):
    models: List[Model] = []

    def __init__(self, *args, **kwargs):
        if not self.models:
            raise AttributeError(
                f"You need to define the `models` member in {self}"
            )
        app_labels = {model._meta.app_label for model in self.models}
        if len(app_labels) != 1:
            raise AttributeError(
                f"The `models` defined different apps in {self}"
            )
        self.app_label = app_labels.pop()
        super().__init__()

    def test_func(self):
        models = tuple(model._meta.model_name for model in self.models)
        user_permissions = self._user_permissions()
        return self.request.user.is_active and all(
            permission in user_permissions
            for permission in self._model_permissions(
                content_type__model__in=models
            )
        )
