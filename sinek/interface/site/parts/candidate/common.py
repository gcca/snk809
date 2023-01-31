from django.http import HttpRequest
from neom.core.ioc import Wireable, Wired

from sinek.domain.model.candidate import (Candidate, CandidateId,
                                          CandidateRepository)
from sinek.interface.controller.account import UserIdRequiredMixin


class OnlyCandidateMixin(UserIdRequiredMixin):
  permission_required = 'auth.im_candidate'


@Wireable
class CandidateViewBase(OnlyCandidateMixin):
  """This must be used for each hunter view to enforce permissions, validations
  and common members."""

  candidateRepository: Wired[CandidateRepository]

  def setup(self, request: HttpRequest, *args, **kwargs):
    super().setup(request, *args, **kwargs)
    email = self.request.user.username
    candidate = self.candidateRepository.Find(CandidateId(email))
    self.candidate = candidate

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['candidate'] = self.candidate
    return context
