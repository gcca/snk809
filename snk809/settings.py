# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

"""Django 4.0.2 settings for snk809 project."""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-4cc(eobu#08z$tu-h!u&5-_feiq@_5imfkksuri1mw8&3)vyd="
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "neom.apps.NeomConfig",
    "sinek.interface.apps.InterfaceConfig",
    "sinek.apps.SinekConfig",
    "neodash",
    "onboard",
    "customers",
    "applicating",
    "neonauts",
]

if DEBUG:
    INSTALLED_APPS.append("devtools")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "snk809.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {"neom_md2": "neom.kit.md2.templatetags.neom_md2"},
        },
    },
]

WSGI_APPLICATION = "snk809.wsgi.application"


# Backend

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "sinek.application.backends.GoogleBackend",
]


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# Internationalization

LANGUAGE_CODE = "es"  # "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = ((BASE_DIR / "neodash/locale"),)

# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "uploads/"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Google Oauth client information

GOOGLE_OAUTH2_BASE_DOMAIN_URL = "http://localhost:8000"

GOOGLE_OAUTH2_CLIENT_ID = (
    "576150906215-3h79jgm3ceib1p2hetlu9j3nt3m6fej8.apps.googleusercontent.com"
)

GOOGLE_OAUTH2_CLIENT_SECRET = "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"


# LUCI Main Google Drive Folder ID
LUCI_MAIN_FOLDER_ID = "17WaFcfUzh2HhEv_J-KO7XRyxcmQhocLs"


# LUCI BackUp Google Drive Folder ID
LUCI_BACKUP_MAIN_FOLDER_ID = "1vDH5gHldLgBNHqvCPY8ONSNQkBbkcCbN"


# SAT Google Spreadsheet ID
SAT_SPREADSHEET_ID = "1MoxQpqJAu_2GDu-nNiwVaGWwxqUymr8C5JifGTSRb34"


# Wire domain
# BIG TODO: wire actual domain to infrastructure


