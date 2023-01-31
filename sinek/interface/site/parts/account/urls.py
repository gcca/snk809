from django.contrib.auth.views import logout_then_login
from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'account'


urlpatterns = [
  path(
    '',
    RedirectView.as_view(
      url='signup/')),
  path(
    'signin/',
    views.SignInView.as_view(),
    name='signin'),
  path(
    'default-login/',
    views.DefaultSignInView.as_view(),
    name='default-login'),
  path(
    'google-login/',
    views.GoogleSignInView.as_view(),
    name='google-login'),
  path(
    'signout/',
    logout_then_login,
    name='signout'),
  path(
    'signup/',
    views.SignUpView.as_view(),
    name='signup'),
  path('reset-session/', views.ResetSessionView.as_view(), name='reset-session')
  ]
