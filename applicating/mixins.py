# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from neodash import mixins as neodash_mixins

from . import models

__all__ = ["ApplicantPermissionsMixin"]


class ApplicantPermissionsMixin(neodash_mixins.PermissionsModelMixin):
    login_url = "neonauts:login"
    model = models.Applicant


class ConfigurationPermissionsMixin(neodash_mixins.PermissionsModelsMixin):
    login_url = "neonauts:login"
    models = [
        models.Country,
        models.Availability,
        models.Modality,
        models.InterestIndustry,
        models.InterestSubject,
        models.EnglishReading,
        models.EnglishWriting,
        models.EnglishTalking,
    ]
