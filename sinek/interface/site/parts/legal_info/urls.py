from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'legal-info'

urlpatterns = [
  path(
    'terms-and-conditions/',
    views.TermsAndConditionsView.as_view(),
    name='terms-and-conditions'),
  path(
    'data-policy/',
    views.DataPolicyView.as_view(),
    name='data-policy'),
  path(
    'cookies-policy/',
    views.CookiesPolicyView.as_view(),
    name='cookies-policy'),
]
