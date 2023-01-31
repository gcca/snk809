from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'freelancer'

urlpatterns = [
  path('', RedirectView.as_view(url='profile-wizard/')),
  path('profile/', views.ProfileView.as_view(), name='profile'),
  path('profile-wizard/', views.ProfileWizardView.as_view(), name='profile-wizard'),
]
