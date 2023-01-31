# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import Any, Dict, List

from django.core.exceptions import ValidationError
from django.forms import ChoiceField, Form, RadioSelect, formset_factory
from django.forms.formsets import BaseFormSet

from .models import DiscSelectQuestion, Quiz

DISC_CHOICES = (("o", "NA"), ("+", "plus"), ("-", "minus"))


class DiscForm(Form):  # Tal vez BaseForm es mejor

    DISC_OPTIONS = None
    QUESTION_IDS = None

    def __init__(self, *args, discIndex=None, **kwargs):
        if DiscForm.DISC_OPTIONS is None:  # cache and optimize query
            questions = DiscSelectQuestion.objects.filter(quiz=Quiz.ID.DISC)
            DiscForm.DISC_OPTIONS = [
                list(question.options.values_list("text", flat=True))
                for question in questions
            ]
            DiscForm.QUESTION_IDS = [question.id for question in questions]
        labels = DiscForm.DISC_OPTIONS[discIndex]
        self.base_fields = {
            label: ChoiceField(choices=DISC_CHOICES, widget=RadioSelect)
            for label in labels
        }
        self.question_id = DiscForm.QUESTION_IDS[discIndex]
        super().__init__(*args, **kwargs)
        if not self.is_bound:  # hack to init data for clean valid
            for _, boundField in self._bound_items():
                boundField.initial = "o"

    def clean(self):
        cleanedData = super().clean()
        fieldNames = self.fields.keys()

        self.ValidateFieldNamesInCleanedData(fieldNames, cleanedData)
        self.ValidateAnswer(fieldNames, cleanedData)

        return cleanedData

    def ValidateFieldNamesInCleanedData(
        self, fieldNames: List[str], cleanedData: Dict[str, str]
    ):
        if not all(name in cleanedData for name in fieldNames):
            raise ValidationError(
                "El formulario no tiene todos los campos.",
                code="incomplete-data",
            )

    def ValidateAnswer(
        self, fieldNames: List[str], cleanedData: Dict[str, str]
    ):
        answerValues = []

        for name in fieldNames:
            value = cleanedData[name]
            if value in ("+", "-"):
                answerValues.append(value)

        if "+" not in answerValues:
            raise ValidationError(
                "Se debe registrar una opción como plus en cada pregunta",
                code="missing-plus",
            )
        if "-" not in answerValues:
            raise ValidationError(
                "Se debe registrar una opción como minus en cada pregunta",
                code="missing-minus",
            )

        if len(answerValues) != 2:
            raise ValidationError(
                "Se debe registrar 2 opciones por pregunta",
                code="invalid-options",
            )


class DiscFormSetSupport(BaseFormSet):
    def get_form_kwargs(self, index: int) -> Dict[str, Any]:
        return {"discIndex": index}

    @classmethod
    def get_default_prefix(cls) -> str:
        return "disc"


DiscFormSet = formset_factory(DiscForm, DiscFormSetSupport, extra=24)
