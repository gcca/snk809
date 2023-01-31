from __future__ import annotations

from typing import ForwardRef, overload

from neom.ddd.shared import Entity


class Role(Entity):
  # TODO: All roles must have an email
  # email: Identity[Email]

  @overload
  def Is(self, hunter: ForwardRef('Hunter')) -> bool:
    ...

  @overload
  def Is(self, candidate: ForwardRef('Candidate')) -> bool:
    ...

  @overload
  def Is(self, accountmanager: ForwardRef('AccountManager')) -> bool:
    ...

  @overload
  def Is(self, freelancer: ForwardRef('Freelancer')) -> bool:
    ...

  def Is(self, role: Role) -> bool:
    return isinstance(self, role)

  @staticmethod
  def IsHunter() -> bool:
    return False

  @staticmethod
  def IsCandidate() -> bool:
    return False

  @staticmethod
  def IsAccountManager() -> bool:
    return False

  @staticmethod
  def IsFreelancer() -> bool:
    return False

  @staticmethod
  def IsStaff() -> bool:
    return False
