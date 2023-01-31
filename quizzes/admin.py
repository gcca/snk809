# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.contrib import admin

from .models import (
    MultiSelectQuestion,
    Option,
    Question,
    Quiz,
    SingleSelectQuestion,
)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


class OptionsStackedInline(admin.StackedInline):
    model = Option
    extra = 1


@admin.register(SingleSelectQuestion)
class SingleSelectQuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsStackedInline]


@admin.register(MultiSelectQuestion)
class MultiSelectQuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsStackedInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass
