from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from neom.core.ioc import Wireable, Wired
from neom.ddd.staff import Email

from sinek.domain.model.freelancer import Freelancer, FreelancerRepository
from sinek.interface.controller.account import UserIdRequiredMixin


class OnlyFreelancerMixin(UserIdRequiredMixin):
  permission_required = 'auth.im_freelancer'


@Wireable
class FreelancerViewBase(OnlyFreelancerMixin):
  """This must be used for each freelancer view to enforce permissions, validations
  and common members."""

  freelancerRepository: Wired[FreelancerRepository]

  def setup(self, request: HttpRequest, *args, **kwargs):
    super().setup(request, *args, **kwargs)
    email = self.request.user.email
    freelancer = self.freelancerRepository.Find(Email(email))
    self.freelancer = freelancer

  def dispatch(self, request, *args, **kwargs):
    if 'rc' in request.path:
      return super().dispatch(request, *args, **kwargs)
    if not self.freelancer.isOnboarded and not 'profile-wizard' in request.path:
      return redirect(reverse('site:freelancer:profile-wizard'))
    if self.freelancer.isOnboarded and 'profile-wizard' in request.path:
      return redirect(reverse('site:freelancer:profile'))
    return super().dispatch(request, *args, **kwargs)
