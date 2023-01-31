# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from enum import IntEnum, auto
from typing import Tuple

from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    OneToOneField,
    TextField,
)

from sinek.infrastructure.persistence.orm.models import Freelancer


class Quiz(Model):
    class ID(IntEnum):
        """Progresivamente se irá agregando más tipos de quizzes."""

        UNKNOWN = 0
        DISC = auto()

    id = IntegerField(primary_key=True)
    title = CharField(max_length=256)
    description = TextField(max_length=2048)


class Question(Model):
    text = TextField(max_length=2048)
    quiz = ForeignKey(Quiz, related_name="questions", on_delete=CASCADE)


class SelectQuestion(Question):
    question = OneToOneField(
        Question,
        related_name="as_selectQuestion",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )


class Option(Model):
    question = ForeignKey(
        SelectQuestion, related_name="options", on_delete=CASCADE
    )
    text = CharField(max_length=512)


class SingleSelectQuestion(SelectQuestion):
    selectQuestion = OneToOneField(
        SelectQuestion,
        related_name="as_singleSelectQuestion",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )


class MultiSelectQuestion(SelectQuestion):
    selectQuestion = OneToOneField(
        SelectQuestion,
        related_name="as_multiSelectQuestion",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )


class DiscSelectQuestion(SelectQuestion):
    selectQuestion = OneToOneField(
        SelectQuestion,
        related_name="as_discSelectQuestion",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )


class OpenQuestion(Question):
    question = OneToOneField(
        Question,
        related_name="as_openQuestion",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )


class UploadQuestion(Question):
    question = OneToOneField(
        Question,
        related_name="as_uploadQuestion",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )


class Evaluation(Model):
    quiz = ForeignKey(
        Quiz,
        related_name="evaluations",
        on_delete=CASCADE,
    )
    freelancer = ForeignKey(
        Freelancer,
        related_name="evaluations",
        on_delete=CASCADE,
    )


class Answer(Model):
    question = ForeignKey(
        Question,
        related_name="answers",
        on_delete=CASCADE,
    )
    evaluation = ForeignKey(
        Evaluation,
        related_name="answers",
        on_delete=CASCADE,
    )


class OpenAnswer(Answer):
    answer = OneToOneField(
        Answer,
        related_name="as_openAnswer",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )
    text = TextField(max_length=2048)


class SelectAnswer(Answer):
    answer = OneToOneField(
        Answer,
        related_name="as_selectAnswer",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )


class SingleSelectAnswer(SelectAnswer):
    selectAnswer = OneToOneField(
        SelectAnswer,
        related_name="as_singleSelectAnswer",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )
    option = ForeignKey(
        Option,
        on_delete=CASCADE,
    )


class MultiSelectAnswer(SelectAnswer):
    selectAnswer = OneToOneField(
        SelectAnswer,
        related_name="as_multiSelectAnswer",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )
    options = ManyToManyField(Option)


class DiscSelectAnswer(SelectAnswer):
    selectAnswer = OneToOneField(
        SelectAnswer,
        related_name="as_discSelectAnswer",
        on_delete=CASCADE,
        parent_link=True,
        primary_key=True,
    )
    mostOption = ForeignKey(
        Option,
        related_name="most_options",
        on_delete=CASCADE,
    )
    leastOption = ForeignKey(
        Option,
        related_name="least_options",
        on_delete=CASCADE,
    )


class Respondent(Freelancer):
    class Meta:
        proxy = True

    @staticmethod
    def AvailableQuizzes() -> Tuple[Quiz.ID]:
        return ((Quiz.ID.DISC.value, "Test personal"),)
