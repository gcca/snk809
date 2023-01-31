# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import Any, Dict

from django import forms

__all__ = ["SignupForm"]


class SignupForm(forms.Form):
    email = forms.CharField(max_length=64)
    email_confirm = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        max_length=64, widget=forms.PasswordInput
    )

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        if cleaned_data["email"] != cleaned_data["email_confirm"]:
            self.add_error("email_confirm", "Different emails")

        if cleaned_data["password"] != cleaned_data["password_confirm"]:
            self.add_error("password_confirm", "Different passwords")

        return cleaned_data
