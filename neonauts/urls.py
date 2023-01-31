# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.urls import include, path

from . import views

app_name = "neonauts"


user_patterns = (
    (
        path(
            "password-change",
            views.UserPasswordChangeView.as_view(),
            name="password-change",
        ),
        path(
            "password-change-done",
            views.UserPasswordChangeDoneView.as_view(),
            name="password-change-done",
        ),
    ),
    "user",
)

urlpatterns = (
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("applicating/", include("applicating.urls")),
    path("user/", include(user_patterns)),
)
