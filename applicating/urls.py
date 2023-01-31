# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import Type

from django.urls import URLPattern, include, path
from nomos.urls import model_patterns

from . import mixins, models, views

app_name = "applicating"

affiliation_patterns = (
    (
        path("first/", views.AffiliationFirstView.as_view(), name="first"),
        path("second/", views.AffiliationSecondView.as_view(), name="second"),
        path("third/", views.AffiliationThirdView.as_view(), name="third"),
    ),
    "affiliation",
)


def configurationpath(
    name: str, model: Type[models.models.Model]
) -> URLPattern:
    return path(
        name,
        include(
            model_patterns(
                model,
                "neonauts:applicating:configuration",
                (mixins.ConfigurationPermissionsMixin,),
            )
        ),
    )


configuration_patterns = (
    (
        path("", views.ConfigurationView.as_view(), name="menu"),
        configurationpath("country/", models.Country),
        configurationpath("modality/", models.Modality),
        configurationpath("availability/", models.Availability),
        configurationpath("interest-industry/", models.InterestIndustry),
        configurationpath("interest-subject/", models.InterestSubject),
        configurationpath("english-reading/", models.EnglishReading),
        configurationpath("english-writing/", models.EnglishWriting),
        configurationpath("english-talking/", models.EnglishTalking),
    ),
    "configuration",
)

urlpatterns = (
    path("affiliation/", include(affiliation_patterns)),
    path("configuration/", include(configuration_patterns)),
)
