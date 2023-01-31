# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

import contextlib
import os

from django import http, shortcuts, urls
from django.conf import settings
from django.core import mail
from django.db.models import Exists, OuterRef
from django.template.loader import get_template
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView

from . import forms, mixins, models

# -----------------------------------------------------------------------------
# views


class DashboardView(mixins.OnboardPermissionsMixin, TemplateView):
    template_name = "onboard/dashboard.html"


# -----------------------------------------------------------------------------
# applicant views


class ApplicantDashboardView(mixins.OnboardPermissionsMixin, TemplateView):
    template_name = "onboard/applicant/dashboard.html"


class ApplicantListView(mixins.OnboardPermissionsMixin, ListView):
    template_name = "onboard/applicant/list.html"
    model = models.Applicant


class ApplicantCreateView(mixins.OnboardPermissionsMixin, CreateView):
    template_name = "onboard/applicant/form.html"
    success_url = urls.reverse_lazy("onboard:applicant:list")
    model = models.Applicant
    fields = "__all__"

    def form_valid(self, form):
        response = super().form_valid(form)

        applicant = form.instance
        slug = self.CreateSlug()

        # TODO: crear validaciones para retornar un internal error
        # si falla el guardado, tanto aquí como en el form de applicant
        models.Onboard.objects.create(applicant=applicant, slug=slug)

        return response

    # -----------------------------------------------------
    # TODO: Este view puede reducirse usando signal del orm
    # signal after_create -> create onboard (with slug)
    # -----------------------------------------------------

    @staticmethod
    def CreateSlug() -> str:
        from uuid import uuid1

        return uuid1().hex


class AssessmentVisibilityToggleView(
    mixins.OnboardPermissionsMixin, mixins.OnboardSlugCheckMixin, View
):
    def post(self, request, **kwargs):
        onboard = models.Onboard.objects.get(slug=self.kwargs["slug"])
        assessment_name = self.kwargs["assessment_name"]

        actions = {
            "disc": onboard.ToggleDisc,
            "tmms": onboard.ToggleTmms,
            "complex_instructions": onboard.ToggleComplexInstructions,
            "career_anchors": onboard.ToggleCareerAnchors,
        }

        try:
            actions[assessment_name]()
        except KeyError:
            return http.HttpResponseBadRequest()

        onboard.save()

        redirect_url = urls.reverse(
            "onboard:applicant:detail",
            kwargs={"applicant_id": onboard.applicant.id},
        )

        return shortcuts.redirect(redirect_url)


class AssessmentVisibilityGoogleFormToggleView(
    mixins.OnboardPermissionsMixin, mixins.OnboardSlugCheckMixin, View
):
    def post(self, request, **kwargs):
        onboard = models.Onboard.objects.get(slug=self.kwargs["slug"])
        googleform_id = self.kwargs["googleform_id"]

        googleform_model = models.GoogleForm.objects.get(id=googleform_id)

        if onboard.google_forms.filter(id=googleform_model.id).exists():
            onboard.google_forms.remove(googleform_model)
        else:
            onboard.google_forms.add(googleform_model)

        onboard.save()

        redirect_url = urls.reverse(
            "onboard:applicant:detail",
            kwargs={"applicant_id": onboard.applicant.id},
        )

        return shortcuts.redirect(redirect_url)


class ApplicantDetailView(mixins.OnboardPermissionsMixin, DetailView):
    template_name = "onboard/applicant/detail.html"
    model = models.Applicant
    pk_url_kwarg = "applicant_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["googleforms"] = self.CheckedGoogleForms()
        return context

    def CheckedGoogleForms(self):
        checked_googleforms = self.object.onboard.google_forms.filter(
            id=OuterRef("pk")
        )
        return models.GoogleForm.objects.annotate(
            checked=Exists(checked_googleforms)
        ).values("id", "title", "view_link", "checked")


class ApplicantResumeView(mixins.OnboardPermissionsMixin, View):
    def get(self, request, applicant_id):
        applicant = shortcuts.get_object_or_404(
            models.Applicant, id=applicant_id
        )

        resume = applicant.onboard.resume

        return http.FileResponse(
            resume.file,
            as_attachment=True,
            filename=os.path.basename(resume.name),
        )


class ApplicantUpdateView(mixins.OnboardPermissionsMixin, UpdateView):
    template_name = "onboard/applicant/form.html"
    success_url = urls.reverse_lazy("onboard:applicant:list")
    model = models.Applicant
    fields = "__all__"
    pk_url_kwarg = "applicant_id"


