# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

"""snk809 URL Configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="luci/")),
    path("luci/", include("sinek.interface.site.urls")),
    path("sinek/rc/", include("sinek.interface.rc.urls")),
    path("accounts/login/", RedirectView.as_view(url="/luci/account/signin")),
    path("neodash/", include("neodash.urls")),
    path("neodash/onboard/", include("onboard.urls")),
    path("neodash/customers/", include("customers.urls")),
    path("neoadmin/", admin.site.urls),
    path("neonauts/", include("neonauts.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("devtools/", include("devtools.urls")))
