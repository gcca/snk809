from django.urls import path

from . import views

app_name = 'freelancer'

urlpatterns = [
  path(
    'knowledge-update/',
    views.KnowledgeUpdateView.as_view(),
    name='knowledge-update'),
  path(
    'knowledge-delete/',
    views.KnowledgeDeleteView.as_view(),
    name='knowledge-delete'),
  path(
    'personal-update/',
    views.PersonalUpdateView.as_view(),
    name='personal-update'),
  path(
    'configuration-update/',
    views.InterestUpdateView.as_view(),
    name='interest-update'),
  path(
    'business-update/',
    views.BusinessUpdateView.as_view(),
    name='business-update'),
  path(
    'project-update/',
    views.ProjectUpdateView.as_view(),
    name='project-update'),
  path(
    'network-update/',
    views.NetworkUpdateView.as_view(),
    name='network-update'),
  path(
    'network-delete/',
    views.NetworkDeleteView.as_view(),
    name='network-delete'),
  path(
    'file-upload/',
    views.FileUploadView.as_view(),
    name='file-upload'),
  path(
    'file-delete/',
    views.FileDeleteView.as_view(),
    name='file-delete'),
  path(
    'cv-upload/',
    views.CVUploadView.as_view(),
    name='cv-upload'),
  path(
    'cv-delete/',
    views.CVDeleteView.as_view(),
    name='cv-delete'),
  path(
    'auto-skills/',
    views.PortfolioAutoSkillsView.as_view(),
    name='auto-skills'),
  # New URLS
  path(
    'first-step/',
    views.FirstStepView.as_view(),
    name='first-step'),
  path(
    'second-step/',
    views.SecondStepView.as_view(),
    name='second-step'),
  path(
    'cv-upload-wizard/',
    views.CVUploadWizardView.as_view(),
    name='cv-upload-wizard'),
  path(
    'third-step/',
    views.ThirdStepView.as_view(),
    name='third-step'),
  path(
    'fourth-step/',
    views.FourthStepView.as_view(),
    name='fourth-step')
]
