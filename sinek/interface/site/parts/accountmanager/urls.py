from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'accountmanager'

urlpatterns = [
  path(
    '',
    RedirectView.as_view(
      url='freelancers/')),
  path(
    'dashboard/',
    views.DashboardView.as_view(),
    name='dashboard'),
  path(
    'new-project/',
    views.CreateProjectView.as_view(),
    name='new-project'),
  path(
    'freelancers/',
    views.FreelancerListView.as_view(),
    name='freelancer-list'),
  path(
    'freelancer-info/<str:email>',
    views.FreelancerInfoView.as_view(),
    name='freelancer-info'),
  path(
    'freelancer-info/<str:email>/cv-open/<str:fileName>/',
    views.CVOpenView.as_view(),
    name='cv-open'),
  path(
    'freelancer-info/<str:email>/file-open/<str:fileName>/',
    views.FileOpenView.as_view(),
    name='file-open'),
  path(
    'dashboard-freelancer/',
    views.FreelancerDashboardView.as_view(),
    name='dashboard-freelancer'),
  path(
    'initiatives/',
    views.InitiativeListView.as_view(),
    name='initiative-list'),
  path(
    'new-initiative/',
    views.NewInitiativeView.as_view(),
    name='new-initiative'),
  path(
    'quotation-initiative/<str:initiativeCode>/',
    views.QuotationView.as_view(),
    name='quotation'),
  path(
    'update-initiative/',
    views.InitiativeUpdateView.as_view(),
    name='update-initiative'),
]
