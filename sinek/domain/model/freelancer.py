from abc import ABC, abstractmethod
from datetime import datetime
from enum import unique
from typing import Any, ForwardRef, List, Set, Tuple, Type

from neom.ddd.shared import (Entity, EntitySupport, Identity, Repository,
                             ValueObject)
from neom.lib.enum import IntEnum
from neom.ddd.staff import Email

from sinek.domain.shared import NotFoundError

from .role import Role

# neompy ------------------------------------------------


class Url(ValueObject):
  value: str

  def __str__(self):
    return self.value

  # TODO: Validate

# end neompy ------------------------------------------------


class Knowledge(Entity, EntitySupport):
  class Score(IntEnum):
    PREMARKED = -1
    BEGINNER = 1
    JUNIOR = 2
    MIDDLE = 3
    SENIOR = 4

  key: Identity[str]
  name: str
  score: Score


class Network(ValueObject):
  @unique
  class Kind(IntEnum):
    GITHUB = 1
    BEHANCE = 2
    LINKEDIN = 3
    OTHER = 4

  url: Url

  def InferKind(self) -> Kind:
    map = {
      'github.com': self.Kind.GITHUB,
      'linkedin.com': self.Kind.LINKEDIN,
      'behance.com': self.Kind.BEHANCE,
    }

    strUrl = str(self.url)
    for key, value in map.items():
      if key in strUrl:
        return value
    return self.Kind.OTHER


class Tag(ValueObject):
  name: str

  def __hash__(self):
    return hash(self.name)


class Condition(ABC):
  ...


class Initial(Condition):
  ...


class Talent(Condition):
  class Disponibility(IntEnum):
    NOSETTLED = 0
    ONEWEEK = 1
    TWOWEEKS = 2
    THREEWEEKS = 3
    ONEMONTH = 4

  class Modality(IntEnum):
    NOSETTLED = 0
    REMOTE = 1
    HYBRID = 2
    OFFICE = 3

  incomeRange: tuple
  disponibility: Disponibility
  modality: Modality
  expectative: str

  def __init__(self, incomeRange, disponibility, modality, expectative):
    self.incomeRange = incomeRange
    self.disponibility = disponibility
    self.modality = modality
    self.expectative = expectative


class Lancer(Condition):
  ...


class FullTime(Lancer):
  ...