class ApplicantOnboardUpdateView(mixins.OnboardPermissionsMixin, UpdateView):
    template_name = "onboard/applicant/onboard/form.html"
    model = models.Onboard
    fields = (
        "process_name",
        "process_link",
    )
    pk_url_kwarg = "applicant_id"

    def get_success_url(self):
        return urls.reverse(
            "onboard:applicant:detail",
            kwargs={"applicant_id": self.kwargs["applicant_id"]},
        )


# -----------------------------------------------------------------------------
# applicant views / assessments


class BaseApplicantAssessmentView(mixins.OnboardPermissionsMixin, DetailView):
    fields = "__all__"
    pk_url_kwarg = "applicant_id"
    slug_field = "onboard__slug"


class ApplicantAssessmentDiscView(BaseApplicantAssessmentView):
    template_name = "onboard/applicant/assessment/disc.html"
    model = models.DiscInput


class ApplicantAssessmentTmmsView(BaseApplicantAssessmentView):
    template_name = "onboard/applicant/assessment/tmms.html"
    model = models.TmmsInput


class ApplicantAssessmentComplexInstructionsView(BaseApplicantAssessmentView):
    template_name = "onboard/applicant/assessment/complex-instructions.html"
    model = models.ComplexInstructionsInput


class ApplicantAssessmentCareerAnchorsView(BaseApplicantAssessmentView):
    template_name = "onboard/applicant/assessment/career-anchors.html"
    model = models.CareerAnchorsInput


# -----------------------------------------------------------------------------
# applicant options views


class ApplicantOnboardOptionCVUploadView(
    mixins.OnboardPermissionsMixin, UpdateView
):
    template_name = "onboard/applicant/options/cv-upload.html"
    model = models.Onboard
    fields = (
        "resume",
        "show_resume",
    )
    pk_url_kwarg = "applicant_id"

    def get_success_url(self):
        return urls.reverse(
            "onboard:applicant:detail",
            kwargs={"applicant_id": self.kwargs["applicant_id"]},
        )


# -----------------------------------------------------------------------------
# onboard views


class OnboardDashboardView(mixins.OnboardSlugCheckMixin, TemplateView):
    template_name = "onboard/onboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs["slug"]
        onboard = models.Onboard.objects.get(slug=slug)

        context["resume_form"] = forms.OnboardResumeForm(instance=onboard)
        context["googleforms"] = onboard.google_forms.all()
        context["onboard"] = onboard

        return context


class OnboardResumeView(mixins.OnboardSlugCheckMixin, UpdateView):
    model = models.Onboard
    fields = ("resume",)
    pk_url_kwarg = None

    def get_success_url(self):
        return urls.reverse(
            "onboard:onboard:saved",
            kwargs={"slug": self.kwargs["slug"]},
        )


class OnboardSavedView(mixins.OnboardSlugCheckMixin, TemplateView):
    template_name = "onboard/onboard/saved.html"


class OnboardAlreadySavedView(mixins.OnboardSlugCheckMixin, TemplateView):
    template_name = "onboard/onboard/already-saved.html"


class BaseOnboardAssessmentView(
    mixins.OnboardSlugCheckMixin, mixins.AlreadySavedAssessmentMixin, FormView
):
    class DiscDisplayValidator:
        def validate(self, onboard: models.Onboard):
            return onboard.show_disc

    class TmmsDisplayValidator:
        def validate(self, onboard: models.Onboard):
            return onboard.show_tmms

    class CareerAnchorsDisplayValidator:
        def validate(self, onboard: models.Onboard):
            return onboard.show_career_anchors

    class ComplexInstructionsDisplayValidator:
        def validate(self, onboard: models.Onboard):
            return onboard.show_complex_instructions

    model = None

    validators = {
        models.DiscInput: DiscDisplayValidator(),
        models.TmmsInput: TmmsDisplayValidator(),
        models.ComplexInstructionsInput: ComplexInstructionsDisplayValidator(),
        models.CareerAnchorsInput: CareerAnchorsDisplayValidator(),
    }

    def _GetValidator(self):
        try:
            return self.validators[self.model]
        except KeyError:
            raise ValueError("Validator not defined for the given model")

    def get(self, request, *args, **kwargs):
        onboard = models.Onboard.objects.get(slug=self.kwargs["slug"])

        validator = self._GetValidator()

        if not validator.validate(onboard):
            return http.HttpResponseForbidden()

        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        onboard = models.Onboard.objects.get(slug=self.kwargs["slug"])
        query_name = self.model.onboard.field.related_query_name()

        with contextlib.suppress(self.model.DoesNotExist):
            kwargs["instance"] = getattr(onboard, query_name)

        return kwargs

    def form_valid(self, form):
        onboard = models.Onboard.objects.get(slug=self.kwargs["slug"])
        form.instance.onboard = onboard
        form.save()
        return super().form_valid(form)


