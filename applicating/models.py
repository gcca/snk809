# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from __future__ import annotations

from django.db import models

__all__ = [
    "Applicant",
    "Availability",
    "Country",
    "InterestIndustry",
    "InterestSubject",
    "EnglishReading",
    "EnglishTalking",
    "EnglishWriting",
    "Modality",
]


class Country(models.Model):
    name = models.CharField(max_length=64)
    phonecode = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Availability(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Modality(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class InterestIndustry(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class InterestSubject(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class EnglishReading(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class EnglishWriting(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class EnglishTalking(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


def resumepath(applicant: Applicant, name: str) -> str:
    return f"applicating/resumes/{applicant.id}/{name}"


class Applicant(models.Model):
    email = models.EmailField(max_length=128, db_index=True)
    displayname = models.CharField(max_length=64)
    fullname = models.CharField(max_length=128)
    whatsappprefix = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="whatsappprefix_applicant_set",
    )
    whatsappnumber = models.PositiveIntegerField()
    residencecountry = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="residencecountry_applicant_set",
    )
    residencecity = models.CharField(max_length=64)
    allow_to_travel_country = models.BooleanField()
    allow_to_travel_city = models.BooleanField()
    role_frontend = models.BooleanField()
    role_backend = models.BooleanField()
    role_fullstack = models.BooleanField()
    role_mobile = models.BooleanField()
    role_qatesting = models.BooleanField()
    role_softwarearchitect = models.BooleanField()
    role_enterprisesolutiondeveloper = models.BooleanField()
    role_businessanalytics = models.BooleanField()
    role_qasecurity = models.BooleanField()
    role_solutionarchitect = models.BooleanField()
    role_cloudarchitect = models.BooleanField()
    role_devops = models.BooleanField()
    role_productmanager = models.BooleanField()
    role_productowner = models.BooleanField()
    role_scrummaster = models.BooleanField()
    role_agilecoach = models.BooleanField()
    role_dataengineer = models.BooleanField()
    role_datamodeler = models.BooleanField()
    role_datascience = models.BooleanField()
    role_machinelearning = models.BooleanField()
    role_designresearch = models.BooleanField()
    role_uxuidesigner = models.BooleanField()
    role_uxwriter = models.BooleanField()
    role_cxdesigner = models.BooleanField()
    role_graphicaldesigner = models.BooleanField()
    role_campaingmanager = models.BooleanField()
    role_creativewriter = models.BooleanField()
    role_growthmarketer = models.BooleanField()
    role_businessdeveloper = models.BooleanField()
    role_accountmanager = models.BooleanField()
    amount_minimum = models.PositiveIntegerField()
    amount_wished = models.PositiveIntegerField()
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)
    resume = models.FileField(
        upload_to=resumepath,
        blank=True,
    )
    network_linkedin = models.URLField(max_length=128, blank=True)
    network_github = models.URLField(max_length=128, blank=True)
    network_behance = models.URLField(max_length=128, blank=True)
    network_website = models.URLField(max_length=128, blank=True)
    interest_industry = models.ManyToManyField(InterestIndustry)
    interest_subject = models.ManyToManyField(InterestSubject)
    english_reading = models.ForeignKey(
        EnglishReading,
        on_delete=models.CASCADE,
    )
    english_writing = models.ForeignKey(
        EnglishWriting, on_delete=models.CASCADE
    )
    english_talking = models.ForeignKey(
        EnglishTalking, on_delete=models.CASCADE
    )
