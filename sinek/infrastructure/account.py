from typing import Type, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, User
from django.db.models import Model
from django.urls import reverse
from neom.ddd.shared import Entity

from sinek.application.account import UserRoleService
from sinek.domain.model.accountmanager import AccountManager
from sinek.domain.model.candidate import Candidate
from sinek.domain.model.freelancer import Freelancer
from sinek.domain.model.hunter import Hunter
from sinek.domain.model.role import Role
from sinek.domain.model.staff import Staff
from sinek.infrastructure.persistence.orm.models import \
  AccountManager as ORMAccountManager
from sinek.infrastructure.persistence.orm.models import \
  Candidate as ORMCandidate
from sinek.infrastructure.persistence.orm.models import \
  Freelancer as ORMFreelancer
from sinek.infrastructure.persistence.orm.models import Hunter as ORMHunter
from sinek.infrastructure.persistence.orm.models import Role as ORMRole
from sinek.infrastructure.persistence.orm.models import Staff as ORMStaff


class UserRoleServiceImpl(UserRoleService):

  def ResolveDashboardUrl(self, user: User) -> str:
    try:
      role = ORMRole.objects.get(user=user)
    except ORMRole.DoesNotExist:
      return reverse('site:account:reset-session')

    if role.hunter:
      return reverse('site:hunter:dashboard')
    if role.candidate:
      return reverse('site:candidate:dashboard')
    if role.accountManager:
      return reverse('site:accountmanager:freelancer-list')
    if role.freelancer:
      return reverse('site:freelancer:profile')
    if role.staff:
      return reverse('site:staff:dashboard')

    raise RuntimeError('Bad role record')

  def CreateUser(self, role: Role, password: str):
    # TODO: improve user creation using the future @identity in neompy
    if role.IsHunter():
      return UpdateOrCreate(
        password,
        role,
        Hunter,
        ORMHunter,
        'im_hunter',
        'name',
        'hunter')

    if role.IsCandidate():
      return UpdateOrCreate(
        password,
        role,
        Candidate,
        ORMCandidate,
        'im_candidate',
        'email',
        'candidate')

    if role.IsAccountManager():
      return UpdateOrCreate(
        password,
        role,
        AccountManager,
        ORMAccountManager,
        'im_accountmanager',
        'email',
        'accountManager')

    if role.IsFreelancer():
      return UpdateOrCreate(
        password,
        role,
        Freelancer,
        ORMFreelancer,
        'im_freelancer',
        'email',
        'freelancer')

    if role.IsStaff():
      return UpdateOrCreate(
        password,
        role,
        Staff,
        ORMStaff,
        'im_staff',
        'name',
        'staff')

    raise RuntimeError(f'Fatal role: {role}')


def UpdateOrCreate(
    password: str,
    role: Entity,
    entityClass: Type[Entity],
    ORMModel: Type[Model],
    permission: str,
    name: str,
    owner: str):
  entity = cast(entityClass, role)
  try:
    value = str(getattr(entity, name))
    ormModel = ORMModel.objects.get(**{name: value})
  except ORMModel.DoesNotExist:
    raise ValueError(f'Not stored role: {role}')
  _CreateUser(value, password, permission, **{owner: ormModel})


def _CreateUser(username: str, password: str, codename: str, **kwargs):
  userModel = get_user_model()
  user = userModel.objects.create_user(username, username, password)
  permission = Permission.objects.get(codename=codename)
  user.user_permissions.add(permission)
  ORMRole.objects.create(user=user, **kwargs)