class OnboardAssessmentTmmsView(BaseOnboardAssessmentView):
    template_name = "onboard/onboard/assessment/tmms.html"
    form_class = forms.TmmsForm
    model = models.TmmsInput


class OnboardAssessmentComplexInstructionsView(BaseOnboardAssessmentView):
    template_name = "onboard/onboard/assessment/complex-instructions.html"
    form_class = forms.ComplexInstructionsForm
    model = models.ComplexInstructionsInput


class OnboardAssessmentDiscView(BaseOnboardAssessmentView):
    template_name = "onboard/onboard/assessment/disc.html"
    form_class = forms.DiscForm
    model = models.DiscInput


class OnboardAssessmentCareerAnchorsView(BaseOnboardAssessmentView):
    template_name = "onboard/onboard/assessment/career-anchors.html"
    form_class = forms.CareerAnchorsFormFacade
    model = models.CareerAnchorsInput


class OnboardGoogleFormEmbedView(mixins.OnboardSlugCheckMixin, DetailView):
    template_name = "onboard/onboard/google-form.html"
    model = models.GoogleForm
    pk_url_kwarg = "googleform_id"


# -----------------------------------------------------------------------------
# google form views


class GoogleFormDashboardView(mixins.OnboardPermissionsMixin, TemplateView):
    template_name = "onboard/google_form/dashboard.html"


class GoogleFormListView(mixins.OnboardPermissionsMixin, ListView):
    template_name = "onboard/google_form/list.html"
    model = models.GoogleForm


class GoogleFormCreateView(mixins.OnboardPermissionsMixin, CreateView):
    template_name = "onboard/google_form/form.html"
    success_url = urls.reverse_lazy("onboard:googleform:list")
    model = models.GoogleForm
    fields = "__all__"


class GoogleFormDetailView(mixins.OnboardPermissionsMixin, DetailView):
    template_name = "onboard/google_form/detail.html"
    model = models.GoogleForm
    pk_url_kwarg = "googleform_id"


class GoogleFormUpdateView(mixins.OnboardPermissionsMixin, UpdateView):
    template_name = "onboard/google_form/form.html"
    success_url = urls.reverse_lazy("onboard:googleform:list")
    model = models.GoogleForm
    fields = "__all__"
    pk_url_kwarg = "googleform_id"


# -----------------------------------------------------------------------------
#  email views


class EmailSenderBaseView(TemplateView):
    message_template_name = None
    template_name = None

    # Patch: static content available only in www.domain
    # Scheme required
    def __get_static_host(self):
        host = self.request.get_host()
        host = host if "www" in host else f"www.{host}"
        return host if "https://" in host else f"https://{host}"

    def get_html_message(self, **kwargs):
        if self.message_template_name is None:
            return None

        template = get_template(self.message_template_name)
        context = self.get_context_data(**kwargs)

        context["static_host"] = self.__get_static_host()

        return template.render(context)

    def send_email(self, subject, recipient, message=None):
        mail.send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
            html_message=self.get_html_message(),
            fail_silently=False,
        )


class ApplicantOnboardEmailView(
    mixins.OnboardPermissionsMixin, EmailSenderBaseView
):
    message_template_name = "onboard/email/applicant-email.html"
    template_name = "onboard/email/send-confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applicant"] = models.Applicant.objects.get(
            id=self.kwargs["applicant_id"]
        )
        return context

    def post(self, request, **kwargs):
        applicant = models.Applicant.objects.get(id=self.kwargs["applicant_id"])

        self.send_email(
            "#Snk809Jobs | Avanzaste a la 1ª Etapa🎉 | Puesto:"
            f" {applicant.onboard.process_name}",
            applicant.email,
        )

        redirect_url = urls.reverse(
            "onboard:applicant:email-sent",
            kwargs={"applicant_id": self.kwargs["applicant_id"]},
        )

        return shortcuts.redirect(redirect_url)


class ApplicantEmailSentView(mixins.OnboardPermissionsMixin, TemplateView):
    template_name = "onboard/email/applicant-email-sent.html"
