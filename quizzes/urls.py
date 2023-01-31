# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.urls import path

from . import views

app_name = "quizzes"

urlpatterns = [
    path(
        "<int:quiz_id>/evaluate/<int:freelancer_id>/",
        views.EvaluateView.as_view(),
        name="evaluate",
    ),
    path(
        "evaluations/", views.EvaluationListView.as_view(), name="evaluations"
    ),
    path(
        "answers/<int:evaluation_id>/",
        views.EvaluationDetailView.as_view(),
        name="answers",
    ),
    path(
        "for/<int:freelancer_id>/", views.QuizzesForView.as_view(), name="for"
    ),
]
