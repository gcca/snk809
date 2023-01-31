# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from __future__ import annotations

import os
import re
import shutil
from enum import Enum
from typing import List, NamedTuple, Set
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

# -----------------------------------------------------------------------------
# Applicant


class Applicant(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 1
        FEMALE = 2

    name = models.CharField(max_length=1024)
    email = models.EmailField(max_length=128, unique=True)
    gender = models.IntegerField(choices=Gender.choices)

    def __str__(self):
        return self.name

    def IsMale(self):
        return self.gender == self.Gender.MALE

    def IsFemale(self):
        return self.gender == self.Gender.FEMALE


def ResumeDirectoryPath(instance, filename):
    return f"resumes/{instance.applicant.id}/{filename}"


def validate_googleform_url(value):
    if urlparse(value).query:
        raise ValidationError(
            _(
                "%(value)s has a not allowed query string. Please write this"
                " with this structure:"
                " https://docs.google.com/forms/d/e/string_code/viewform"
            ),
            params={"value": value},
        )


class GoogleForm(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=2048)
    shared_url = models.URLField(
        max_length=1024, validators=[validate_googleform_url]
    )
    view_link = models.URLField(max_length=1024, null=True, blank=True)

    @property
    def embed_url(self):
        parsedUrl = urlparse(self.shared_url)
        return parsedUrl._replace(query="embedded=true").geturl()


class Onboard(models.Model):
    applicant = models.OneToOneField(
        Applicant, on_delete=models.CASCADE, primary_key=True
    )
    slug = models.SlugField(max_length=128, unique=True)
    resume = models.FileField(
        upload_to=ResumeDirectoryPath, null=True, blank=True
    )
    show_disc = models.BooleanField(default=True)
    show_tmms = models.BooleanField(default=True)
    show_complex_instructions = models.BooleanField(default=True)
    show_career_anchors = models.BooleanField(default=True)
    show_resume = models.BooleanField(default=True)
    process_name = models.CharField(max_length=1024, blank=True)
    process_link = models.URLField(max_length=1024, blank=True)

    google_forms = models.ManyToManyField(GoogleForm)

    def _Toggle(self, value: bool):
        return not value

    def ToggleDisc(self):
        self.show_disc = self._Toggle(self.show_disc)

    def ToggleTmms(self):
        self.show_tmms = self._Toggle(self.show_tmms)

    def ToggleComplexInstructions(self):
        self.show_complex_instructions = self._Toggle(
            self.show_complex_instructions
        )

    def ToggleCareerAnchors(self):
        self.show_career_anchors = self._Toggle(self.show_career_anchors)


@receiver(pre_save, sender=Onboard)
def UpdateFileEvent(sender, **kwargs):
    onboard = kwargs["instance"]
    dirname = os.path.dirname(
        onboard.resume.storage.path(
            ResumeDirectoryPath(onboard, onboard.resume.name)
        )
    )
    if os.path.exists(dirname):
        shutil.rmtree(dirname)


class TmmsInput(models.Model):
    CHOICES = ((1, ""), (2, ""), (3, ""), (4, ""), (5, ""))
    onboard = models.OneToOneField(
        Onboard, on_delete=models.CASCADE, primary_key=True
    )
    q1 = models.IntegerField(choices=CHOICES)
    q2 = models.IntegerField(choices=CHOICES)
    q3 = models.IntegerField(choices=CHOICES)
    q4 = models.IntegerField(choices=CHOICES)
    q5 = models.IntegerField(choices=CHOICES)
    q6 = models.IntegerField(choices=CHOICES)
    q7 = models.IntegerField(choices=CHOICES)
    q8 = models.IntegerField(choices=CHOICES)
    q9 = models.IntegerField(choices=CHOICES)
    q10 = models.IntegerField(choices=CHOICES)
    q11 = models.IntegerField(choices=CHOICES)
    q12 = models.IntegerField(choices=CHOICES)
    q13 = models.IntegerField(choices=CHOICES)
    q14 = models.IntegerField(choices=CHOICES)
    q15 = models.IntegerField(choices=CHOICES)
    q16 = models.IntegerField(choices=CHOICES)
    q17 = models.IntegerField(choices=CHOICES)
    q18 = models.IntegerField(choices=CHOICES)
    q19 = models.IntegerField(choices=CHOICES)
    q20 = models.IntegerField(choices=CHOICES)
    q21 = models.IntegerField(choices=CHOICES)
    q22 = models.IntegerField(choices=CHOICES)
    q23 = models.IntegerField(choices=CHOICES)
    q24 = models.IntegerField(choices=CHOICES)

    @property
    def scores(self):
        attention_score = (
            self.q1
            + self.q2
            + self.q3
            + self.q4
            + self.q5
            + self.q6
            + self.q7
            + self.q8
        )
        clarity_score = (
            self.q9
            + self.q10
            + self.q11
            + self.q12
            + self.q13
            + self.q14
            + self.q15
            + self.q16
        )
        repair_score = (
            self.q17
            + self.q18
            + self.q19
            + self.q20
            + self.q21
            + self.q22
            + self.q23
            + self.q24
        )
        return (attention_score, clarity_score, repair_score)

    def _GetLabelByBound(self, value, bounds, labels):
        lower, upper = bounds
        if value < lower:
            return labels.below
        if value > upper:
            return labels.above
        return labels.average

    def _GetLabels(self):
        MALE_BOUNDS = {
            "attention": (21, 33),
            "clarity": (25, 36),
            "repair": (23, 36),
        }
        FEMALE_BOUNDS = {
            "attention": (24, 36),
            "clarity": (23, 35),
            "repair": (23, 35),
        }
        LabelTuple = NamedTuple(
            "LabelCollection",
            [
                ("below", str),
                ("average", str),
                ("above", str),
            ],
        )
        LABELS = {
            "attention": LabelTuple(
                "Presta poca atención",
                "Adecuada atención",
                "Presta demasiada atención",
            ),
            "clarity": LabelTuple(
                "Deficiente comprensión",
                "Adecuada compresión",
                "Excelente compresión",
            ),
            "repair": LabelTuple(
                "Deficiente regulación",
                "Adecuada regulación",
                "Excelente regulación",
            ),
        }

        applicant = self.onboard.applicant
        if applicant.IsMale():
            bounds = MALE_BOUNDS
        elif applicant.IsFemale():
            bounds = FEMALE_BOUNDS
        else:
            raise RuntimeError("Illegal state")

        attention_score, clarity_score, repair_score = self.scores
        attention_label = self._GetLabelByBound(
            attention_score, bounds["attention"], LABELS["attention"]
        )
        clarity_label = self._GetLabelByBound(
            clarity_score, bounds["clarity"], LABELS["clarity"]
        )
        repair_label = self._GetLabelByBound(
            repair_score, bounds["repair"], LABELS["repair"]
        )
        return (attention_label, clarity_label, repair_label)

    class TmmsScore(NamedTuple):
        score: int
        label: str

    class TmmsResult(NamedTuple):
        attention: TmmsInput.TmmsScore
        clarity: TmmsInput.TmmsScore
        repair: TmmsInput.TmmsScore

    @property
    def labeled_scores(self):
        scores = self.scores
        labels = self._GetLabels()

        attention = self.TmmsScore(scores[0], labels[0])
        clarity = self.TmmsScore(scores[1], labels[1])
        repair = self.TmmsScore(scores[2], labels[2])

        return self.TmmsResult(attention, clarity, repair)


class ComplexInstructionsInput(models.Model):
    onboard = models.OneToOneField(
        Onboard, on_delete=models.CASCADE, primary_key=True
    )

    q1_a = models.BooleanField(default=False)
    q1_b = models.BooleanField(default=False)
    q1_c = models.BooleanField(default=False)

    q2_a = models.BooleanField(default=False)
    q2_b = models.BooleanField(default=False)
    q2_c = models.BooleanField(default=False)

    q3_a = models.BooleanField(default=False)
    q3_b = models.BooleanField(default=False)
    q3_c = models.BooleanField(default=False)

    q4_a = models.BooleanField(default=False)
    q4_b = models.BooleanField(default=False)
    q4_c = models.BooleanField(default=False)

    q5_a = models.BooleanField(default=False)
    q5_b = models.BooleanField(default=False)
    q5_c = models.BooleanField(default=False)

    q6_a = models.BooleanField(default=False)
    q6_b = models.BooleanField(default=False)
    q6_c = models.BooleanField(default=False)

    q7_a = models.BooleanField(default=False)
    q7_b = models.BooleanField(default=False)
    q7_c = models.BooleanField(default=False)

    q8_a = models.BooleanField(default=False)
    q8_b = models.BooleanField(default=False)
    q8_c = models.BooleanField(default=False)

    q9_a = models.BooleanField(default=False)
    q9_b = models.BooleanField(default=False)
    q9_c = models.BooleanField(default=False)

    q10_a = models.BooleanField(default=False)
    q10_b = models.BooleanField(default=False)
    q10_c = models.BooleanField(default=False)

    q11_a = models.BooleanField(default=False)
    q11_b = models.BooleanField(default=False)
    q11_c = models.BooleanField(default=False)

    q12_a = models.BooleanField(default=False)
    q12_b = models.BooleanField(default=False)
    q12_c = models.BooleanField(default=False)

    q13_a = models.BooleanField(default=False)
    q13_b = models.BooleanField(default=False)
    q13_c = models.BooleanField(default=False)

    q14_a = models.BooleanField(default=False)
    q14_b = models.BooleanField(default=False)
    q14_c = models.BooleanField(default=False)

    q15_a = models.BooleanField(default=False)
    q15_b = models.BooleanField(default=False)
    q15_c = models.BooleanField(default=False)

    q16_a = models.BooleanField(default=False)
    q16_b = models.BooleanField(default=False)
    q16_c = models.BooleanField(default=False)

    q17_a = models.BooleanField(default=False)
    q17_b = models.BooleanField(default=False)
    q17_c = models.BooleanField(default=False)

    q18_a = models.BooleanField(default=False)
    q18_b = models.BooleanField(default=False)
    q18_c = models.BooleanField(default=False)

    q19_a = models.BooleanField(default=False)
    q19_b = models.BooleanField(default=False)
    q19_c = models.BooleanField(default=False)

    q20_a = models.BooleanField(default=False)
    q20_b = models.BooleanField(default=False)
    q20_c = models.BooleanField(default=False)

    q21_a = models.BooleanField(default=False)
    q21_b = models.BooleanField(default=False)
    q21_c = models.BooleanField(default=False)

    q22_a = models.BooleanField(default=False)
    q22_b = models.BooleanField(default=False)
    q22_c = models.BooleanField(default=False)

    q23_a = models.BooleanField(default=False)
    q23_b = models.BooleanField(default=False)
    q23_c = models.BooleanField(default=False)

    q24_a = models.BooleanField(default=False)
    q24_b = models.BooleanField(default=False)
    q24_c = models.BooleanField(default=False)

    q25_a = models.BooleanField(default=False)
    q25_b = models.BooleanField(default=False)
    q25_c = models.BooleanField(default=False)

    @property
    def q1(self):
        return (self.q1_a, self.q1_b, self.q1_c)

    @q1.setter
    def q1(self, val):
        self.q1_a, self.q1_b, self.q1_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q2(self):
        return (self.q2_a, self.q2_b, self.q2_c)

    @q2.setter
    def q2(self, val):
        self.q2_a, self.q2_b, self.q2_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q3(self):
        return (self.q3_a, self.q3_b, self.q3_c)

    @q3.setter
    def q3(self, val):
        self.q3_a, self.q3_b, self.q3_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q4(self):
        return (self.q4_a, self.q4_b, self.q4_c)

    @q4.setter
    def q4(self, val):
        self.q4_a, self.q4_b, self.q4_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q5(self):
        return (self.q5_a, self.q5_b, self.q5_c)

    @q5.setter
    def q5(self, val):
        self.q5_a, self.q5_b, self.q5_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q6(self):
        return (self.q6_a, self.q6_b, self.q6_c)

    @q6.setter
    def q6(self, val):
        self.q6_a, self.q6_b, self.q6_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q7(self):
        return (self.q7_a, self.q7_b, self.q7_c)

    @q7.setter
    def q7(self, val):
        self.q7_a, self.q7_b, self.q7_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q8(self):
        return (self.q8_a, self.q8_b, self.q8_c)

    @q8.setter
    def q8(self, val):
        self.q8_a, self.q8_b, self.q8_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q9(self):
        return (self.q9_a, self.q9_b, self.q9_c)

    @q9.setter
    def q9(self, val):
        self.q9_a, self.q9_b, self.q9_c = ("a" in val, "b" in val, "c" in val)

    @property
    def q10(self):
        return (self.q10_a, self.q10_b, self.q10_c)

    @q10.setter
    def q10(self, val):
        self.q10_a, self.q10_b, self.q10_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q11(self):
        return (self.q11_a, self.q11_b, self.q11_c)

    @q11.setter
    def q11(self, val):
        self.q11_a, self.q11_b, self.q11_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q12(self):
        return (self.q12_a, self.q12_b, self.q12_c)

    @q12.setter
    def q12(self, val):
        self.q12_a, self.q12_b, self.q12_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q13(self):
        return (self.q13_a, self.q13_b, self.q13_c)

    @q13.setter
    def q13(self, val):
        self.q13_a, self.q13_b, self.q13_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q14(self):
        return (self.q14_a, self.q14_b, self.q14_c)

    @q14.setter
    def q14(self, val):
        self.q14_a, self.q14_b, self.q14_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q15(self):
        return (self.q15_a, self.q15_b, self.q15_c)

    @q15.setter
    def q15(self, val):
        self.q15_a, self.q15_b, self.q15_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q16(self):
        return (self.q16_a, self.q16_b, self.q16_c)

    @q16.setter
    def q16(self, val):
        self.q16_a, self.q16_b, self.q16_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q17(self):
        return (self.q17_a, self.q17_b, self.q17_c)

    @q17.setter
    def q17(self, val):
        self.q17_a, self.q17_b, self.q17_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q18(self):
        return (self.q18_a, self.q18_b, self.q18_c)

    @q18.setter
    def q18(self, val):
        self.q18_a, self.q18_b, self.q18_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q19(self):
        return (self.q19_a, self.q19_b, self.q19_c)

    @q19.setter
    def q19(self, val):
        self.q19_a, self.q19_b, self.q19_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q20(self):
        return (self.q20_a, self.q20_b, self.q20_c)

    @q20.setter
    def q20(self, val):
        self.q20_a, self.q20_b, self.q20_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q21(self):
        return (self.q21_a, self.q21_b, self.q21_c)

    @q21.setter
    def q21(self, val):
        self.q21_a, self.q21_b, self.q21_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q22(self):
        return (self.q22_a, self.q22_b, self.q22_c)

    @q22.setter
    def q22(self, val):
        self.q22_a, self.q22_b, self.q22_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q23(self):
        return (self.q23_a, self.q23_b, self.q23_c)

    @q23.setter
    def q23(self, val):
        self.q23_a, self.q23_b, self.q23_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q24(self):
        return (self.q24_a, self.q24_b, self.q24_c)

    @q24.setter
    def q24(self, val):
        self.q24_a, self.q24_b, self.q24_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    @property
    def q25(self):
        return (self.q25_a, self.q25_b, self.q25_c)

    @q25.setter
    def q25(self, val):
        self.q25_a, self.q25_b, self.q25_c = (
            "a" in val,
            "b" in val,
            "c" in val,
        )

    ANSWERS = (
        (True, False, True),
        (False, True, False),
        (True, False, False),
        (False, False, False),
        (False, False, True),
        (True, False, False),
        (False, False, True),
        (False, False, False),
        (False, False, False),
        (True, False, False),
        (False, False, True),
        (False, False, False),
        (False, True, False),
        (False, False, False),
        (False, False, True),
        (False, False, False),
        (False, False, False),
        (False, False, False),
        (True, False, True),
        (True, True, False),
        (False, False, True),
        (False, False, True),
        (True, False, False),
        (False, False, False),
        (True, True, False),
    )

    def _CalculateDifference(self, a, b):
        total_diff = 0
        if len(a) != len(b):
            raise ValueError("Tuples must be of the same size")
        for i in range(len(a)):
            if a[i] != b[i]:
                total_diff = total_diff + 1
        return total_diff

    @property
    def Score(self):
        scores = [
            self._CalculateDifference(self.q1, self.ANSWERS[0]),
            self._CalculateDifference(self.q2, self.ANSWERS[1]),
            self._CalculateDifference(self.q3, self.ANSWERS[2]),
            self._CalculateDifference(self.q4, self.ANSWERS[3]),
            self._CalculateDifference(self.q5, self.ANSWERS[4]),
            self._CalculateDifference(self.q6, self.ANSWERS[5]),
            self._CalculateDifference(self.q7, self.ANSWERS[6]),
            self._CalculateDifference(self.q8, self.ANSWERS[7]),
            self._CalculateDifference(self.q9, self.ANSWERS[8]),
            self._CalculateDifference(self.q10, self.ANSWERS[9]),
            self._CalculateDifference(self.q11, self.ANSWERS[10]),
            self._CalculateDifference(self.q12, self.ANSWERS[11]),
            self._CalculateDifference(self.q13, self.ANSWERS[12]),
            self._CalculateDifference(self.q14, self.ANSWERS[13]),
            self._CalculateDifference(self.q15, self.ANSWERS[14]),
            self._CalculateDifference(self.q16, self.ANSWERS[15]),
            self._CalculateDifference(self.q17, self.ANSWERS[16]),
            self._CalculateDifference(self.q18, self.ANSWERS[17]),
            self._CalculateDifference(self.q19, self.ANSWERS[18]),
            self._CalculateDifference(self.q20, self.ANSWERS[19]),
            self._CalculateDifference(self.q21, self.ANSWERS[20]),
            self._CalculateDifference(self.q22, self.ANSWERS[21]),
            self._CalculateDifference(self.q23, self.ANSWERS[22]),
            self._CalculateDifference(self.q24, self.ANSWERS[23]),
        ]
        return sum(scores)

    @property
    def LabeledScore(self):
        score = self.Score
        if score < 6:
            return (score, "Adecuado")
        if score < 12:
            return (score, "Regular")
        return (score, "Inferior (Contraindicado)")


class DiscInput(models.Model):
    class Q1Input(models.IntegerChoices):
        EXPRESIVO = 1
        SUMISO = 2
        ENÉRGICO = 3
        CONTROLADO = 4

    class Q2Input(models.IntegerChoices):
        FUERTE_DE_CARÁCTER = 1
        CUIDADOSO = 2
        EMOCIONAL = 3
        SATISFECHO = 4

    class Q3Input(models.IntegerChoices):
        CORRECTO = 1
        PIONERO = 2
        TRANQUILO = 3
        INFLUYENTE = 4

    class Q4Input(models.IntegerChoices):
        PRECISO = 1
        DOMINANTE = 2
        DISPUESTO = 3
        ATRACTIVO = 4

    class Q5Input(models.IntegerChoices):
        ECUÁNIME = 1
        ESTIMULANTE = 2
        METICULOSO = 3
        DECIDIDO = 4

    class Q6Input(models.IntegerChoices):
        TÍMIDO = 1
        EXIGENTE = 2
        PACIENTE = 3
        CAUTIVADOR = 4

    class Q7Input(models.IntegerChoices):
        CONCIENZUDO = 1
        BUENA_COMPAÑIA = 2
        BONDADOSO = 3
        DEPENDE_DE_SI = 4

    class Q8Input(models.IntegerChoices):
        AGRADABLE = 1
        CON_DOMINIO_PROPIO = 2
        JUGUETÓN = 3
        PERSISTENTE = 4

    class Q9Input(models.IntegerChoices):
        ANIMOSO = 1
        CONVERSADOR = 2
        BONACHON = 3
        CONSERVADOR = 4

    class Q10Input(models.IntegerChoices):
        CONTENTO = 1
        IMPACIENTE = 2
        CONVICENTE = 3
        RESIGNADO = 4

    class Q11Input(models.IntegerChoices):
        RESPETUOSO = 1
        SOCIALMENTE_DESENVUELTO = 2
        AGRESIVO = 3
        APACIBLE = 4

    class Q12Input(models.IntegerChoices):
        APLOMO = 1
        CONVENCIONAL = 2
        TOMA_RIESGOS = 3
        SERVICIAL = 4

    class Q13Input(models.IntegerChoices):
        SEGURO_DE_SÍ_MISMO = 1
        COOPERATIVO = 2
        DISPUTADOR = 3
        RELAJADO_SIN_TENSIONES = 4

    class Q14Input(models.IntegerChoices):
        INQUIETO = 1
        DISCIPLINADO = 2
        INSPIRADOR = 3
        CONSIDERADO = 4

    class Q15Input(models.IntegerChoices):
        DIPLOMÁTICO = 1
        VALIENTE = 2
        COMPASIVO = 3
        OPTIMISTA = 4

    class Q16Input(models.IntegerChoices):
        ENCANTADOR = 1
        POSITIVO = 2
        INDULGENTE = 3
        RIGUROSO = 4

    class Q17Input(models.IntegerChoices):
        AVENTURERO = 1
        ENTUSIASTA = 2
        SIGUE_LAS_REGLAS = 3
        LEAL = 4

    class Q18Input(models.IntegerChoices):
        HUMILDE = 1
        OYENTE_ATENTO = 2
        ENTRETENIDO = 3
        CON_FUERZA_DE_VOLUNTAD = 4

    class Q19Input(models.IntegerChoices):
        DIVERTIDO = 1
        OBEDIENTE = 2
        DISCRETO = 3
        COMPETITIVO = 4

    class Q20Input(models.IntegerChoices):
        CAUTELOSO = 1
        AMISTOSO = 2
        VIGOROSO = 3
        PERSUASIVO = 4

    class Q21Input(models.IntegerChoices):
        RESERVADO = 1
        FRANCO = 2
        ESTRICTO = 3
        ELOCUENTE = 4

    class Q22Input(models.IntegerChoices):
        CORTÉS = 1
        ANIMADO = 2
        DECISIVO = 3
        PRECISO = 4

    class Q23Input(models.IntegerChoices):
        ASERTIVO = 1
        SOCIABLE = 2
        ESTABLE = 3
        METÓDICO = 4

    class Q24Input(models.IntegerChoices):
        EXTROVERTIDO = 1
        INTREPIDO = 2
        MODERADO = 3
        PERFECCIONISTA = 4

    onboard = models.OneToOneField(
        Onboard, on_delete=models.CASCADE, primary_key=True
    )

    q1_minus = models.IntegerField(choices=Q1Input.choices)
    q1_plus = models.IntegerField(choices=Q1Input.choices)

    q2_minus = models.IntegerField(choices=Q2Input.choices)
    q2_plus = models.IntegerField(choices=Q2Input.choices)

    q3_minus = models.IntegerField(choices=Q3Input.choices)
    q3_plus = models.IntegerField(choices=Q3Input.choices)

    q4_minus = models.IntegerField(choices=Q4Input.choices)
    q4_plus = models.IntegerField(choices=Q4Input.choices)

    q5_minus = models.IntegerField(choices=Q5Input.choices)
    q5_plus = models.IntegerField(choices=Q5Input.choices)

    q6_minus = models.IntegerField(choices=Q6Input.choices)
    q6_plus = models.IntegerField(choices=Q6Input.choices)

    q7_minus = models.IntegerField(choices=Q7Input.choices)
    q7_plus = models.IntegerField(choices=Q7Input.choices)

    q8_minus = models.IntegerField(choices=Q8Input.choices)
    q8_plus = models.IntegerField(choices=Q8Input.choices)

    q9_minus = models.IntegerField(choices=Q9Input.choices)
    q9_plus = models.IntegerField(choices=Q9Input.choices)

    q10_minus = models.IntegerField(choices=Q10Input.choices)
    q10_plus = models.IntegerField(choices=Q10Input.choices)

    q11_minus = models.IntegerField(choices=Q11Input.choices)
    q11_plus = models.IntegerField(choices=Q11Input.choices)

    q12_minus = models.IntegerField(choices=Q12Input.choices)
    q12_plus = models.IntegerField(choices=Q12Input.choices)

    q13_minus = models.IntegerField(choices=Q13Input.choices)
    q13_plus = models.IntegerField(choices=Q13Input.choices)

    q14_minus = models.IntegerField(choices=Q14Input.choices)
    q14_plus = models.IntegerField(choices=Q14Input.choices)

    q15_minus = models.IntegerField(choices=Q15Input.choices)
    q15_plus = models.IntegerField(choices=Q15Input.choices)

    q16_minus = models.IntegerField(choices=Q16Input.choices)
    q16_plus = models.IntegerField(choices=Q16Input.choices)

    q17_minus = models.IntegerField(choices=Q17Input.choices)
    q17_plus = models.IntegerField(choices=Q17Input.choices)

    q18_minus = models.IntegerField(choices=Q18Input.choices)
    q18_plus = models.IntegerField(choices=Q18Input.choices)

    q19_minus = models.IntegerField(choices=Q19Input.choices)
    q19_plus = models.IntegerField(choices=Q19Input.choices)

    q20_minus = models.IntegerField(choices=Q20Input.choices)
    q20_plus = models.IntegerField(choices=Q20Input.choices)

    q21_minus = models.IntegerField(choices=Q21Input.choices)
    q21_plus = models.IntegerField(choices=Q21Input.choices)

    q22_minus = models.IntegerField(choices=Q22Input.choices)
    q22_plus = models.IntegerField(choices=Q22Input.choices)

    q23_minus = models.IntegerField(choices=Q23Input.choices)
    q23_plus = models.IntegerField(choices=Q23Input.choices)

    q24_minus = models.IntegerField(choices=Q24Input.choices)
    q24_plus = models.IntegerField(choices=Q24Input.choices)

    class DiscDomain(Enum):
        DOMINANCE = 1
        INFLUENCE = 2
        STEADINESS = 3
        CONSCIENTIOUSNESS = 4

    MAPPINGS = {
        Q1Input: {
            Q1Input.EXPRESIVO: DiscDomain.INFLUENCE,
            Q1Input.SUMISO: DiscDomain.CONSCIENTIOUSNESS,
            Q1Input.ENÉRGICO: DiscDomain.DOMINANCE,
            Q1Input.CONTROLADO: DiscDomain.STEADINESS,
        },
        Q2Input: {
            Q2Input.FUERTE_DE_CARÁCTER: DiscDomain.DOMINANCE,
            Q2Input.CUIDADOSO: DiscDomain.CONSCIENTIOUSNESS,
            Q2Input.EMOCIONAL: DiscDomain.INFLUENCE,
            Q2Input.SATISFECHO: DiscDomain.STEADINESS,
        },
        Q3Input: {
            Q3Input.CORRECTO: DiscDomain.CONSCIENTIOUSNESS,
            Q3Input.PIONERO: DiscDomain.DOMINANCE,
            Q3Input.TRANQUILO: DiscDomain.STEADINESS,
            Q3Input.INFLUYENTE: DiscDomain.INFLUENCE,
        },
        Q4Input: {
            Q4Input.PRECISO: DiscDomain.CONSCIENTIOUSNESS,
            Q4Input.DOMINANTE: DiscDomain.DOMINANCE,
            Q4Input.DISPUESTO: DiscDomain.STEADINESS,
            Q4Input.ATRACTIVO: DiscDomain.INFLUENCE,
        },
        Q5Input: {
            Q5Input.ECUÁNIME: DiscDomain.STEADINESS,
            Q5Input.ESTIMULANTE: DiscDomain.INFLUENCE,
            Q5Input.METICULOSO: DiscDomain.CONSCIENTIOUSNESS,
            Q5Input.DECIDIDO: DiscDomain.DOMINANCE,
        },
        Q6Input: {
            Q6Input.TÍMIDO: DiscDomain.CONSCIENTIOUSNESS,
            Q6Input.EXIGENTE: DiscDomain.DOMINANCE,
            Q6Input.PACIENTE: DiscDomain.STEADINESS,
            Q6Input.CAUTIVADOR: DiscDomain.INFLUENCE,
        },
        Q7Input: {
            Q7Input.CONCIENZUDO: DiscDomain.CONSCIENTIOUSNESS,
            Q7Input.BUENA_COMPAÑIA: DiscDomain.INFLUENCE,
            Q7Input.BONDADOSO: DiscDomain.STEADINESS,
            Q7Input.DEPENDE_DE_SI: DiscDomain.DOMINANCE,
        },
        Q8Input: {
            Q8Input.AGRADABLE: DiscDomain.CONSCIENTIOUSNESS,
            Q8Input.CON_DOMINIO_PROPIO: DiscDomain.STEADINESS,
            Q8Input.JUGUETÓN: DiscDomain.INFLUENCE,
            Q8Input.PERSISTENTE: DiscDomain.DOMINANCE,
        },
        Q9Input: {
            Q9Input.ANIMOSO: DiscDomain.DOMINANCE,
            Q9Input.CONVERSADOR: DiscDomain.INFLUENCE,
            Q9Input.BONACHON: DiscDomain.STEADINESS,
            Q9Input.CONSERVADOR: DiscDomain.CONSCIENTIOUSNESS,
        },
        Q10Input: {
            Q10Input.CONTENTO: DiscDomain.STEADINESS,
            Q10Input.IMPACIENTE: DiscDomain.DOMINANCE,
            Q10Input.CONVICENTE: DiscDomain.INFLUENCE,
            Q10Input.RESIGNADO: DiscDomain.CONSCIENTIOUSNESS,
        },
        Q11Input: {
            Q11Input.RESPETUOSO: DiscDomain.CONSCIENTIOUSNESS,
            Q11Input.SOCIALMENTE_DESENVUELTO: DiscDomain.INFLUENCE,
            Q11Input.AGRESIVO: DiscDomain.DOMINANCE,
            Q11Input.APACIBLE: DiscDomain.STEADINESS,
        },
        Q12Input: {
            Q12Input.APLOMO: DiscDomain.INFLUENCE,
            Q12Input.CONVENCIONAL: DiscDomain.CONSCIENTIOUSNESS,
            Q12Input.TOMA_RIESGOS: DiscDomain.DOMINANCE,
            Q12Input.SERVICIAL: DiscDomain.STEADINESS,
        },
        Q13Input: {
            Q13Input.SEGURO_DE_SÍ_MISMO: DiscDomain.INFLUENCE,
            Q13Input.COOPERATIVO: DiscDomain.CONSCIENTIOUSNESS,
            Q13Input.DISPUTADOR: DiscDomain.DOMINANCE,
            Q13Input.RELAJADO_SIN_TENSIONES: DiscDomain.STEADINESS,
        },
        Q14Input: {
            Q14Input.INQUIETO: DiscDomain.DOMINANCE,
            Q14Input.DISCIPLINADO: DiscDomain.CONSCIENTIOUSNESS,
            Q14Input.INSPIRADOR: DiscDomain.INFLUENCE,
            Q14Input.CONSIDERADO: DiscDomain.STEADINESS,
        },
        Q15Input: {
            Q15Input.DIPLOMÁTICO: DiscDomain.CONSCIENTIOUSNESS,
            Q15Input.VALIENTE: DiscDomain.DOMINANCE,
            Q15Input.COMPASIVO: DiscDomain.STEADINESS,
            Q15Input.OPTIMISTA: DiscDomain.INFLUENCE,
        },
        Q16Input: {
            Q16Input.ENCANTADOR: DiscDomain.INFLUENCE,
            Q16Input.POSITIVO: DiscDomain.DOMINANCE,
            Q16Input.INDULGENTE: DiscDomain.STEADINESS,
            Q16Input.RIGUROSO: DiscDomain.CONSCIENTIOUSNESS,
        },
        Q17Input: {
            Q17Input.AVENTURERO: DiscDomain.DOMINANCE,
            Q17Input.ENTUSIASTA: DiscDomain.INFLUENCE,
            Q17Input.SIGUE_LAS_REGLAS: DiscDomain.CONSCIENTIOUSNESS,
            Q17Input.LEAL: DiscDomain.STEADINESS,
        },
        Q18Input: {
            Q18Input.HUMILDE: DiscDomain.CONSCIENTIOUSNESS,
            Q18Input.OYENTE_ATENTO: DiscDomain.STEADINESS,
            Q18Input.ENTRETENIDO: DiscDomain.INFLUENCE,
            Q18Input.CON_FUERZA_DE_VOLUNTAD: DiscDomain.DOMINANCE,
        },
        Q19Input: {
            Q19Input.DIVERTIDO: DiscDomain.INFLUENCE,
            Q19Input.OBEDIENTE: DiscDomain.STEADINESS,
            Q19Input.DISCRETO: DiscDomain.CONSCIENTIOUSNESS,
            Q19Input.COMPETITIVO: DiscDomain.DOMINANCE,
        },
        Q20Input: {
            Q20Input.CAUTELOSO: DiscDomain.CONSCIENTIOUSNESS,
            Q20Input.AMISTOSO: DiscDomain.STEADINESS,
            Q20Input.VIGOROSO: DiscDomain.DOMINANCE,
            Q20Input.PERSUASIVO: DiscDomain.INFLUENCE,
        },
        Q21Input: {
            Q21Input.RESERVADO: DiscDomain.STEADINESS,
            Q21Input.FRANCO: DiscDomain.DOMINANCE,
            Q21Input.ESTRICTO: DiscDomain.CONSCIENTIOUSNESS,
            Q21Input.ELOCUENTE: DiscDomain.INFLUENCE,
        },
        Q22Input: {
            Q22Input.CORTÉS: DiscDomain.STEADINESS,
            Q22Input.ANIMADO: DiscDomain.INFLUENCE,
            Q22Input.DECISIVO: DiscDomain.DOMINANCE,
            Q22Input.PRECISO: DiscDomain.CONSCIENTIOUSNESS,
        },
        Q23Input: {
            Q23Input.ASERTIVO: DiscDomain.DOMINANCE,
            Q23Input.SOCIABLE: DiscDomain.INFLUENCE,
            Q23Input.ESTABLE: DiscDomain.STEADINESS,
            Q23Input.METÓDICO: DiscDomain.CONSCIENTIOUSNESS,
        },
        Q24Input: {
            Q24Input.EXTROVERTIDO: DiscDomain.INFLUENCE,
            Q24Input.INTREPIDO: DiscDomain.DOMINANCE,
            Q24Input.MODERADO: DiscDomain.STEADINESS,
            Q24Input.PERFECCIONISTA: DiscDomain.CONSCIENTIOUSNESS,
        },
    }

    BAREMOS = {
        DiscDomain.DOMINANCE: {
            "-16": 10,
            "-15": 16,
            "-14": 20,
            "-13": 20,
            "-12": 30,
            "-11": 30,
            "-10": 30,
            "-9": 40,
            "-8": 40,
            "-7": 50,
            "-6": 50,
            "-5": 60,
            "-4": 60,
            "-3": 60,
            "-2": 60,
            "-1": 70,
            "0": 70,
            "1": 80,
            "2": 80,
            "3": 84,
            "4": 90,
            "5": 95,
            "6": 95,
            "7": 95,
            "8": 95,
            "9": 95,
            "10": 95,
            "11": 99,
            "12": 99,
            "13": 99,
            "14": 99,
            "15": 99,
        },
        DiscDomain.INFLUENCE: {
            "-16": 1,
            "-15": 1,
            "-14": 1,
            "-13": 5,
            "-12": 5,
            "-11": 10,
            "-10": 10,
            "-9": 10,
            "-8": 16,
            "-7": 20,
            "-6": 30,
            "-5": 30,
            "-4": 40,
            "-3": 50,
            "-2": 50,
            "-1": 60,
            "0": 60,
            "1": 60,
            "2": 70,
            "3": 70,
            "4": 70,
            "5": 70,
            "6": 80,
            "7": 90,
            "8": 90,
            "9": 95,
            "10": 95,
            "11": 99,
            "12": 99,
            "13": 99,
            "14": 99,
            "15": 99,
            "16": 99,
            "17": 99,
            "18": 99,
        },
        DiscDomain.STEADINESS: {
            "-13": 1,
            "-12": 1,
            "-11": 1,
            "-10": 5,
            "-9": 10,
            "-8": 10,
            "-7": 10,
            "-6": 16,
            "-5": 20,
            "-4": 20,
            "-3": 20,
            "-2": 30,
            "-1": 30,
            "0": 40,
            "1": 40,
            "2": 50,
            "3": 50,
            "4": 50,
            "5": 60,
            "6": 60,
            "7": 60,
            "8": 60,
            "9": 70,
            "10": 70,
            "11": 70,
            "12": 80,
            "13": 90,
            "14": 95,
            "15": 95,
            "16": 99,
            "17": 99,
        },
        DiscDomain.CONSCIENTIOUSNESS: {
            "-15": 1,
            "-14": 1,
            "-13": 5,
            "-12": 5,
            "-11": 10,
            "-10": 10,
            "-9": 10,
            "-8": 16,
            "-7": 20,
            "-6": 20,
            "-5": 30,
            "-4": 30,
            "-3": 40,
            "-2": 30,
            "-1": 40,
            "0": 50,
            "1": 53,
            "2": 60,
            "3": 70,
            "4": 70,
            "5": 80,
            "6": 84,
            "7": 90,
            "8": 90,
            "9": 95,
            "10": 95,
            "11": 99,
            "12": 99,
            "13": 99,
        },
    }

    class DiscTuple(NamedTuple):
        d: int
        i: int
        s: int
        c: int

    class DiscPersonality:
        def __init__(self, name: str, d: int, i: int, s: int, c: int):
            self.name = name
            self.d = d
            self.i = i
            self.s = s
            self.c = c

        def _GetMin(self):
            return min(self.d, self.i, self.s, self.c)

        def NormalizeValue(self, value):
            minimum = self._GetMin()
            return value - minimum

        def NormalizedValues(self):
            norm_d = self.NormalizeValue(self.d)
            norm_i = self.NormalizeValue(self.i)
            norm_s = self.NormalizeValue(self.s)
            norm_c = self.NormalizeValue(self.c)

            return (norm_d, norm_i, norm_s, norm_c)

        def distance(self, other):
            a, b, c, d = self.NormalizedValues()
            w, x, y, z = other.NormalizedValues()

            ratio = max(a, b, c, d) / max(w, x, y, z)

            w, x, y, z = ratio * w, ratio * x, ratio * y, ratio * z

            # mean squared error
            d_diff = (a - w) ** 2
            i_diff = (b - x) ** 2
            s_diff = (c - y) ** 2
            c_diff = (d - z) ** 2
            diff = d_diff + i_diff + s_diff + c_diff
            SAMPLES = 4

            return diff / SAMPLES

    PERSONALITIES = (
        DiscPersonality(name="Director", d=95, i=30, s=30, c=30),
        DiscPersonality(name="Emprendedor", d=95, i=70, s=30, c=10),
        DiscPersonality(name="Organizador", d=90, i=80, s=10, c=30),
        DiscPersonality(name="Pionero", d=90, i=30, s=16, c=70),
        DiscPersonality(name="Cooperativo", d=10, i=70, s=80, c=70),
        DiscPersonality(name="Afiliador", d=40, i=95, s=30, c=30),
        DiscPersonality(name="Negociador", d=20, i=90, s=20, c=90),
        DiscPersonality(name="Motivador", d=84, i=95, s=16, c=20),
        DiscPersonality(name="Persuasivo", d=70, i=95, s=30, c=20),
        DiscPersonality(name="Estratega", d=70, i=5, s=80, c=60),
        DiscPersonality(name="Perseverante", d=30, i=30, s=95, c=30),
        DiscPersonality(name="Investigador", d=84, i=20, s=84, c=20),
        DiscPersonality(name="Especialista", d=10, i=30, s=90, c=84),
        DiscPersonality(name="Asesor", d=20, i=90, s=90, c=16),
        DiscPersonality(name="Torbellino", d=70, i=70, s=5, c=70),
        DiscPersonality(name="Perfeccionista", d=40, i=30, s=40, c=95),
        DiscPersonality(name="Analista", d=30, i=16, s=84, c=90),
        DiscPersonality(name="Acomodadizo", d=5, i=40, s=80, c=95),
        DiscPersonality(name="Creador", d=80, i=30, s=30, c=80),
        DiscPersonality(name="Individualista", d=70, i=80, s=70, c=5),
        DiscPersonality(name="Patrones uniformes", d=60, i=50, s=60, c=60),
    )

    class DiscUserPersonality:
        class DiscResults(NamedTuple):
            positives: DiscInput.DiscTuple
            negatives: DiscInput.DiscTuple
            compounds: DiscInput.DiscTuple

        def Compounds(self):
            return DiscInput.DiscTuple(
                self.positives[DiscInput.DiscDomain.DOMINANCE]
                - self.negatives[DiscInput.DiscDomain.DOMINANCE],
                self.positives[DiscInput.DiscDomain.INFLUENCE]
                - self.negatives[DiscInput.DiscDomain.INFLUENCE],
                self.positives[DiscInput.DiscDomain.STEADINESS]
                - self.negatives[DiscInput.DiscDomain.STEADINESS],
                self.positives[DiscInput.DiscDomain.CONSCIENTIOUSNESS]
                - self.negatives[DiscInput.DiscDomain.CONSCIENTIOUSNESS],
            )

        def Positives(self):
            return DiscInput.DiscTuple(
                self.positives[DiscInput.DiscDomain.DOMINANCE],
                self.positives[DiscInput.DiscDomain.INFLUENCE],
                self.positives[DiscInput.DiscDomain.STEADINESS],
                self.positives[DiscInput.DiscDomain.CONSCIENTIOUSNESS],
            )

        def Negatives(self):
            return DiscInput.DiscTuple(
                self.negatives[DiscInput.DiscDomain.DOMINANCE],
                self.negatives[DiscInput.DiscDomain.INFLUENCE],
                self.negatives[DiscInput.DiscDomain.STEADINESS],
                self.negatives[DiscInput.DiscDomain.CONSCIENTIOUSNESS],
            )

        def Results(self):
            return self.DiscResults(
                positives=self.Positives(),
                negatives=self.Negatives(),
                compounds=self.Compounds(),
            )

        class AddPositive:
            def UpdateScore(self, personality, domain):
                personality.positives[domain] += 1

        class AddNegative:
            def UpdateScore(self, personality, domain):
                personality.negatives[domain] += 1

        def __init__(self):
            self.positives = {
                DiscInput.DiscDomain.DOMINANCE: 0,
                DiscInput.DiscDomain.INFLUENCE: 0,
                DiscInput.DiscDomain.STEADINESS: 0,
                DiscInput.DiscDomain.CONSCIENTIOUSNESS: 0,
            }
            self.negatives = {
                DiscInput.DiscDomain.DOMINANCE: 0,
                DiscInput.DiscDomain.INFLUENCE: 0,
                DiscInput.DiscDomain.STEADINESS: 0,
                DiscInput.DiscDomain.CONSCIENTIOUSNESS: 0,
            }
            self.actions = {
                "add": self.AddPositive(),
                "substract": self.AddNegative(),
            }

        def Execute(self, order):
            action, domain = order
            action = self.actions[action]
            action.UpdateScore(self, domain)

    @property
    def results(self):
        user_personality = DiscInput.DiscUserPersonality()
        input_pattern = re.compile("^Q.*Input$")

        input_classes = [c for c in dir(DiscInput) if input_pattern.match(c)]
        input_classes.sort(key=len)

        for class_name in input_classes:
            input_class = getattr(DiscInput, class_name)
            question_number = re.findall(r"\d+", class_name)[0]

            plus_value = getattr(self, f"q{question_number}_plus")
            plus_domain = DiscInput.MAPPINGS[input_class][
                input_class(plus_value)
            ]

            minus_value = getattr(self, f"q{question_number}_minus")
            minus_domain = DiscInput.MAPPINGS[input_class][
                input_class(minus_value)
            ]

            user_personality.Execute(("add", plus_domain))
            user_personality.Execute(("substract", minus_domain))

        return user_personality.Results()

    @property
    def baremos(self):
        compounds = self.results.compounds
        return DiscInput.DiscTuple(
            d=DiscInput.BAREMOS[DiscInput.DiscDomain.DOMINANCE][
                str(compounds.d)
            ],
            i=DiscInput.BAREMOS[DiscInput.DiscDomain.INFLUENCE][
                str(compounds.i)
            ],
            s=DiscInput.BAREMOS[DiscInput.DiscDomain.STEADINESS][
                str(compounds.s)
            ],
            c=DiscInput.BAREMOS[DiscInput.DiscDomain.CONSCIENTIOUSNESS][
                str(compounds.c)
            ],
        )

    def _GetPersonality(self, baremos):
        d, i, s, c = baremos
        personality_aux = self.DiscPersonality(name="TBD", d=d, i=i, s=s, c=c)

        closest_distance = self.PERSONALITIES[0].distance(personality_aux)
        closest_personality = self.PERSONALITIES[0]

        for personality in self.PERSONALITIES[1:]:
            distance = personality.distance(personality_aux)
            if distance < closest_distance:
                closest_distance = distance
                closest_personality = personality

        return closest_personality

    @property
    def personality(self):
        return self._GetPersonality(self.baremos)


class CareerAnchorsInput(models.Model):
    QUESTION_CHOICES = ((1, ""), (2, ""), (3, ""), (4, ""), (5, ""), (6, ""))
    FAVORITE_CHOICES = [(i, i) for i in range(1, 41)]

    onboard = models.OneToOneField(
        Onboard, on_delete=models.CASCADE, primary_key=True
    )

    q1 = models.IntegerField(choices=QUESTION_CHOICES)
    q2 = models.IntegerField(choices=QUESTION_CHOICES)
    q3 = models.IntegerField(choices=QUESTION_CHOICES)
    q4 = models.IntegerField(choices=QUESTION_CHOICES)
    q5 = models.IntegerField(choices=QUESTION_CHOICES)
    q6 = models.IntegerField(choices=QUESTION_CHOICES)
    q7 = models.IntegerField(choices=QUESTION_CHOICES)
    q8 = models.IntegerField(choices=QUESTION_CHOICES)
    q9 = models.IntegerField(choices=QUESTION_CHOICES)
    q10 = models.IntegerField(choices=QUESTION_CHOICES)
    q11 = models.IntegerField(choices=QUESTION_CHOICES)
    q12 = models.IntegerField(choices=QUESTION_CHOICES)
    q13 = models.IntegerField(choices=QUESTION_CHOICES)
    q14 = models.IntegerField(choices=QUESTION_CHOICES)
    q15 = models.IntegerField(choices=QUESTION_CHOICES)
    q16 = models.IntegerField(choices=QUESTION_CHOICES)
    q17 = models.IntegerField(choices=QUESTION_CHOICES)
    q18 = models.IntegerField(choices=QUESTION_CHOICES)
    q19 = models.IntegerField(choices=QUESTION_CHOICES)
    q20 = models.IntegerField(choices=QUESTION_CHOICES)
    q21 = models.IntegerField(choices=QUESTION_CHOICES)
    q22 = models.IntegerField(choices=QUESTION_CHOICES)
    q23 = models.IntegerField(choices=QUESTION_CHOICES)
    q24 = models.IntegerField(choices=QUESTION_CHOICES)
    q25 = models.IntegerField(choices=QUESTION_CHOICES)
    q26 = models.IntegerField(choices=QUESTION_CHOICES)
    q27 = models.IntegerField(choices=QUESTION_CHOICES)
    q28 = models.IntegerField(choices=QUESTION_CHOICES)
    q29 = models.IntegerField(choices=QUESTION_CHOICES)
    q30 = models.IntegerField(choices=QUESTION_CHOICES)
    q31 = models.IntegerField(choices=QUESTION_CHOICES)
    q32 = models.IntegerField(choices=QUESTION_CHOICES)
    q33 = models.IntegerField(choices=QUESTION_CHOICES)
    q34 = models.IntegerField(choices=QUESTION_CHOICES)
    q35 = models.IntegerField(choices=QUESTION_CHOICES)
    q36 = models.IntegerField(choices=QUESTION_CHOICES)
    q37 = models.IntegerField(choices=QUESTION_CHOICES)
    q38 = models.IntegerField(choices=QUESTION_CHOICES)
    q39 = models.IntegerField(choices=QUESTION_CHOICES)
    q40 = models.IntegerField(choices=QUESTION_CHOICES)

    favorite1 = models.IntegerField(choices=FAVORITE_CHOICES, default=None)
    favorite2 = models.IntegerField(choices=FAVORITE_CHOICES, default=None)
    favorite3 = models.IntegerField(choices=FAVORITE_CHOICES, default=None)

    class ScoredCareerAnchor:
        def __init__(self, name: str, score: int):
            self.name = name
            self.score = score

    class ScoredCareerAnchorBuilder:
        def __init__(self, index: int, name: str):
            self.q_indexes = list(range(index, 41, 8))
            self.name = name

        def Build(self, answers: dict) -> CareerAnchorsInput.ScoredCareerAnchor:
            score = sum([answers.get(f"q{index}") for index in self.q_indexes])
            favorites = {
                answers["favorite1"],
                answers["favorite2"],
                answers["favorite3"],
            }
            if self._CanBeFavorite(favorites):
                score += 4
            return CareerAnchorsInput.ScoredCareerAnchor(self.name, score)

        def _CanBeFavorite(self, favorites: Set[int]) -> bool:
            return bool(favorites.intersection(self.q_indexes))

    CAREER_ANCHORS = [
        ScoredCareerAnchorBuilder(1, "Técnica Funcional"),
        ScoredCareerAnchorBuilder(2, "Dirección General"),
        ScoredCareerAnchorBuilder(3, "Autonomía - Independencia"),
        ScoredCareerAnchorBuilder(4, "Seguridad y Estabilidad"),
        ScoredCareerAnchorBuilder(5, "Creatividad Empresarial"),
        ScoredCareerAnchorBuilder(6, "Servicio-Dedicación a una causa"),
        ScoredCareerAnchorBuilder(7, "Exclusivamente desafío"),
        ScoredCareerAnchorBuilder(8, "Estilo de vida"),
    ]

    @property
    def TopThreeRanking(self) -> List[ScoredCareerAnchor]:

        career_anchor_model_values = model_to_dict(self)

        anchors = [
            anchor.Build(career_anchor_model_values)
            for anchor in self.CAREER_ANCHORS
        ]

        three_anchors_most_scored = self._RankThreeFirsts(anchors)

        return three_anchors_most_scored

    def _RankThreeFirsts(
        self, anchors: List[ScoredCareerAnchor]
    ) -> List[ScoredCareerAnchor]:
        return sorted(anchors, key=lambda anchor: anchor.score, reverse=True)[
            :3
        ]
