from neom.core.ioc import AutoWire

from sinek.domain.model.freelancer import (Email, Freelancer,
                                           FreelancerRepository)
from sinek.infrastructure.account import UserRoleService

from .forms import NewFreelancerForm


@AutoWire
class FreelancerFacade:
  userRoleService: UserRoleService
  freelancerRepository: FreelancerRepository

  def SignUp(self, form: NewFreelancerForm):
    freelancerName = form['name'].value()
    freelancerEmail = form['username'].value()
    freelancerPassword = form['password'].value()

    email = Email(freelancerEmail)

    freelancer = Freelancer.CreateWithoutExperience(email, freelancerName)

    self.freelancerRepository.Store(freelancer)
    self.userRoleService.CreateUser(freelancer, freelancerPassword)
