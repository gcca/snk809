# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.urls import include, path

from . import views

app_name = "onboard"


# -----------------------------------------------------------------------------
# applicant patterns


applicant_assessment_patterns = (
    (
        path("disc/", views.ApplicantAssessmentDiscView.as_view(), name="disc"),
        path(
            "tmms/",
            views.ApplicantAssessmentTmmsView.as_view(),
            name="tmms",
        ),
        path(
            "complex/",
            views.ApplicantAssessmentComplexInstructionsView.as_view(),
            name="complex",
        ),
        path(
            "career-anchors/",
            views.ApplicantAssessmentCareerAnchorsView.as_view(),
            name="career-anchors",
        ),
    ),
    "assessment",
)


applicant_onboard_patterns = (
    (
        path(
            "update/",
            views.ApplicantOnboardUpdateView.as_view(),
            name="update",
        ),
        path(
            "cv-upload/",
            views.ApplicantOnboardOptionCVUploadView.as_view(),
            name="cv-upload",
        ),
    ),
    "onboard",
)

applicant_patterns = (
    (
        path(
            "dashboard/",
            views.ApplicantDashboardView.as_view(),
            name="dashboard",
        ),
        path("list/", views.ApplicantListView.as_view(), name="list"),
        path("create/", views.ApplicantCreateView.as_view(), name="create"),
        path(
            "<int:applicant_id>/detail/",
            views.ApplicantDetailView.as_view(),
            name="detail",
        ),
        path(
            "<int:applicant_id>/update/",
            views.ApplicantUpdateView.as_view(),
            name="update",
        ),
        path(
            "<int:applicant_id>/resume/",
            views.ApplicantResumeView.as_view(),
            name="resume",
        ),
        path(
            "<int:applicant_id>/email/onboard/",
            views.ApplicantOnboardEmailView.as_view(),
            name="email-onboard",
        ),
        path(
            "<int:applicant_id>/email/sent/",
            views.ApplicantEmailSentView.as_view(),
            name="email-sent",
        ),
        path(
            "<int:applicant_id>/assessment/",
            include(applicant_assessment_patterns),
        ),
        path(
            "<int:applicant_id>/onboard/", include(applicant_onboard_patterns)
        ),
    ),
    "applicant",
)


# -----------------------------------------------------------------------------
# onboard patterns


assessment_patterns = (
    (
        path(
            "1/",
            views.OnboardAssessmentDiscView.as_view(),
            name="disc",
        ),
        path("2/", views.OnboardAssessmentTmmsView.as_view(), name="tmms"),
        path(
            "3/",
            views.OnboardAssessmentComplexInstructionsView.as_view(),
            name="complex",
        ),
        path(
            "4/",
            views.OnboardAssessmentCareerAnchorsView.as_view(),
            name="career-anchors",
        ),
    ),
    "assessment",
)


onboard_patterns = (
    (
        path(
            "<slug:slug>/",
            views.OnboardDashboardView.as_view(),
            name="dashboard",
        ),
        path(
            "<slug:slug>/resume/",
            views.OnboardResumeView.as_view(),
            name="resume",
        ),
        path(
            "<slug:slug>/saved/",
            views.OnboardSavedView.as_view(),
            name="saved",
        ),
        path(
            "<slug:slug>/already/saved/",
            views.OnboardAlreadySavedView.as_view(),
            name="already-saved",
        ),
        path(
            "<slug:slug>/toggle-visibility/<str:assessment_name>",
            views.AssessmentVisibilityToggleView.as_view(),
            name="toggle-visibility",
        ),
        path(
            "<slug:slug>/googleform-toggle-visibility/<int:googleform_id>",
            views.AssessmentVisibilityGoogleFormToggleView.as_view(),
            name="googleform-toggle-visibility",
        ),
        path("<slug:slug>/assessment/", include(assessment_patterns)),
        path(
            "<slug:slug>/googleform/<int:googleform_id>/",
            views.OnboardGoogleFormEmbedView.as_view(),
            name="googleform",
        ),
    ),
    "onboard",
)


# -----------------------------------------------------------------------------
# google form tests patterns


google_form_patterns = (
    (
        path(
            "dashboard/",
            views.GoogleFormDashboardView.as_view(),
            name="dashboard",
        ),
        path("list/", views.GoogleFormListView.as_view(), name="list"),
        path("create/", views.GoogleFormCreateView.as_view(), name="create"),
        path(
            "<int:googleform_id>/update/",
            views.GoogleFormUpdateView.as_view(),
            name="update",
        ),
        path(
            "<int:googleform_id>/detail/",
            views.GoogleFormDetailView.as_view(),
            name="detail",
        ),
    ),
    "googleform",
)


urlpatterns = (
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("applicant/", include(applicant_patterns)),
    path("onboard/", include(onboard_patterns)),
    path("googleform/", include(google_form_patterns)),
)
