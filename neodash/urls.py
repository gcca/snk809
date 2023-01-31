# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.urls import include, path

from . import views

app_name = "neodash"


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
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("user/", include(user_patterns)),
)