class HalfTime(Lancer):
  class Experience(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
  availability: int
  experience: Experience

  def __init__(self, availability: int, experience: Experience):
    self.availability = availability
    self.experience = experience


class ConditionBuilder:
  _buildArgs: List[Type[Condition]]

  def __init__(self):
    self._buildArgs: List[Type[Condition]] = []
    self._conditionTypes: Set[Type[Condition]] = set()

  class BuildArg:
    conditionType: Type[Condition]
    args: Tuple[Any]

    def __init__(self, conditionType: Type[Condition], *args):
      self.conditionType: Type[Condition] = conditionType
      self.args: Tuple[Any] = args

  def AsInitial(self) -> ForwardRef('ConditionBuilder'):
    if self._buildArgs:
      raise TypeError('Condition has a previous status')
    self._buildArgs.append(self.BuildArg(Initial))
    self._conditionTypes.add(Initial)
    return self

  def AsTalent(self, incomeRange, disponibility, modality,
               expectative) -> ForwardRef('ConditionBuilder'):
    self._ValidatePreInitial()
    self._ValidateNoTalent()
    self._buildArgs.append(
      self.BuildArg(
        Talent,
        incomeRange,
        disponibility,
        modality,
        expectative))
    self._conditionTypes.add(Talent)
    return self

  def AsFullTime(self) -> ForwardRef('ConditionBuilder'):
    self._ValidatePreInitial()
    self._ValidateNoHalfTime()
    self._ValidateNoFullTime()
    self._buildArgs.append(self.BuildArg(FullTime))
    self._conditionTypes.add(FullTime)
    return self

  def AsHalfTime(
      self,
      availability: int,
      experience: HalfTime.Experience) -> ForwardRef('ConditionBuilder'):
    self._ValidatePreInitial()
    self._ValidateNoFullTime()
    self._ValidateNoHalfTime()
    self._buildArgs.append(self.BuildArg(HalfTime, availability, experience))
    self._conditionTypes.add(HalfTime)
    return self

  def Build(self) -> Condition:
    if not self._buildArgs:
      raise ValueError('You need to call AsInitial, etc')

    conditionBuilderSelf = self

    class ConcreteCondition(*(c.conditionType for c in self._buildArgs)):
      def __init__(self):
        for c in conditionBuilderSelf._buildArgs:
          c.conditionType.__init__(self, *c.args)

    return ConcreteCondition()

  def _ValidatePreInitial(self):
    if Initial in self._conditionTypes:
      raise TypeError('Condition was setted as Initial')

  def _ValidateNoHalfTime(self):
    if HalfTime in self._conditionTypes:
      raise TypeError('HalfTime was setted')

  def _ValidateNoFullTime(self):
    if FullTime in self._conditionTypes:
      raise TypeError('FullTime was setted')

  def _ValidateNoTalent(self):
    if Talent in self._conditionTypes:
      raise TypeError('Talent was setted')


class Residence(ValueObject):
  country: str
  location: str

  def __str__(self):
    return f'{self.location}, {self.country}'

# ----------------------------------------------


class Phone(ValueObject):

  class CountryCode(IntEnum):
    ARG = 54
    BOL = 591
    BRA = 55
    CHI = 56
    COL = 57
    CRI = 506
    CUB = 53
    ECU = 593
    SLV = 503
    GTM = 502
    HTI = 509
    HND = 504
    MEX = 52
    NIC = 505
    PAN = 507
    PRY = 595
    PER = 51
    URY = 598
    VEN = 58

  countryCode: CountryCode
  number: str

  # TODO: remover este método. Acá sólo se está llamando al constructor
  @staticmethod
  def RemakeMake(countryCode: CountryCode, number: str) -> 'Phone':
    return Phone(
      countryCode=countryCode,
      number=number
    )


class AcceptanceAvailability(ValueObject):
  class JobSwitchTime(IntEnum):
    NOSETTLED = 0
    BW_1M_2M = 1
    BW_3M_6M = 2
    BW_6M_12M = 3
    GT_12M = 4

  wouldChangeCountry: bool
  wouldChangeCity: bool
  interviewAvailability: bool
  jobSwitchTime: JobSwitchTime


class EnglishProficiency(ValueObject):
  class EnglishSkill(IntEnum):
    NOSETTLED = 0
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    PROFICIENT = 4

  writing: EnglishSkill
  speaking: EnglishSkill


class Freelancer(Role):
  email: Identity[Email]
  name: str
  phone: Phone
  condition: Condition
  residence: Residence
  networks: List[Network]
  businesses: Set[Tag]
  projects: Set[Tag]
  acceptanceAvailability: AcceptanceAvailability
  englishProficiency: EnglishProficiency
  roleInterests: Set[Tag]
  jobPreferences: Set[Tag]
  worklifePreferences: Set[Tag]
  isOnboarded: bool

  @staticmethod
  def IsFreelancer():
    return True

  @staticmethod
  def CreateWithoutExperience(email: Email, name: str) -> 'Freelancer':
    return Freelancer(
      email=email,
      name=name,
      phone=Phone(
        Phone.CountryCode.PER,
        ''),
      condition=Initial(),
      residence=Residence(
        country='',
        location=''),
      networks=[],
      businesses=[],
      projects=[],
      jobPreferences=[],
      worklifePreferences=[],
      roleInterests=[],
      acceptanceAvailability=AcceptanceAvailability(
        wouldChangeCountry=False,
        wouldChangeCity=False,
        interviewAvailability=False,
        jobSwitchTime=AcceptanceAvailability.JobSwitchTime.NOSETTLED),
      englishProficiency=EnglishProficiency(
        writing=EnglishProficiency.EnglishSkill.NOSETTLED,
        speaking=EnglishProficiency.EnglishSkill.NOSETTLED),
      isOnboarded=False)


# Freelancer Repository


class FreelancerRepository(Repository):

  @abstractmethod
  def All(self) -> List[Freelancer]:
    ...

  @abstractmethod
  def Find(self, email: str) -> Freelancer:
    ...

  @abstractmethod
  def Store(self, freelancer: Freelancer):
    ...


class FreelancerNotFoundError(NotFoundError):
  ...

# queries --------------------------------------------

# TODO: Big TODO agregar queryset pattern


class FreelancerCommandService:

  @abstractmethod
  def StoreKnowledge(self, freelancer: Freelancer, knowledge: Knowledge):
    ...

  @abstractmethod
  def DropBusiness(self, freelancer: Freelancer, tag: Tag):
    ...

  @abstractmethod
  def DropProject(self, freelancer: Freelancer, tag: Tag):
    ...

  @abstractmethod
  def DropKnowledge(self, freelancer: Freelancer, knowledge: Knowledge):
    ...

  @abstractmethod
  def DropPremarkedKnowledges(self, freelancer: Freelancer,
                              knowledge: Knowledge):
    ...


class FreelancerQueryService:

  # TODO: Circular error import cuando se pone el tipo de dato de retorno
  @abstractmethod
  def FindToComputeCompatibility(
      self,
      name: str,
      pagination: int,
      limit: int = 10) -> List[str]:
    ...

  @abstractmethod
  def ListAllBusinesses(self) -> Set[str]:
    ...

  @abstractmethod
  def ListAllProjects(self) -> Set[str]:
    ...

  @abstractmethod
  def ListKnowledges(self, freelancer: Freelancer) -> List[Knowledge]:
    ...

  @abstractmethod
  def ListKnowledgesNotScored(self, freelancer: Freelancer) -> Set[str]:
    ...

  @abstractmethod
  def CounterFreelancers(self, name: str = '') -> int:
    ...

  @abstractmethod
  def ListFreelancersByPeriod(self, period: 'Period') -> List[Freelancer]:
    ...

  @abstractmethod
  def ListFreelancersByTwoLastPeriod(
      self, period: 'Period') -> Tuple[List[Freelancer], List[Freelancer]]:
    ...

  @abstractmethod
  def ListPagFreelancers(
      self,
      pagination: int,
      limit: int) -> List[Freelancer]:
    ...

  @abstractmethod
  def HasPremarkeds(self, freelancer: Freelancer) -> bool:
    ...


# CV --------------------------------------------

class GoogleId(ValueObject):
  id: str

  def __str__(self):
    return self.id


class CV(Entity):
  googleId: Identity[GoogleId]
  freelancer: Freelancer
  name: str
  created: datetime
  blob: bytes


class CVRepository(Repository):

  @abstractmethod
  def Find(self, freelancer: Freelancer) -> CV:
    ...

  @abstractmethod
  def Store(self, cvValue: CV):
    ...

  @abstractmethod
  def Drop(self, freelancer: Freelancer, fileName: str):
    ...

  # TODO: Temporal. Remover y usar el query set
  @abstractmethod
  def FindBy(self, freelancer: Freelancer) -> List[CV]:
    ...


class CVNotFoundError(NotFoundError):
  ...


# File ------------------------------------------


class File(Entity):
  googleId: Identity[GoogleId]
  freelancer: Freelancer
  name: str
  created: datetime
  blob: bytes


class FileRepository(Repository):

  @abstractmethod
  def Find(self, freelancer: Freelancer, fileName: str) -> File:
    ...

  @abstractmethod
  def Store(self, file: File):
    ...

  # TODO: Temporal. Remover y usar el query set
  @abstractmethod
  def FindBy(self, freelancer: Freelancer) -> List[File]:
    ...

  @abstractmethod
  def Drop(self, freelancer: Freelancer, fileName: str):
    ...


class FileNotFoundError(NotFoundError):
  ...
