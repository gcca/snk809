from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntEnum, auto
from typing import ForwardRef, List, NamedTuple, Set, Tuple, Type

from neom.ddd.shared import Service, Stuff

from sinek.domain.model.candidate import Candidate, CandidateId
from sinek.domain.model.freelancer import CV, File, Freelancer
from sinek.domain.model.freelancer import Knowledge as FreelancerKnowledge
from sinek.domain.model.personality_test.anchor import (AnchorAnswer,
                                                        AnchorRecord)
from sinek.domain.model.personality_test.complex import (ComplexAnswer,
                                                         ComplexRecord)
from sinek.domain.model.personality_test.disc import DiscAnswer, DiscRecord
from sinek.domain.model.personality_test.tmms24 import (TMMS24Answer,
                                                        TMMS24Record)
from sinek.domain.model.project import Project
from sinek.domain.model.skill import Group, Knowledge, Root
from sinek.domain.model.initiative import Company, Contact


class AffiliationService(Service):

  @abstractmethod
  def Affiliate(self, candidate: Candidate):
    pass


class RecordDISCAnswersService(Service):

  @abstractmethod
  def Record(
    self,
    candidateId: CandidateId,
    answers: List[DiscAnswer]) -> DiscRecord: ...


class DISCEvaluationService(Service):

  class Personality(IntEnum):
    ACOMODADIZO = auto()
    AFILIADOR = auto()
    ANALISTA = auto()
    ASESOR = auto()
    COOPERATIVO = auto()
    CREADOR = auto()
    DIRECTOR = auto()
    EMPRENDEDOR = auto()
    ESPECIALISTA = auto()
    ESTRATEGA = auto()
    INDIVIDUALISTA = auto()
    INVESTIGADOR = auto()
    MOTIVADOR = auto()
    NEGOCIADOR = auto()
    ORGANIZADOR = auto()
    PERFECCIONISTA = auto()
    PERSEVERANTE = auto()
    PERSUASIVO = auto()
    PIONERO = auto()
    TORBELLINO = auto()
    PATRONESUNIFORMES = auto()

  class Result(Stuff):
    personality: DISCEvaluationService.Personality
    compounds: DISCEvaluationService.DiscResult
    pointsUser: DISCEvaluationService.DiscResult
    pointsPersonality: DISCEvaluationService.DiscResult

  class DiscResult(NamedTuple):
    d: int
    i: int
    s: int
    c: int

  @abstractmethod
  def Evaluate(self, discRecord: DiscRecord) -> Result:
    pass


class CandidateTestChecklistService(Service):

  class Check(Stuff):
    candidate: Candidate
    disc_completed: bool
    tmms24_completed: bool
    anchor_completed: bool
    complex_completed: bool

  @abstractmethod
  def ListForOneCandidate(self, candidate: Candidate) -> Check:
    """
    List the Check object only for the candidate given
    """

  @abstractmethod
  def ListForAllCandidates(self) -> List[Check]:
    """
    List the Check objects for a list of candidates given
    """

  @abstractmethod
  def IsDiscCompleted(self, candidateEmail: str) -> bool:
    pass

  @abstractmethod
  def IsTmms24Completed(self, candidateEmail: str) -> bool:
    pass

  @abstractmethod
  def IsAnchorCompleted(self, candidateEmail: str) -> bool:
    pass

  @abstractmethod
  def IsComplexCompleted(self, candidateEmail: str) -> bool:
    pass


class RecordTMMS24AnswersService(Service):

  @abstractmethod
  def Record(self,
             candidateId: CandidateId,
             answers: List[TMMS24Answer]) -> TMMS24Record: ...


class TMMS24EvaluationService(Service):

  class Personality(IntEnum):
    INADECUADO = auto()
    ADECUADO = auto()
    EXCELENTE = auto()

  class Result(Stuff):
    atencion: TMMS24EvaluationService.Personality
    claridad: TMMS24EvaluationService.Personality
    reparacion: TMMS24EvaluationService.Personality

  @abstractmethod
  def Evaluate(self, candidate: Candidate, record: TMMS24Record):
    pass


class RecordAnchorAnswersService(Service):

  @abstractmethod
  def Record(self,
             candidateId: CandidateId,
             answers: List[AnchorAnswer],
             relevants: Tuple[int,
                              int,
                              int]) -> AnchorRecord:
    pass


class AnchorEvaluationService(Service):

  class Personality(IntEnum):
    TF = auto()
    DG = auto()
    AI = auto()
    SE = auto()
    CE = auto()
    SC = auto()
    ED = auto()
    EV = auto()

  class Result(Stuff):
    first: AnchorEvaluationService.Personality
    second: AnchorEvaluationService.Personality
    third: AnchorEvaluationService.Personality
    totals: Tuple[int, int, int, int, int, int, int, int]

  @abstractmethod
  def Evaluate(self, record: AnchorRecord):
    pass


class RecordComplexAnswersService(Service):

  @abstractmethod
  def Record(
      self,
      candidateId: CandidateId,
      answers: List[ComplexAnswer],
      start: datetime,
      finish: datetime) -> ComplexRecord:
    pass


