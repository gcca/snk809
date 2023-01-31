from abc import abstractmethod

from neom.ddd.shared import Identity, Repository
from neom.ddd.staff import Email

from sinek.domain.shared import NotFoundError

from .role import Role

# Account Manager entity


class AccountManager(Role):  # TODO: AccountManager(Employee)
  email: Identity[Email]
  name: str

  @staticmethod
  def IsAccountManager():
    return True


# AccountManager Repository

class AccountManagerRepository(Repository):

  @abstractmethod
  def Store(self, accountManager: AccountManager):
    """ TODO: Raises: Repository.PersistenceError."""


class AccountManagerNotFoundError(NotFoundError):
  pass
