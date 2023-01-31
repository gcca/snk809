from abc import abstractmethod

from django.contrib.auth.models import User
from neom.ddd.shared import Service

from sinek.domain.model.role import Role


class UserRoleService(Service):

  @abstractmethod
  def ResolveDashboardUrl(self, user: User) -> str:
    ...

  @abstractmethod
  def CreateUser(self, role: Role, password: str):
    ...
