# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django import shortcuts, urls
from django.contrib.auth import get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

from . import forms


class LoginView(auth_views.LoginView):
    template_name = "neonauts/registration/login.html"

    def get_default_redirect_url(self):
        return shortcuts.resolve_url("neonauts:applicating:affiliation:first")


class SignupView(auth_views.FormView):
    template_name = "neonauts/registration/signup.html"
    form_class = forms.SignupForm
    success_url = urls.reverse_lazy("neonauts:login")

    def form_valid(self, form: forms.SignupForm) -> HttpResponse:
        user_model = get_user_model()
        cleaned_data = form.cleaned_data
        user_model.objects.create_user(
            cleaned_data["email"],
            cleaned_data["email_confirm"],
            cleaned_data["password"],
        )
        return super().form_valid(form)


class UserPasswordChangeView(
    auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView
):
    template_name = "neonauts/registration/password-change.html"
    success_url = urls.reverse_lazy("neonauts:user:password-change-done")


class UserPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "neonauts/registration/password-change-done.html"