def NEOM_IOC_WIRES(manager):
    from sinek.domain.model.hunter import HunterRepository
    from sinek.infrastructure.persistence.orm.hunter import HunterRepositoryORM

    manager.wire(HunterRepository, HunterRepositoryORM)

    from sinek.domain.model.candidate import CandidateRepository
    from sinek.infrastructure.persistence.orm.candidate import (
        CandidateRepositoryORM,
    )

    manager.wire(CandidateRepository, CandidateRepositoryORM)

    from sinek.domain.model.personality_test.disc import DiscRecordRepository
    from sinek.infrastructure.persistence.orm.discrecord import (
        DiscRecordRepositoryORM,
    )

    manager.wire(DiscRecordRepository, DiscRecordRepositoryORM)

    from sinek.domain.model.personality_test.tmms24 import (
        TMMS24RecordRepository,
    )
    from sinek.infrastructure.persistence.orm.tmms24record import (
        TMMS24RecordRepositoryORM,
    )

    manager.wire(TMMS24RecordRepository, TMMS24RecordRepositoryORM)

    from sinek.domain.model.personality_test.anchor import (
        AnchorRecordRepository,
    )
    from sinek.infrastructure.persistence.orm.anchorrecord import (
        AnchorRecordRepositoryORM,
    )

    manager.wire(AnchorRecordRepository, AnchorRecordRepositoryORM)

    from sinek.domain.model.personality_test.complex import (
        ComplexRecordRepository,
    )
    from sinek.infrastructure.persistence.orm.complexrecord import (
        ComplexRecordRepositoryORM,
    )

    manager.wire(ComplexRecordRepository, ComplexRecordRepositoryORM)

    from sinek.domain.service import AffiliationService
    from sinek.domain.service_impl import AffiliationServiceImpl

    manager.wire(AffiliationService, AffiliationServiceImpl)

    from sinek.domain.service import DISCEvaluationService
    from sinek.domain.service_impl import DISCEvaluationServiceImpl

    manager.wire(DISCEvaluationService, DISCEvaluationServiceImpl)

    from sinek.domain.service import TMMS24EvaluationService
    from sinek.domain.service_impl import TMMS24EvaluationServiceImpl

    manager.wire(TMMS24EvaluationService, TMMS24EvaluationServiceImpl)

    from sinek.domain.service import AnchorEvaluationService
    from sinek.domain.service_impl import AnchorEvaluationServiceImpl

    manager.wire(AnchorEvaluationService, AnchorEvaluationServiceImpl)

    from sinek.domain.service import ComplexEvaluationService
    from sinek.domain.service_impl import ComplexEvaluationServiceImpl

    manager.wire(ComplexEvaluationService, ComplexEvaluationServiceImpl)

    from sinek.domain.service import RecordDISCAnswersService
    from sinek.domain.service_impl import RecordDISCAnswersServiceImpl

    manager.wire(RecordDISCAnswersService, RecordDISCAnswersServiceImpl)

    from sinek.domain.service import RecordTMMS24AnswersService
    from sinek.domain.service_impl import RecordTMMS24AnswersServiceImpl

    manager.wire(RecordTMMS24AnswersService, RecordTMMS24AnswersServiceImpl)

    from sinek.domain.service import RecordAnchorAnswersService
    from sinek.domain.service_impl import RecordAnchorAnswersServiceImpl

    manager.wire(RecordAnchorAnswersService, RecordAnchorAnswersServiceImpl)

    from sinek.domain.service import RecordComplexAnswersService
    from sinek.domain.service_impl import RecordComplexAnswersServiceImpl

    manager.wire(RecordComplexAnswersService, RecordComplexAnswersServiceImpl)

    from sinek.domain.service import CandidateTestChecklistService
    from sinek.domain.service_impl import CandidateTestChecklistServiceImpl

    manager.wire(
        CandidateTestChecklistService, CandidateTestChecklistServiceImpl
    )

    from sinek.application.account import UserRoleService
    from sinek.infrastructure.account import UserRoleServiceImpl

    manager.wire(UserRoleService, UserRoleServiceImpl)

    from sinek.domain.service import ProjectService
    from sinek.domain.service_impl import ProjectServiceImpl

    manager.wire(ProjectService, ProjectServiceImpl)

    from sinek.domain.service import ProfileService
    from sinek.domain.service_impl import ProfileServiceImpl

    manager.wire(ProfileService, ProfileServiceImpl)

    from sinek.domain.service import FreelancerKnowledgeTreeService
    from sinek.domain.service_impl import FreelancerKnowledgeTreeServiceImpl

    manager.wire(
        FreelancerKnowledgeTreeService, FreelancerKnowledgeTreeServiceImpl
    )

    from sinek.domain.service import FreelancerExperienceService
    from sinek.domain.service_impl import FreelancerExperienceServiceImpl

    manager.wire(FreelancerExperienceService, FreelancerExperienceServiceImpl)

    from sinek.domain.service import FreelancerPeriodService
    from sinek.domain.service_impl import FreelancerPeriodServiceImpl

    manager.wire(FreelancerPeriodService, FreelancerPeriodServiceImpl)

    from sinek.domain.model.project import ProjectRepository
    from sinek.infrastructure.persistence.orm.project import (
        ProjectRepositoryORM,
    )

    manager.wire(ProjectRepository, ProjectRepositoryORM)

    from sinek.domain.model.accountmanager import AccountManagerRepository
    from sinek.infrastructure.persistence.orm.accountmanager import (
        AccountManagerRepositoryORM,
    )

    manager.wire(AccountManagerRepository, AccountManagerRepositoryORM)

    from sinek.domain.model.staff import StaffRepository
    from sinek.infrastructure.persistence.orm.staff import StaffRepositoryORM

    manager.wire(StaffRepository, StaffRepositoryORM)

    from sinek.domain.model.freelancer import FreelancerRepository
    from sinek.infrastructure.persistence.orm.freelancer import (
        FreelancerRepositoryORM,
    )

    manager.wire(FreelancerRepository, FreelancerRepositoryORM)

    from sinek.domain.model.freelancer import CVRepository
    from sinek.infrastructure.persistence.orm.freelancer import CVRepositoryORM

    manager.wire(CVRepository, CVRepositoryORM)

    from sinek.domain.model.freelancer import FileRepository
    from sinek.infrastructure.persistence.orm.freelancer import (
        FileRepositoryORM,
    )

    manager.wire(FileRepository, FileRepositoryORM)

    from sinek.domain.model.initiative import InitiativeRepository
    from sinek.infrastructure.persistence.orm.initiative import (
        InitiativeGoogleSheetRepositoryORM,
    )

    manager.wire(InitiativeRepository, InitiativeGoogleSheetRepositoryORM)

    from sinek.domain.model.initiative import InitiativeQueryService
    from sinek.infrastructure.persistence.orm.initiative import (
        InitiativeGoogleSheetQueryService,
    )

    manager.wire(InitiativeQueryService, InitiativeGoogleSheetQueryService)

    from sinek.domain.model.freelancer import FreelancerCommandService
    from sinek.infrastructure.persistence.orm.freelancer import (
        FreelancerCommandServiceORM,
    )

    manager.wire(FreelancerCommandService, FreelancerCommandServiceORM)

    from sinek.domain.model.freelancer import FreelancerQueryService
    from sinek.infrastructure.persistence.orm.freelancer import (
        FreelancerQueryServiceORM,
    )

    manager.wire(FreelancerQueryService, FreelancerQueryServiceORM)

    from sinek.domain.model.skill import SkillQueryService
    from sinek.infrastructure.persistence.orm.skill import SkillQueryServiceORM

    manager.wire(SkillQueryService, SkillQueryServiceORM)

    from sinek.domain.model.skill import SkillRepository
    from sinek.infrastructure.persistence.orm.skill import SkillRepositoryORM

    manager.wire(SkillRepository, SkillRepositoryORM)

    from sinek.application.service import GoogleDriveService
    from sinek.infrastructure.service_impl import GoogleDriveServiceImpl

    manager.wire(GoogleDriveService, GoogleDriveServiceImpl)

    from sinek.domain.service import FreelancerCountTreeService
    from sinek.domain.service_impl import FreelancerCountTreeServiceImpl

    manager.wire(FreelancerCountTreeService, FreelancerCountTreeServiceImpl)

    from sinek.domain.service import InitiativeCreationService
    from sinek.domain.service_impl import InitiativeCreationServiceImpl

    manager.wire(InitiativeCreationService, InitiativeCreationServiceImpl)

    from sinek.domain.service import AutoKnowledgeService
    from sinek.domain.service_impl import AutoKnowledgeServiceImpl

    manager.wire(AutoKnowledgeService, AutoKnowledgeServiceImpl)


# Database population settings for neom


NEOM_POPULATION = {
    "DIR": BASE_DIR / "devtools" / "populators",
    "POPULATORS": [
        "superuser",
        "permissions",
        "users",
        "skills",
    ],
}


# Email settings

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
