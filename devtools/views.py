# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.contrib.auth.views import LoginView


class AutoLogin(LoginView):
    def get(self, request):
        from django.contrib.auth import authenticate, login

        user = authenticate(username="admin", password="admin")
        login(request, user)

        from django import urls
        from django.shortcuts import redirect

        return redirect(urls.reverse("onboard:dashboard"))
