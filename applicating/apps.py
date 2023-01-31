# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.apps import AppConfig


class ApplicatingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applicating"
    verbose_name = "Snk809 applicant proocesses"
