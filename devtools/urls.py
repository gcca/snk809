# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.urls import path

from . import views

app_name = "devtools"

urlpatterns = [
    path("autologin/", views.AutoLogin.as_view(), name="dashboard"),
]
