# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django import shortcuts, urls
from django.contrib.auth.mixins import UserPassesTestMixin

from neodash import mixins as neodash_mixins

from . import models


class OnboardPermissionsMixin(neodash_mixins.PermissionsAppMixin):
    """Temporalmente usamos esto para verificar que el usuario tiene los
    permisos sobre todo el módulo. El objetivo es no usar este mixin y tener
    los permisos asociados a cada view o acción."""

    app_label = "onboard"


class OnboardSlugCheckMixin(UserPassesTestMixin):
    """Evita que alguien use un slug no existente para acceder al dashboard
    del candidadto.
    Se puede usar para tener links de uso temporal o de un solo uso.
    Bastaría cambiar el slug luego de que el candidato "use" el link."""

    def test_func(self):
        slug = self.kwargs["slug"]

        if len(slug) > models.Onboard.slug.field.max_length:
            return False

        return models.Onboard.objects.filter(slug=slug).exists()


class AlreadySavedAssessmentMixin:
    """Usado en los views de los cuestionarios para evitar actualizarlos.
    Es necesario asignar el atribudo `model` de la clase view.
    """

    def get_success_url(self):
        return urls.reverse(
            "onboard:onboard:saved",
            kwargs={"slug": self.kwargs["slug"]},
        )

    def post(self, request, *args, **kwargs):
        slug = self.kwargs["slug"]

        if self.model.objects.filter(onboard__slug=slug).exists():
            return shortcuts.redirect(
                urls.reverse(
                    "onboard:onboard:already-saved",
                    kwargs={"slug": slug},
                )
            )

        return super().post(request, *args, **kwargs)
