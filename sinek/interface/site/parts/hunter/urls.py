from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'hunter'


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
    'affiliation/',
    views.AffiliationView.as_view(),
    name='affiliation'),
  path(
    'candidate/<str:email>/',
    views.CandidateInformation.as_view(),
    name='candidate-info'),
  path(
    'candidate/<str:email>/personality_test/disc',
    views.CandidateTestResultDisc.as_view(),
    name='candidate-result-disc'),
  path(
    'candidate/<str:email>/personality_test/tmms24',
    views.CandidateTestResultTMMS24.as_view(),
    name='candidate-result-tmms24'),
  path(
    'candidate/<str:email>/personality_test/anchor',
    views.CandidateTestResultAnchor.as_view(),
    name='candidate-result-anchor'),
  path(
    'candidate/<str:email>/personality_test/complex',
    views.CandidateTestResultComplex.as_view(),
    name='candidate-result-complex'),
]
