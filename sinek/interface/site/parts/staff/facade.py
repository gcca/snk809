from neom.core.ioc import AutoWire
from neom.ddd.staff import Email

from sinek.application.account import UserRoleService
from sinek.domain.model.accountmanager import (AccountManager,
                                               AccountManagerRepository)
from sinek.domain.model.hunter import Hunter, HunterRepository

from .forms import NewAccountManagerForm, NewHunterForm


@AutoWire
class StaffServiceFacade:

  accountManagerRepository: AccountManagerRepository
  userRoleService: UserRoleService
  hunterRepository: HunterRepository

  def CreateHunter(self, form: NewHunterForm):
    hunterName = form['name'].value()
    # TODO: what is username?
    # username = form['username'].value()
    password = form['password'].value()

    hunter = Hunter(name=hunterName)
    self.hunterRepository.Store(hunter)
    self.userRoleService.CreateUser(hunter, password)

  def CreateAccountManager(self, form: NewAccountManagerForm):
    accountManagerName = form['name'].value()
    email = form['email'].value()
    password = form['password'].value()

    email = Email(email)

    # TODO: missing AccountManagerRepository
    accountManager = AccountManager(name=accountManagerName, email=email)
    self.accountManagerRepository.Store(accountManager)
    self.userRoleService.CreateUser(accountManager, password)
