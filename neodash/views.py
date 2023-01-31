# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django import urls
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import views as auth_views
from django.views.generic import base as views_base


class LoginView(auth_views.LoginView):
    template_name = "neodash/registration/login.html"
    next_page = urls.reverse_lazy("neodash:home")


class HomeView(auth_mixins.LoginRequiredMixin, views_base.TemplateView):
    login_url = "neodash:login"
    template_name = "neodash/home.html"


class UserPasswordChangeView(
    auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView
):
    template_name = "neodash/registration/password-change.html"
    success_url = urls.reverse_lazy("neodash:user:password-change-done")


class UserPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "neodash/registration/password-change-done.html"