class ComplexEvaluationService(Service):

  class Level(IntEnum):
    ADECUADO = auto()
    REGULAR = auto()
    INFERIOR = auto()

  class Result(Stuff):
    level: ComplexEvaluationService.Level
    points: int
    percentage: int

  @abstractmethod
  def Evaluate(self, record: ComplexRecord):
    pass


class ProjectService(Service):

  @abstractmethod
  def Create(self, project: Project):
    pass

  @abstractmethod
  def ListAll(self) -> List[Project]:
    pass


class ProfileService(Service):

  @abstractmethod
  def GetProfile(self, freelancer: Freelancer) -> Tuple[List[CV], List[File]]:
    pass


class FreelancerKnowledgeTreeService(Service):
  class ScoredKnowledge(Knowledge):
    score: FreelancerKnowledge.Score

  class PremarkedKnowledge(Knowledge):
    pass

  class UnScoredKnowledge(Knowledge):
    pass

  class ScoredGroup(Group):
    pass

  class PremarkedGroup(Group):
    pass

  class GroupBuilder:
    def __init__(self):
      self._buildArgs: List[Type[Group]] = []
      self._groupTypes: Set[Type[Group]] = set()

    def AsScored(self) -> ForwardRef('GroupBuilder'):
      pass

    def AsPremarked(self) -> ForwardRef('GroupBuilder'):
      pass

    def Build(self, key: int, name: str, children: List[Group]) -> Group:
      pass

  @abstractmethod
  def MakeTree(
      self,
      knowledges: List[FreelancerKnowledge],
      root: Root) -> Root:
    pass

  @abstractmethod
  def MakeTreeEdit(
      self,
      knowledges: List[FreelancerKnowledge],
      root: Root) -> Root:
    pass


class FreelancerExperienceService(Service):
  class FreelancerExperience(Stuff):
    freelancer: Freelancer
    knowledges: List[Knowledge]

  class Rank(Stuff):
    freelancer: Freelancer
    businessMatch: Set[str]
    projectMatch: Set[str]
    knowledgeMatch: Set[str]
    compatibility: int

  class Criteria(Stuff):
    businesses: Set[str]
    projects: Set[str]
    knowledges: Set[str]

  @abstractmethod
  def ComputeRanks(
      self,
      freelancerExperiences: List[FreelancerExperience],
      criteria: Criteria) -> List[Rank]:

    pass


class FreelancerCountTreeService(Service):
  class FreelancerShort():
    idFreelancerShort: str
    name: str

    def __init__(self, _id: str, _name: str):
      self.idFreelancerShort = _id
      self.name = _name

  @abstractmethod
  def UpdateCount(
      self,
      countedTree,
      knowledges: List[Knowledge],
      freelancerShort: FreelancerShort,
      levels: List[bool]):
    pass


class FreelancerPeriodService(Service):
  class RatingScales(IntEnum):
    BAD = 0
    NORMAL = 1
    GOOD = 2

  class RatePeriodResult(Stuff):
    cantCurrentAffiliates: int
    cantPreviousAffiliates: int
    rate: str
    scale: FreelancerPeriodService.RatingScales

  class Period(Stuff):

    @abstractmethod
    def GetAffiliates(
        self, visitor: FreelancerPeriodService.PeriodVisitor):
      pass

  class Yearly(Period):

    def GetAffiliates(self, visitor: FreelancerPeriodService.PeriodVisitor):
      return visitor.GetYearAffiliates()

  class Monthly(Period):

    def GetAffiliates(self, visitor: FreelancerPeriodService.PeriodVisitor):
      return visitor.GetMonthAffiliates()

  class Weekly(Period):

    def GetAffiliates(self, visitor: FreelancerPeriodService.PeriodVisitor):
      return visitor.GetWeekAffiliates()

  class Custom(Period):
    start: datetime
    end: datetime

    def __init__(self, start: datetime, end: datetime):
      self.start = start
      self.end = end

    def GetAffiliates(self, visitor: FreelancerPeriodService.PeriodVisitor):
      return visitor.GetCustomPeriodAffiliates(self)

  class PeriodVisitor(ABC):
    @abstractmethod
    def GetYearAffiliates(self):
      pass

    @abstractmethod
    def GetMonthAffiliates(self):
      pass

    @abstractmethod
    def GetWeekAffiliates(self):
      pass

    @abstractmethod
    def GetCustomPeriodAffiliates(self, period):
      pass

  @abstractmethod
  def GetChangeRate(self, period: Period) -> RatePeriodResult:
    pass

  @abstractmethod
  def ListFreelancersByPeriod(self, period: Period):
    pass

  @abstractmethod
  def ListFreelancersByTwoLastPeriod(self, period: Period):
    pass


class InitiativeCreationService(Service):
  class CompanyWorkers(Stuff):
    company: Company
    contacts: List[Contact]

  class CompanyFolderInformation(Stuff):
    company: Company
    contactFolderId: str
    initiativeFolderId: str
    digitalProjectsFolderId: str
    bagHoursFolderId: str

  @abstractmethod
  def ListCompanyWorkers(self) -> List[CompanyWorkers]:
    pass

  @abstractmethod
  def GetCompanyFolderInformation(self) -> CompanyFolderInformation:
    pass


class AutoKnowledgeService(Service):

  @abstractmethod
  def UpdateKnowledgesFromPortfolio(
      self, cvs: List[CV],
      freelancer: Freelancer):
    pass
