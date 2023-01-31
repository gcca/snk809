# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import Tuple

from django import forms
from django.core.exceptions import ValidationError

from . import widgets


class DiscField(forms.Field):
    widget = widgets.DiscInput

    def __init__(self, traits: Tuple[str], **kwargs):
        self.traits = traits
        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs["traits"] = self.traits
        return attrs

    def validate(self, value):
        super().validate(value)

        if not value.minus:
            raise ValidationError(
                "Selecciona una opción para la columna menos.", code="no-minus"
            )

        if not value.plus:
            raise ValidationError(
                "Selecciona una opción para la columna más.", code="no-plus"
            )

        if value.minus == value.plus:
            raise ValidationError(
                "No puede seleccionar ambas opciones para una sola"
                " característica.",
                code="no-equal",
            )
