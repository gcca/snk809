# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import Any, Dict, Iterator, Tuple

from django import urls
from django.views.generic.base import TemplateView
from nomos.views.generic.sequence import CompleteView, StepView

from . import forms, mixins


class AffiliationFirstView(StepView):
    template_name = "applicating/affiliation/first.html"
    form_class = forms.AffiliationFirstForm
    success_url = urls.reverse_lazy("neonauts:applicating:affiliation:second")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        form = context["form"]
        if not form.instance.email:
            form["email"].initial = self.request.user.username
        return context


class AffiliationSecondView(StepView):
    template_name = "applicating/affiliation/second.html"
    form_class = forms.AffiliationSecondForm
    success_url = urls.reverse_lazy("neonauts:applicating:affiliation:third")

    softwaredevelopment_names = (
        "role_frontend",
        "role_backend",
        "role_fullstack",
        "role_mobile",
        "role_qatesting",
        "role_softwarearchitect",
        "role_enterprisesolutiondeveloper",
        "role_businessanalytics",
        "role_qasecurity",
    )

    operationmanagement_names = (
        "role_solutionarchitect",
        "role_cloudarchitect",
        "role_devops",
    )

    marketing_names = (
        "role_graphicaldesigner",
        "role_campaingmanager",
        "role_creativewriter",
        "role_growthmarketer",
    )

    managementbusinessagility_names = (
        "role_productmanager",
        "role_productowner",
        "role_scrummaster",
        "role_agilecoach",
    )

    datamanagementexploitation_names = (
        "role_dataengineer",
        "role_datamodeler",
        "role_datascience",
        "role_machinelearning",
    )

    productservicedesign_names = (
        "role_designresearch",
        "role_uxuidesigner",
        "role_uxwriter",
        "role_cxdesigner",
    )

    comercial_names = (
        "role_businessdeveloper",
        "role_accountmanager",
    )

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        form = context["form"]
        context["softwaredevelopment_fields"] = self.__FieldNames(
            form, self.softwaredevelopment_names
        )
        context["operationmanagement_fields"] = self.__FieldNames(
            form, self.operationmanagement_names
        )
        context["marketing_fields"] = self.__FieldNames(
            form, self.marketing_names
        )
        context["managementbusinessagility_fields"] = self.__FieldNames(
            form, self.managementbusinessagility_names
        )
        context["datamanagementexploitation_fields"] = self.__FieldNames(
            form, self.datamanagementexploitation_names
        )
        context["productservicedesign_fields"] = self.__FieldNames(
            form, self.productservicedesign_names
        )
        context["comercial_fields"] = self.__FieldNames(
            form, self.comercial_names
        )
        return context

    @staticmethod
    def __FieldNames(
        form: forms.AffiliationSecondForm, names: Tuple[str, ...]
    ) -> Iterator[forms.forms.BoundField]:
        return (form[name] for name in names)


class AffiliationThirdView(CompleteView):
    template_name = "applicating/affiliation/third.html"
    form_class = forms.AffiliationThirdForm
    success_url = urls.reverse_lazy("neonauts:applicating:affiliation:first")


class AffiliationCompletedView(TemplateView):
    template_name = "applicating/affiliation/completed.html"


class ConfigurationView(mixins.ConfigurationPermissionsMixin, TemplateView):
    template_name = "applicating/configuration.html"
