from datetime import datetime
from abc import abstractmethod
from enum import IntEnum, unique
from typing import List

from neom.ddd.shared import Entity, Identity, Repository, ValueObject

from sinek.domain.shared import NotFoundError


class Contact(ValueObject):
  name: str


class CompanyCode(ValueObject):
  code: str

  def __str__(self):
    return self.code


class Company(Entity):
  @unique
  class Kind(IntEnum):
    NEW_BUSINESS = 0
    ACCOUNT = 1

  code: Identity[CompanyCode]
  ruc: str
  name: str
  kind: Kind


class InitiativeCode(ValueObject):
  code: str

  def __str__(self):
    return self.code

  # TODO: Cambiar este método
  # luci/infrastructure/persistence/orm/initiative.py:361
  # Esta transformación de `code` o bien es parte del dominio (por lo tanto,
  # debería ser manejado en el la clase CompanyCode, o bien sólo es necesario
  # durante la persistencia (por lo que sólo debería aparecer este código
  # dentro de la implementación del repositorio).
  @staticmethod
  def RemakeMake(
      companyCode: CompanyCode,
      year: str,
      serie: int) -> 'InitiativeCode':
    code = str(companyCode) + '-INI-' + year + str(serie).zfill(3)
    return InitiativeCode(code=code)


class Initiative(Entity):
  @unique
  class WorkKind(IntEnum):
    MAN_POWER = 0
    DIGITAL_PRODUCT = 1
    BAG_HOURS = 2
    RECRUITMENT = 3
    SELECTION = 4
    RS = 5

  @unique
  class State(IntEnum):
    FORTH_COMING = 0
    DISPATCHED = 1
    EARNED = 2
    LOST = 3

  code: Identity[InitiativeCode]
  company: Company
  contact: Contact
  workKind: WorkKind
  name: str
  amount: float
  state: State
  goal: str
  submission: datetime
  successRate: str
  folderId: str

  @property
  def percentage(self):
    return self.successRate + '%'

  @property
  def amountSoles(self):
    thousands_separator = '.'
    fractional_separator = ','

    currency = f'{float(self.amount):.2f}'

    if thousands_separator == '.':
      main_currency, fractional_currency = currency.split(
        '.')[0], currency.split('.')[1]
      new_main_currency = main_currency.replace(',', '.')
      currency = new_main_currency + fractional_separator + fractional_currency

    return 'S/.' + currency


class InitiativeRepository(Repository):

  @abstractmethod
  def Find(self, initiativeCode: InitiativeCode) -> Initiative:
    ...

  @abstractmethod
  def Store(self, initiativeCode: InitiativeCode):
    ...


class InitiativeNotFoundError(NotFoundError):
  pass


class InitiativeQueryService:

  @abstractmethod
  def ListForthComingAndDispatchedInitiatives(self) -> List[Initiative]:
    ...

  @abstractmethod
  def FindCompany(self, companyCode: CompanyCode) -> Company:
    ...

  @abstractmethod
  def FindNextInitiativeCode(
      self, companyCode: CompanyCode) -> InitiativeCode:
    ...

  @abstractmethod
  def ListAllContacts(self) -> List[Contact]:
    ...

  @abstractmethod
  def ListAllAccounts(self) -> List[Company]:
    ...


class ContactNotFoundError(NotFoundError):
  pass


class CompanyNotFoundError(NotFoundError):
  pass
