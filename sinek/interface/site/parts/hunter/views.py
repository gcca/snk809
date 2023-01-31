from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from neom.core.ioc import AutoWire, Wireable, Wired

from sinek.domain.model.candidate import CandidateRepository
from sinek.domain.model.personality_test.disc import DiscRecordRepository
from sinek.domain.service import (CandidateTestChecklistService,
                                  DISCEvaluationService)

from .common import HunterViewBase
from .facade import (AffiliationServiceFacade, AnchorEvaluationServiceFacade,
                     CandidateTestChecklistServiceFacade,
                     ComplexEvaluationServiceFacade,
                     DiscEvaluationServiceFacade,
                     Tmms24EvaluationServiceFacade)
from .forms import AffiliationForm


class DashboardView(HunterViewBase, TemplateView):
  template_name = 'desktop/hunter/dashboard.html'

  def get_context_data(self, **kwargs):
    candidateTestCheckListServiceFacade = CandidateTestChecklistServiceFacade()
    context = super().get_context_data(**kwargs)

    candidatesChecklists = candidateTestCheckListServiceFacade.ListForAllCandidates()

    context['candidates'] = candidatesChecklists

    return context


class AffiliationView(HunterViewBase, FormView):
  template_name = 'desktop/hunter/new-candidate.html'
  form_class = AffiliationForm
  success_url = reverse_lazy('site:hunter:dashboard')

  def form_valid(self, form: AffiliationForm) -> HttpResponse:
    affiliationServiceFacade = AffiliationServiceFacade()
    affiliationServiceFacade.Affiliate(form)
    return super().form_valid(form)


@AutoWire
class CandidateInformation(HunterViewBase, TemplateView):
  template_name = 'desktop/hunter/candidate-info.html'

  candidateTestChecklistService: CandidateTestChecklistService

  candidateRepository: CandidateRepository

  def get_context_data(self, **kwargs):
    candidateTestCheckListServiceFacade = CandidateTestChecklistServiceFacade()
    context = super().get_context_data(**kwargs)

    email = self.kwargs['email']

    candidateChecklist = candidateTestCheckListServiceFacade.ListForOneCandidate(
      email)

    context['check'] = candidateChecklist

    return context


@Wireable
class CandidateTestResultDisc(HunterViewBase, TemplateView):
  template_name = 'desktop/hunter/test/disc-result.html'

  discEvaluationService: Wired[DISCEvaluationService]
  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  discRecordRepository: Wired[DiscRecordRepository]
  candidateRepository: Wired[CandidateRepository]

  def get(self, request, **kwargs):
    email = kwargs['email']
    discCompleted = self.candidateTestChecklistService.IsDiscCompleted(email)
    if not discCompleted:
      return redirect(
        reverse(
          'site:hunter:candidate-info',
          kwargs={
            'email': email}))
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    email = self.kwargs['email']

    discEvaluationServiceFacade = DiscEvaluationServiceFacade()

    result, candidate = discEvaluationServiceFacade.Evaluate(email)

    context['name'] = candidate.name
    context['result'] = result

    return context


@Wireable
class CandidateTestResultTMMS24(HunterViewBase, TemplateView):
  template_name = 'desktop/hunter/test/tmms24-result.html'

  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  def get(self, request, **kwargs):
    email = kwargs['email']
    tmms24Completed = self.candidateTestChecklistService.IsTmms24Completed(
      email)
    if not tmms24Completed:
      return redirect(
        reverse(
          'site:hunter:candidate-info',
          kwargs={
            'email': email}))
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    email = self.kwargs['email']

    tmms24EvaluationServiceFacade = Tmms24EvaluationServiceFacade()

    result, candidate = tmms24EvaluationServiceFacade.Evaluate(email)

    context['name'] = candidate.name
    context['result'] = result

    return context


@Wireable
class CandidateTestResultAnchor(HunterViewBase, TemplateView):
  template_name = 'desktop/hunter/test/anchor-result.html'

  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  def get(self, request, **kwargs):
    email = kwargs['email']
    anchorCompleted = self.candidateTestChecklistService.IsAnchorCompleted(
      email)
    if not anchorCompleted:
      return redirect(
        reverse(
          'site:hunter:candidate-info',
          kwargs={
            'email': email}))
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    email = self.kwargs['email']

    anchorEvaluationServiceFacade = AnchorEvaluationServiceFacade()
    result, candidate = anchorEvaluationServiceFacade.Evaluate(email)

    context['name'] = candidate.name
    context['result'] = result

    return context


@Wireable
class CandidateTestResultComplex(HunterViewBase, TemplateView):
  template_name = 'desktop/hunter/test/complex-result.html'

  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  def get(self, request, **kwargs):
    email = kwargs['email']
    complexCompleted = self.candidateTestChecklistService.IsComplexCompleted(
      email)
    if not complexCompleted:
      return redirect(
        reverse(
          'site:hunter:candidate-info',
          kwargs={
            'email': email}))
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    email = self.kwargs['email']

    anchorEvaluationServiceFacade = ComplexEvaluationServiceFacade()
    result, candidate = anchorEvaluationServiceFacade.Evaluate(email)

    context['name'] = candidate.name
    context['result'] = result
    return context
