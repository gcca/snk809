# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import List, TypedDict

from django import forms

from . import models


class WhatsappprefixChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, country: models.Country):
        return f"{country.phonecode}"


class ResidencecountryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, country: models.Country):
        return country.name


class AffiliationData(TypedDict, total=False):
    email: str
    displayname: str
    fullname: str
    whatsappprefix: int
    whatsappnumber: int
    residencecountry: int
    residencecity: str
    allow_to_travel_country: bool
    allow_to_travel_city: bool
    role_frontend: bool
    role_backend: bool
    role_fullstack: bool
    role_mobile: bool
    role_qatesting: bool
    role_softwarearchitect: bool
    role_enterprisesolutiondeveloper: bool
    role_businessanalytics: bool
    role_qasecurity: bool
    role_solutionarchitect: bool
    role_cloudarchitect: bool
    role_devops: bool
    role_productmanager: bool
    role_productowner: bool
    role_scrummaster: bool
    role_agilecoach: bool
    role_dataengineer: bool
    role_datamodeler: bool
    role_datascience: bool
    role_machinelearning: bool
    role_designresearch: bool
    role_uxuidesigner: bool
    role_uxwriter: bool
    role_cxdesigner: bool
    role_graphicaldesigner: bool
    role_campaingmanager: bool
    role_creativewriter: bool
    role_growthmarketer: bool
    role_businessdeveloper: bool
    role_accountmanager: bool
    amount_minimum: int
    amount_wished: int
    availability: int
    modality: int
    resume: str
    network_linkedin: str
    network_github: str
    network_behance: str
    network_website: str
    interest_industry: List[int]
    interest_subject: List[int]
    english_reading: int
    english_writing: int
    english_talking: int


AffiliationFieldMap = {
    "whatsappprefix": WhatsappprefixChoiceField(
        queryset=models.Country.objects.all()
    ),
    "residencecountry": ResidencecountryChoiceField(
        queryset=models.Country.objects.all()
    ),
}

AffiliationFirstForm = forms.modelform_factory(
    models.Applicant,
    fields=(
        "email",
        "displayname",
        "fullname",
        "whatsappprefix",
        "whatsappnumber",
        "residencecountry",
        "residencecity",
        "allow_to_travel_country",
        "allow_to_travel_city",
    ),
    formfield_callback=lambda f, **e: AffiliationFieldMap[f.name]
    if f.name in AffiliationFieldMap
    else f.formfield(**e),
)

AffiliationSecondForm = forms.modelform_factory(
    models.Applicant,
    fields=(
        "role_frontend",
        "role_backend",
        "role_fullstack",
        "role_mobile",
        "role_qatesting",
        "role_softwarearchitect",
        "role_enterprisesolutiondeveloper",
        "role_businessanalytics",
        "role_qasecurity",
        "role_solutionarchitect",
        "role_cloudarchitect",
        "role_devops",
        "role_productmanager",
        "role_productowner",
        "role_scrummaster",
        "role_agilecoach",
        "role_dataengineer",
        "role_datamodeler",
        "role_datascience",
        "role_machinelearning",
        "role_designresearch",
        "role_uxuidesigner",
        "role_uxwriter",
        "role_cxdesigner",
        "role_graphicaldesigner",
        "role_campaingmanager",
        "role_creativewriter",
        "role_growthmarketer",
        "role_businessdeveloper",
        "role_accountmanager",
        "amount_minimum",
        "amount_wished",
        "availability",
        "modality",
    ),
)

AffiliationThirdForm = forms.modelform_factory(
    models.Applicant,
    fields=(
        "resume",
        "network_linkedin",
        "network_github",
        "network_behance",
        "network_website",
        "interest_industry",
        "interest_subject",
        "english_reading",
        "english_writing",
        "english_talking",
    ),
    labels={
        "resume": "Adjunta tu CV aquí",
        "network_linkedin": "Link de Linkedin",
        "network_github": "Link de Github",
        "network_behance": "Link de Behance",
        "network_website": "Link de tu website",
        "interest_industry": "Industrias",
        "interest_subject": "Áreas o proyectos",
        "english_reading": "Compresión lectora",
        "english_writing": "Escritura",
        "english_talking": "Conversación",
    },
)
