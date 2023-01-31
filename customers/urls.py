# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.urls import path

from . import views

app_name = "customers"

urlpatterns = (
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("list/", views.ListView.as_view(), name="list"),
    path("create/", views.CreateView.as_view(), name="create"),
    path(
        "<int:customer_id>/detail/", views.DetailView.as_view(), name="detail"
    ),
    path(
        "<int:customer_id>/update/", views.UpdateView.as_view(), name="update"
    ),
)
