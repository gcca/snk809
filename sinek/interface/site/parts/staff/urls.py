from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'staff'


urlpatterns = [
  path(
    '',
    RedirectView.as_view(
      url='dashboard/')),
  path(
    'dashboard/',
    views.DashboardView.as_view(),
    name='dashboard'),
  path(
    'new-hunter/',
    views.NewHunterView.as_view(),
    name='new-hunter'),
  path(
    'new-accountmanager/',
    views.NewAccountManagerView.as_view(),
    name='new-accountmanager'),
]
