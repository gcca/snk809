from datetime import datetime
from typing import ForwardRef, List, Set, Tuple, Type
from uuid import uuid1

from fuzzywuzzy import fuzz
from neom.core.ioc import AutoWire
from neom.ddd.shared import Entity, Identity, Repository
from PyPDF2 import PdfFileReader

from sinek.application.service import GoogleDriveService
from sinek.domain.model.candidate import (Candidate, CandidateId,
                                          CandidateRepository)
from sinek.domain.model.freelancer import (CV, CVNotFoundError, CVRepository,
                                           File, FileRepository, Freelancer,
                                           FreelancerCommandService,
                                           FreelancerQueryService,
                                           FreelancerRepository)
from sinek.domain.model.freelancer import Knowledge as FreelancerKnowledge
from sinek.domain.model.initiative import CompanyCode, InitiativeQueryService
from sinek.domain.model.personality_test.anchor import (AnchorAnswer,
                                                        AnchorRecord,
                                                        AnchorRecordRepository)
from sinek.domain.model.personality_test.complex import (
  ComplexAnswer, ComplexRecord, ComplexRecordRepository)
from sinek.domain.model.personality_test.disc import (DiscAnswer, DiscRecord,
                                                      DiscRecordRepository)
from sinek.domain.model.personality_test.tmms24 import (TMMS24Answer,
                                                        TMMS24Record,
                                                        TMMS24RecordRepository)
from sinek.domain.model.project import Project, ProjectRepository
from sinek.domain.model.skill import (Group, Knowledge, Root, Skill,
                                      SkillQueryService)
from sinek.domain.shared import NotFoundError, ServiceError
from sinek.interface.site import imgs
from sinek.interface.site.parts.accountmanager.adapter import (
  CountedGroupViewAdapter, CountedKnowledgeViewAdapter)
from sinek.interface.site.parts.common.adapter import SkillTreeViewAdapter
from sinek.interface.site import imgs

from .service import (AffiliationService, AnchorEvaluationService,
                      AutoKnowledgeService, CandidateTestChecklistService,
                      ComplexEvaluationService, DISCEvaluationService,
                      FreelancerCountTreeService, FreelancerExperienceService,
                      FreelancerKnowledgeTreeService, FreelancerPeriodService,
                      InitiativeCreationService, ProfileService,
                      ProjectService, RecordAnchorAnswersService,
                      RecordComplexAnswersService, RecordDISCAnswersService,
                      RecordTMMS24AnswersService, TMMS24EvaluationService)


@AutoWire
class AffiliationServiceImpl(AffiliationService):

  candidateRepository: CandidateRepository

  def Affiliate(self, candidate: Candidate):
    self.candidateRepository.Store(candidate)


@AutoWire
class RecordDISCAnswersServiceImpl(RecordDISCAnswersService):

  recordRepository: DiscRecordRepository

  def Record(self, candidateId: CandidateId,
             answers: List[DiscAnswer]) -> DiscRecord:
    RecordServiceBase.Record(
      candidateId,
      DiscRecord,
      self.recordRepository,
      candidateId=candidateId,
      answers=answers)


class DISCEvaluationServiceImpl(DISCEvaluationService):

  Result = DISCEvaluationService.Result

  def Evaluate(self, discRecord: DiscRecord) -> Result:
    compounds = self._GetCompounds(discRecord.answers)
    baremos = self._GetBaremos(compounds)
    (personality, points) = self._GetPersonality(baremos)
    result = DISCEvaluationService.Result(
      compounds=compounds,
      personality=personality,
      pointsPersonality=points,
      pointsUser=baremos)
    return result

  def _GetCompounds(
      self,
      answers: List[DiscAnswer]) -> DISCEvaluationService.DiscResult:
    countPlus = 0
    countMinus = 0

    for answer in answers:
      countPlus += pow(100, int(answer.plus) - 1)
      countMinus += pow(100, int(answer.minus) - 1)

    (d, countPlus, countMinus) = self._DiscompundValuesDisc(
      countPlus, countMinus)
    (i, countPlus, countMinus) = self._DiscompundValuesDisc(
      countPlus, countMinus)
    (s, countPlus, countMinus) = self._DiscompundValuesDisc(
      countPlus, countMinus)
    (c, countPlus, countMinus) = self._DiscompundValuesDisc(
      countPlus, countMinus)
    return DISCEvaluationService.DiscResult(d=d, i=i, s=s, c=c)

  def _DiscompundValuesDisc(self, countPlus: int, countMinus: int):
    discompoundValue = countPlus % 100 - countMinus % 100
    countPlus = countPlus // 100
    countMinus = countMinus // 100
    return (discompoundValue, countPlus, countMinus)

  def _GetBaremos(
      self,
      compounds: DISCEvaluationService.DiscResult) \
      -> DISCEvaluationService.DiscResult:
    baremoTable = self.BaremoTables()
    try:
      d = baremoTable.dicionaryD[str(compounds.d)]
      i = baremoTable.dicionaryI[str(compounds.i)]
      s = baremoTable.dicionaryS[str(compounds.s)]
      c = baremoTable.dicionaryC[str(compounds.c)]
    except KeyError:
      d, i, s, c = 60, 50, 60, 60
    return DISCEvaluationService.DiscResult(d=d, i=i, s=s, c=c)

  def _GetPersonality(self, tupleUser: DISCEvaluationService.DiscResult):
    personalities = self.Personalities()
    minTuple = personalities.personalityTuple[0]
    minComparation = self._CompareTuples(tupleUser, minTuple)

    for t in personalities.personalityTuple[1:]:
      r = self._CompareTuples(tupleUser, t)
      # TODO: Asegurar que no exista valores iguales
      if r < minComparation:
        minTuple = t

    return (personalities.personalityMap[minTuple], minTuple)

  def _CompareTuples(
      self,
      tupleUser: DISCEvaluationService.DiscResult,
      tupleList: DISCEvaluationService.DiscResult):
    return sum((x - y)**2 for x, y in zip(tupleUser, tupleList)) / 4

  class BaremoTables():
    dicionaryD = {
      '-16': 10,
      '-15': 16,
      '-14': 20,
      '-13': 20,
      '-12': 30,
      '-11': 30,
      '-10': 30,
      '-9': 40,
      '-8': 40,
      '-7': 50,
      '-6': 50,
      '-5': 60,
      '-4': 60,
      '-3': 60,
      '-2': 60,
      '-1': 70,
      '0': 70,
      '1': 80,
      '2': 80,
      '3': 84,
      '4': 90,
      '5': 95,
      '6': 95,
      '7': 95,
      '8': 95,
      '9': 95,
      '10': 95,
      '11': 99,
      '12': 99,
      '13': 99,
      '14': 99,
      '15': 99,
    }

    dicionaryI = {
      '-16': 1,
      '-15': 1,
      '-14': 1,
      '-13': 5,
      '-12': 5,
      '-11': 10,
      '-10': 10,
      '-9': 10,
      '-8': 16,
      '-7': 20,
      '-6': 30,
      '-5': 30,
      '-4': 40,
      '-3': 50,
      '-2': 50,
      '-1': 60,
      '0': 60,
      '1': 60,
      '2': 70,
      '3': 70,
      '4': 70,
      '5': 70,
      '6': 80,
      '7': 90,
      '8': 90,
      '9': 95,
      '10': 95,
      '11': 99,
      '12': 99,
      '13': 99,
      '14': 99,
      '15': 99,
      '16': 99,
      '17': 99,
      '18': 99,
    }

    dicionaryS = {
      '-13': 1,
      '-12': 1,
      '-11': 1,
      '-10': 5,
      '-9': 10,
      '-8': 10,
      '-7': 10,
      '-6': 16,
      '-5': 20,
      '-4': 20,
      '-3': 20,
      '-2': 30,
      '-1': 30,
      '0': 40,
      '1': 40,
      '2': 50,
      '3': 50,
      '4': 50,
      '5': 60,
      '6': 60,
      '7': 60,
      '8': 60,
      '9': 70,
      '10': 70,
      '11': 70,
      '12': 80,
      '13': 90,
      '14': 95,
      '15': 95,
      '16': 99,
      '17': 99,
    }

    dicionaryC = {
      '-15': 1,
      '-14': 1,
      '-13': 5,
      '-12': 5,
      '-11': 10,
      '-10': 10,
      '-9': 10,
      '-8': 16,
      '-7': 20,
      '-6': 20,
      '-5': 30,
      '-4': 30,
      '-3': 40,
      '-2': 30,
      '-1': 40,
      '0': 50,
      '1': 53,
      '2': 60,
      '3': 70,
      '4': 70,
      '5': 80,
      '6': 84,
      '7': 90,
      '8': 90,
      '9': 95,
      '10': 95,
      '11': 99,
      '12': 99,
      '13': 99,
    }

  class Personalities():
    personalityTuple = (
      DISCEvaluationService.DiscResult(d=95, i=30, s=30, c=30),
      DISCEvaluationService.DiscResult(d=95, i=70, s=30, c=10),
      DISCEvaluationService.DiscResult(d=90, i=80, s=10, c=30),
      DISCEvaluationService.DiscResult(d=90, i=30, s=16, c=70),
      DISCEvaluationService.DiscResult(d=10, i=70, s=80, c=70),
      DISCEvaluationService.DiscResult(d=40, i=95, s=30, c=30),
      DISCEvaluationService.DiscResult(d=20, i=90, s=20, c=90),
      DISCEvaluationService.DiscResult(d=84, i=95, s=16, c=20),
      DISCEvaluationService.DiscResult(d=70, i=95, s=30, c=20),
      DISCEvaluationService.DiscResult(d=70, i=5, s=80, c=60),
      DISCEvaluationService.DiscResult(d=30, i=30, s=95, c=30),
      DISCEvaluationService.DiscResult(d=84, i=20, s=84, c=20),
      DISCEvaluationService.DiscResult(d=10, i=30, s=90, c=84),
      DISCEvaluationService.DiscResult(d=20, i=90, s=90, c=16),
      DISCEvaluationService.DiscResult(d=70, i=70, s=5, c=70),
      DISCEvaluationService.DiscResult(d=40, i=30, s=40, c=95),
      DISCEvaluationService.DiscResult(d=30, i=16, s=84, c=90),
      DISCEvaluationService.DiscResult(d=5, i=40, s=80, c=95),
      DISCEvaluationService.DiscResult(d=80, i=30, s=30, c=80),
      DISCEvaluationService.DiscResult(d=70, i=80, s=70, c=5),
      DISCEvaluationService.DiscResult(d=60, i=50, s=60, c=60)
    )

    Personality = DISCEvaluationService.Personality
    personalityName = (
      Personality.DIRECTOR,
      Personality.EMPRENDEDOR,
      Personality.ORGANIZADOR,
      Personality.PIONERO,
      Personality.COOPERATIVO,
      Personality.AFILIADOR,
      Personality.NEGOCIADOR,
      Personality.MOTIVADOR,
      Personality.PERSUASIVO,
      Personality.ESTRATEGA,
      Personality.PERSEVERANTE,
      Personality.INVESTIGADOR,
      Personality.ESPECIALISTA,
      Personality.ASESOR,
      Personality.TORBELLINO,
      Personality.PERFECCIONISTA,
      Personality.ANALISTA,
      Personality.ACOMODADIZO,
      Personality.CREADOR,
      Personality.INDIVIDUALISTA,
      Personality.PATRONESUNIFORMES
    )

    personalityMap = {}
    for i in range(21):
      personalityMap[personalityTuple[i]] = personalityName[i]


@AutoWire
class CandidateTestChecklistServiceImpl(CandidateTestChecklistService):

  Check = CandidateTestChecklistService.Check

  anchorRecordRepository: AnchorRecordRepository
  candidateRepository: CandidateRepository
  complexRecordRepository: ComplexRecordRepository
  discRecordRepository: DiscRecordRepository
  tmms24RecordRepository: TMMS24RecordRepository

  def ListForOneCandidate(self, candidateId: CandidateId) -> Check:
    candidate = self.candidateRepository.Find(candidateId)
    return self._MakeCheck(candidate)

  def ListForAllCandidates(self) -> List[Check]:
    candidates = self.candidateRepository.All()
    checkList = [self._MakeCheck(candidate) for candidate in candidates]
    return checkList

  def IsDiscCompleted(self, candidateEmail: str) -> bool:
    candidateId = CandidateId(candidateEmail)
    return self.IsCompleted(candidateId, self.discRecordRepository)

  def IsTmms24Completed(self, candidateEmail: str) -> bool:
    candidateId = CandidateId(candidateEmail)
    return self.IsCompleted(candidateId, self.tmms24RecordRepository)

  def IsAnchorCompleted(self, candidateEmail: str) -> bool:
    candidateId = CandidateId(candidateEmail)
    try:
      anchorRecord = self.anchorRecordRepository.Find(candidateId)
    except BaseException:
      anchorRecord = None
    return bool(anchorRecord)

  def IsComplexCompleted(self, candidateEmail: str) -> bool:
    candidateId = CandidateId(candidateEmail)
    return self.IsCompleted(candidateId, self.complexRecordRepository)

  def _MakeCheck(self, candidate: Candidate) -> Check:
    candidateId = CandidateId(candidate.email)

    check = self.Check(
      candidate=candidate,
      disc_completed=self.IsCompleted(
        candidateId, self.discRecordRepository),
      tmms24_completed=self.IsCompleted(
        candidate, self.tmms24RecordRepository),  # TODO: BIG ERROR
      anchor_completed=self.IsCompleted(
        candidateId, self.anchorRecordRepository),
      complex_completed=self.IsCompleted(candidateId,
                                         self.complexRecordRepository))

    return check

  @staticmethod
  def IsCompleted(candidateId: CandidateId, repository: Repository) -> bool:
    try:
      repository.Find(candidateId)
      return True
    except NotFoundError:
      return False


@AutoWire
class RecordTMMS24AnswersServiceImpl(RecordTMMS24AnswersService):

  recordRepository: TMMS24RecordRepository

  def Record(
      self,
      candidateId: CandidateId,
      answers: List[TMMS24Answer]) -> TMMS24Record:
    RecordServiceBase.Record(
      candidateId,
      TMMS24Record,
      self.recordRepository,
      candidateId=candidateId,
      answers=answers)


class TMMS24EvaluationServiceImpl(TMMS24EvaluationService):
  Result = TMMS24EvaluationService.Result
  Personality = TMMS24EvaluationService.Personality

  def Evaluate(
      self,
      candidate: Candidate,
      tmms24Record: TMMS24Record) -> Result:
    totals = self._GetTotals(tmms24Record.answers)
    results = self._GetResults(candidate.gender, totals)
    return results

  def _GetTotals(self, answers: List[TMMS24Answer]):
    atencion = sum(int(answer.score) for answer in answers[0:8])
    claridad = sum(int(answer.score) for answer in answers[8:16])
    reparacion = sum(int(answer.score) for answer in answers[16:24])

    return (atencion, claridad, reparacion)

  def _GetResults(self, gender: Candidate.Gender,
                  totals: Tuple[int, int, int]) -> Result:
    if gender.IsMale():
      if totals[0] < 22:
        atencion = self.Personality.INADECUADO
      elif totals[0] < 33:
        atencion = self.Personality.ADECUADO
      else:
        atencion = self.Personality.EXCELENTE

      if totals[1] < 26:
        claridad = self.Personality.INADECUADO
      elif totals[1] < 36:
        claridad = self.Personality.ADECUADO
      else:
        claridad = self.Personality.EXCELENTE

      if totals[2] < 24:
        reparacion = self.Personality.INADECUADO
      elif totals[2] < 36:
        reparacion = self.Personality.ADECUADO
      else:
        reparacion = self.Personality.EXCELENTE

    else:
      if totals[0] < 25:
        atencion = self.Personality.INADECUADO
      elif totals[0] < 36:
        atencion = self.Personality.ADECUADO
      else:
        atencion = self.Personality.EXCELENTE

      if totals[1] < 24:
        claridad = self.Personality.INADECUADO
      elif totals[1] < 35:
        claridad = self.Personality.ADECUADO
      else:
        claridad = self.Personality.EXCELENTE

      if totals[2] < 24:
        reparacion = self.Personality.INADECUADO
      elif totals[2] < 35:
        reparacion = self.Personality.ADECUADO
      else:
        reparacion = self.Personality.EXCELENTE

    return self.Result(
      atencion=atencion,
      claridad=claridad,
      reparacion=reparacion)


@AutoWire
class RecordAnchorAnswersServiceImpl(RecordAnchorAnswersService):

  recordRepository: AnchorRecordRepository

  def Record(self,
             candidateId: CandidateId,
             answers: List[AnchorAnswer],
             relevants: Tuple[int,
                              int,
                              int]) -> AnchorRecord:
    RecordServiceBase.Record(
      candidateId,
      AnchorRecord,
      self.recordRepository,
      candidateId=candidateId,
      answers=answers,
      relevants=relevants)


@AutoWire
class AnchorEvaluationServiceImpl(AnchorEvaluationService):
  Result = AnchorEvaluationService.Result

  def Evaluate(self, record: AnchorRecord) -> Result:
    totals = self._GetTotals(record.answers)
    totals = self._AddFavourites(totals, record.relevants)
    result = self._GetResults(totals)
    return result

  def _GetTotals(self, answers: List[AnchorAnswer]):
    totals = [0] * 8
    for answer in answers:
      totals[(answer.number - 1) % 8] += int(answer.score)
    return totals

  def _AddFavourites(self, totals: Tuple, favourites: Tuple[int, int, int]):
    totals[(favourites[0] - 1) % 8] += 4
    totals[(favourites[1] - 1) % 8] += 4
    totals[(favourites[2] - 1) % 8] += 4
    return totals

  def _GetResults(self, totals: List[int]):
    totalTuples = [(enum + 1, value) for enum, value in enumerate(totals)]
    ordenados = sorted(
      totalTuples,
      key=lambda value: value[1],
      reverse=True)
    first = self.Personalities.personalityMap[ordenados[0][0]]
    second = self.Personalities.personalityMap[ordenados[1][0]]
    third = self.Personalities.personalityMap[ordenados[2][0]]

    results = AnchorEvaluationService.Result(
      first=first, second=second, third=third, totals=totals)
    return results

  class Personalities:
    Personality = AnchorEvaluationService.Personality
    personalityMap = {
      1: Personality.TF,
      2: Personality.DG,
      3: Personality.AI,
      4: Personality.SE,
      5: Personality.CE,
      6: Personality.SC,
      7: Personality.ED,
      8: Personality.EV,
    }


class RecordServiceBase:

  class AlreadyRecordedError(ServiceError):
    def __init__(self, identity: Identity):
      self.identity = identity

  @staticmethod
  def Record(
      identity: Identity,
      entityClass: Type[Entity],
      repository: Repository,
      **kwargs) -> Entity:
    try:
      repository.Find(identity)
      raise RecordServiceBase.AlreadyRecordedError(identity)
    except NotFoundError:
      record = entityClass(**kwargs)
      return repository.Store(record)


@AutoWire
class RecordComplexAnswersServiceImpl(RecordComplexAnswersService):

  recordRepository: ComplexRecordRepository

  def Record(
      self,
      candidateId: CandidateId,
      answers: List[ComplexAnswer],
      start: datetime,
      finish: datetime) -> ComplexRecord:
    RecordServiceBase.Record(
      candidateId,
      ComplexRecord,
      self.recordRepository,
      candidateId=candidateId,
      answers=answers,
      start=start,
      finish=finish)


@AutoWire
class ComplexEvaluationServiceImpl(ComplexEvaluationService):
  Result = ComplexEvaluationService.Result

  def Evaluate(self, record: ComplexRecord) -> Result:
    totalPoints = self._GetTotalPoints(record.answers)
    percentage = self._GetPercentage(totalPoints)
    level = self._GetLevel(totalPoints)
    return ComplexEvaluationService.Result(
      level=level, percentage=percentage, points=totalPoints)

  def _GetTotalPoints(self, answers: List[ComplexAnswer]):
    total = 0
    for answer in answers:
      if answer.combination != self.BaremoTable.combinations.get(
          answer.number):
        total += 1
    return total

  def _GetPercentage(self, totalPoints: int):
    return self.BaremoTable.percentages.get(totalPoints)

  def _GetLevel(self, totalPoints: int):
    if totalPoints < 10:
      level = ComplexEvaluationService.Level.ADECUADO
    elif totalPoints < 15:
      level = ComplexEvaluationService.Level.REGULAR
    else:
      level = ComplexEvaluationService.Level.INFERIOR
    return level

  class BaremoTable:
    combinations = {
      1: (True, False, True),
      2: (False, True, False),
      3: (True, False, False),
      4: (False, False, False),
      5: (False, False, True),
      6: (True, False, False),
      7: (False, False, True),
      8: (False, False, False),
      9: (False, False, False),
      10: (True, False, False),
      11: (False, False, True),
      12: (False, False, False),
      13: (False, True, False),
      14: (False, False, False),
      15: (False, False, True),
      16: (False, False, False),
      17: (False, False, False),
      18: (False, False, False),
      19: (True, False, True),
      20: (True, True, False),
      21: (False, False, True),
      22: (False, False, True),
      23: (True, False, False),
      24: (False, False, False),
      25: (True, True, False),
    }

    percentages = {
      0: 100,
      1: 96,
      2: 93,
      3: 89,
      4: 86,
      5: 82,
      6: 79,
      7: 75,
      8: 71,
      9: 68,
      10: 64,
      11: 61,
      12: 57,
      13: 54,
      14: 50,
      15: 46,
      16: 43,
      17: 39,
      18: 36,
      19: 32,
      20: 29,
      21: 25,
      22: 21,
      23: 18,
      24: 14,
      25: 11,
      26: 7,
      27: 4,
      28: 0,
    }


@AutoWire
class ProjectServiceImpl(ProjectService):

  projectRepository: ProjectRepository

  def Create(self, project: Project):
    self.projectRepository.Store(project)

  def ListAll(self) -> List[Project]:
    return self.projectRepository.All()


@AutoWire
class ProfileServiceImpl(ProfileService):

  freelancerRepository: FreelancerRepository
  cvRepository: CVRepository
  fileRepository: FileRepository
  freelancerQueryService: FreelancerQueryService

  def GetProfile(
      self, freelancer: Freelancer) -> Tuple[List[CV], List[File]]:

    try:
      cvs = self.cvRepository.FindBy(freelancer)
    except CVNotFoundError:
      cvs = None

    files = self.fileRepository.FindBy(freelancer)

    return (cvs, files)


@AutoWire
class FreelancerKnowledgeTreeServiceImpl(FreelancerKnowledgeTreeService):

  skillQueryService: SkillQueryService
  freelancerQueryService: FreelancerQueryService
  freelancerRepository: FreelancerRepository

  ScoredKnowledge = FreelancerKnowledgeTreeService.ScoredKnowledge
  PremarkedKnowledge = FreelancerKnowledgeTreeService.PremarkedKnowledge
  ScoredGroup = FreelancerKnowledgeTreeService.ScoredGroup
  PremarkedGroup = FreelancerKnowledgeTreeService.PremarkedGroup

  class GroupBuilder(FreelancerKnowledgeTreeService.GroupBuilder):
    # TODO: Make some tests
    def AsScored(self) -> ForwardRef('GroupBuilder'):
      self._buildArgs.append(FreelancerKnowledgeTreeService.ScoredGroup)

    def AsPremarked(self) -> ForwardRef('GroupBuilder'):
      self._buildArgs.append(
        FreelancerKnowledgeTreeService.PremarkedGroup)

    def Build(self, key: int, name: str, children: List[Group]) -> Group:
      class ConcreteGroup(*(c for c in self._buildArgs)):
        ...
      return ConcreteGroup(key=key, name=name, children=children)

  def MakeTree(
      self,
      knowledges: List[FreelancerKnowledge],
      root: Root) -> Root:
    tree = Root(key=uuid1().hex, name='knowledgeTree', children=[])
    for child in root.children:
      newChild = self._makeNode(child, knowledges)
      if isinstance(
          newChild,
          self.ScoredGroup) or isinstance(
          newChild,
          self.PremarkedGroup):
        tree.children.append(newChild)
    return tree

  def MakeTreeEdit(
      self,
      knowledges: List[FreelancerKnowledge],
      root: Root) -> Root:
    tree = Root(key=uuid1().hex, name='knowledgeTree', children=[])
    for child in root.children:
      newChild = self._makeNodeEdit(child, knowledges)
      tree.children.append(newChild)
    return tree

  def _makeNode(self, node: Skill,
                knowledges: List[FreelancerKnowledge]) -> Skill:
    if isinstance(node, Knowledge):
      indexKnowledge = self._findKnowledgeIndex(node.key, knowledges)
      if indexKnowledge >= 0:
        knowledge = knowledges.pop(indexKnowledge)
        if knowledge.score == FreelancerKnowledge.Score.PREMARKED:
          newSkill = self.PremarkedKnowledge(
            key=knowledge.key, name=knowledge.name)
        else:
          newSkill = self.ScoredKnowledge(
            key=knowledge.key, name=knowledge.name, score=knowledge.score)
      else:
        newSkill = None
      return newSkill

    childrenList = []
    hasScoredChild = False
    hasPremarkedChild = False
    for child in node.children:
      newChild = self._makeNode(child, knowledges)

      if isinstance(
          newChild,
          self.ScoredKnowledge) or isinstance(
          newChild,
          self.ScoredGroup):
        hasScoredChild = True
      if isinstance(
          newChild,
          self.PremarkedKnowledge) or isinstance(
          newChild,
          self.PremarkedGroup):
        hasPremarkedChild = True

      if (hasScoredChild or hasPremarkedChild) and newChild and not isinstance(
          newChild, Group):
        childrenList.append(newChild)

    if not hasScoredChild and not hasPremarkedChild:
      return Group(key=node.key, name=node.name, children=childrenList)

    groupBuilder = self.GroupBuilder()

    if hasScoredChild:
      groupBuilder.AsScored()
    if hasPremarkedChild:
      groupBuilder.AsPremarked()

    return groupBuilder.Build(
      key=node.key,
      name=node.name,
      children=childrenList)

  def _findKnowledgeIndex(
      self,
      key: str,
      knowledges: List[FreelancerKnowledge]) -> int:
    for index, knowledge in enumerate(knowledges):
      if knowledge.key == key:
        return index
    return -1

  def _makeNodeEdit(self, node: Skill,
                    knowledges: List[FreelancerKnowledge]) \
      -> Tuple[Skill, bool]:
    if isinstance(node, Knowledge):
      indexKnowledge = self._findKnowledgeIndex(node.key, knowledges)
      if indexKnowledge >= 0:
        knowledge = knowledges.pop(indexKnowledge)
        if knowledge.score == FreelancerKnowledge.Score.PREMARKED:
          newSkill = self.PremarkedKnowledge(
            key=knowledge.key, name=knowledge.name)
        else:
          newSkill = self.ScoredKnowledge(
            key=knowledge.key, name=knowledge.name, score=knowledge.score)
      else:
        newSkill = self.UnScoredKnowledge(key=node.key, name=node.name)
      return newSkill

    childrenList = []
    hasScoredChild = False
    hasPremarkedChild = False

    for child in node.children:
      newChild = self._makeNodeEdit(child, knowledges)
      childrenList.append(newChild)

      if (isinstance(
          newChild,
          self.ScoredKnowledge)) or isinstance(
          newChild,
          self.ScoredGroup):
        hasScoredChild = True
      if (
        isinstance(
          newChild,
          self.PremarkedKnowledge) or isinstance(
          newChild,
          self.PremarkedGroup)):
        hasPremarkedChild = True

    if not hasScoredChild and not hasPremarkedChild:
      return Group(key=node.key, name=node.name, children=childrenList)

    groupBuilder = self.GroupBuilder()

    if hasScoredChild:
      groupBuilder.AsScored()
    if hasPremarkedChild:
      groupBuilder.AsPremarked()

    return groupBuilder.Build(
      key=node.key,
      name=node.name,
      children=childrenList)


class FreelancerExperienceServiceImpl(FreelancerExperienceService):

  FreelancerExperience = FreelancerExperienceService.FreelancerExperience
  Rank = FreelancerExperienceService.Rank
  Criteria = FreelancerExperienceService.Criteria

  def ComputeRanks(
      self,
      freelancerExperiences: List[FreelancerExperience],
      criteria: Criteria) -> List[Rank]:
    ranks = [self._Rank(freelancerExperience, criteria)
             for freelancerExperience in freelancerExperiences]
    ranks.sort(key=lambda rank: rank.compatibility, reverse=True)
    return ranks

  def _Rank(
      self,
      freelancerExperience: FreelancerExperience,
      criteria: Criteria) -> Rank:
    businesses = set(
      tag.name for tag in freelancerExperience.freelancer.businesses)
    projects = set(
      tag.name for tag in freelancerExperience.freelancer.projects)
    knowledges = set(tag.name for tag in freelancerExperience.knowledges)

    businessMatch = businesses & criteria.businesses
    projectMatch = projects & criteria.projects
    knowledgeMatch = knowledges & criteria.knowledges

    compatibility = len(businessMatch) + \
      len(projectMatch) + len(knowledgeMatch)

    return self.Rank(freelancer=freelancerExperience.freelancer,
                     businessMatch=businessMatch,
                     projectMatch=projectMatch,
                     knowledgeMatch=knowledgeMatch,
                     compatibility=compatibility)


class FreelancerCountTreeServiceImpl(FreelancerCountTreeService):

  # Esto no debería ser así. Los ViewAdapter's son parte de la interfaz.
  # No tiene que ser usado en el dominio.
  def UpdateCount(
      self,
      countedTree: CountedGroupViewAdapter,
      knowledges: List[Knowledge],
      freelancerShort: FreelancerCountTreeService.FreelancerShort,
      levels: List[bool]):

    for child in countedTree.children:
      self._updateNode(child, knowledges, freelancerShort, levels)

  def _updateNode(
      self,
      node: Skill,
      knowledges: List[FreelancerKnowledge],
      freelancerShort: FreelancerCountTreeService.FreelancerShort,
      levels: List[bool]):
    if isinstance(node, CountedKnowledgeViewAdapter):
      indexKnowledge = self._findKnowledgeIndex(node.name, knowledges)
      if indexKnowledge >= 0:
        knowledge = knowledges.pop(indexKnowledge)
        if knowledge.score == 99:
          return False
        node.freelancerLevels[knowledge.score - 1].add(freelancerShort)

        if levels[knowledge.score - 1]:
          node.freelancerResult.add(freelancerShort)
          return True

      return False

    _scored = False
    for child in node.children:
      if self._updateNode(child, knowledges, freelancerShort, levels):
        for freelancer in child.freelancerResult:
          node.freelancerResult.add(freelancer)
        _scored = True
        node.scored = True

      for i in range(4):
        node.freelancerLevels[i] = node.freelancerLevels[i].union(
          child.freelancerLevels[i])

    return _scored

  def _findKnowledgeIndex(
      self,
      name: str,
      knowledges: List[FreelancerKnowledge]) -> int:
    for index, knowledge in enumerate(knowledges):
      if knowledge.name == name:
        return index
    return -1


@AutoWire
class FreelancerPeriodServiceImpl(FreelancerPeriodService):

  freelancerQueryService: FreelancerQueryService

  RatingScales = FreelancerPeriodService.RatingScales
  RatePeriodResult = FreelancerPeriodService.RatePeriodResult
  Period = FreelancerPeriodService.Period

  def GetChangeRate(self, period: Period) -> RatePeriodResult:
    previous, current = self.freelancerQueryService\
      .ListFreelancersByTwoLastPeriod(period)

    cantCurrent = len(current)
    cantPrevious = len(previous)

    if cantPrevious != 0:
      changeRate = (
        (cantCurrent - cantPrevious) / (cantPrevious + 0.0)) * 100
    else:
      changeRate = cantCurrent * 100

    if changeRate >= 15:
      scale = self.RatingScales.GOOD
    elif changeRate >= 5:
      scale = self.RatingScales.NORMAL
    else:
      scale = self.RatingScales.BAD

    return self.RatePeriodResult(cantCurrentAffiliates=cantCurrent,
                                 cantPreviousAffiliates=cantPrevious,
                                 rate=str(int(changeRate)), scale=scale)

  def ListFreelancersByPeriod(self, period: Period):
    return self.freelancerQueryService.ListFreelancersByPeriod(period)

  def ListFreelancersByTwoLastPeriod(self, period: Period):
    return self.freelancerQueryService.ListFreelancersByTwoLastPeriod(
      period)


@AutoWire
class InitiativeCreationServiceImpl(InitiativeCreationService):

  CompanyWorkers = InitiativeCreationService.CompanyWorkers
  CompanyFolderInformation = InitiativeCreationService.CompanyFolderInformation

  initiativeQueryService: InitiativeQueryService

  def ListCompanyWorkers(self) -> List[CompanyWorkers]:
    accounts = self.initiativeQueryService.ListAllAccounts()
    contacts = self.initiativeQueryService.ListAllContacts()

    companyWorkers = []
    for account in accounts:
      _contacts = [contact[1]
                   for contact in contacts if contact[0] == account.code]
      companyWorkers.append(
        self.CompanyWorkers(
          company=account,
          contacts=_contacts))

    return companyWorkers

  def GetCompanyFolderInformation(
      self, companyCode: CompanyCode) -> CompanyFolderInformation:
    return self.initiativeQueryService.FindCompany(companyCode=companyCode)


@AutoWire
class AutoKnowledgeServiceImpl(AutoKnowledgeService):

  freelancerCommandService: FreelancerCommandService
  freelancerQueryService: FreelancerQueryService
  freelancerKnowledgeTreeService: FreelancerKnowledgeTreeService
  googleDriveService: GoogleDriveService
  skillQueryService: SkillQueryService

  def UpdateKnowledgesFromPortfolio(
      self, cvs: List[CV],
      freelancer: Freelancer):
    resumeKnowledges = self._GetKnowledgesFromResumes(cvs, freelancer)
    knowledges = resumeKnowledges

    if not knowledges:
      return None

    self.freelancerCommandService.DropPremarkedKnowledges(freelancer)
    self._UpdateKnowledges(freelancer, knowledges)

    return self._makeHTMLTree(freelancer)

  def _GetKnowledgesFromResumes(
      self, cvs: List[CV],
      freelancer: Freelancer) -> Set[FreelancerKnowledge]:
    resumeKnowledges = set()
    for cv in cvs:
      resumeText = self._ReadPDF(cv)
      knowledges = self._ParsePDFText(freelancer, resumeText)
      resumeKnowledges |= knowledges
    return resumeKnowledges

  def _ReadPDF(self, cvVal: CV) -> str:
    txt = ''
    driveFile = self.googleDriveService._DownloadFile(cvVal.googleId)
    pdf = PdfFileReader(driveFile)
    for i in range(pdf.getNumPages()):
      page = pdf.getPage(i)
      txt += page.extractText()
    return txt

  def _ParsePDFText(
      self,
      freelancer: Freelancer,
      pdfText: str) -> Set[FreelancerKnowledge]:
    import string
    text = ''.join(x for x in pdfText if ord(x) < 128)
    # TODO: sería bueno eliminar las preposiciones como se hacía con NLTK
    pdfSkills = [word.strip(string.punctuation) for word in text.split()]
    return self._MatchKnowledges(freelancer, pdfSkills)

  def _ReadLinkedin(self,) -> str:
    ...

  def _ParseLinkedinText(
    self,) -> Set[FreelancerKnowledge]: ...

  def _UpdateKnowledges(
      self,
      freelancer: Freelancer,
      knowledges: List[FreelancerKnowledge]):
    # TODO: Crear command StoreKnowledges utilizando batch update or create
    for knowledge in knowledges:
      self.freelancerCommandService.StoreKnowledge(freelancer, knowledge)

  def _MatchKnowledges(
      self,
      freelancer: Freelancer,
      portfolioSkills: List[str]) -> Set[FreelancerKnowledge]:
    skillsMatchORM = self.freelancerQueryService.ListKnowledgesNotScored(
      freelancer)
    knowledges = set()
    for skillName in portfolioSkills:
      try:
        skillMatches = self._getCloseMatches(skillName, skillsMatchORM)
        knowledges.update([
          FreelancerKnowledge(
            key=skill.key, name=skill.name,
            score=FreelancerKnowledge.Score.PREMARKED)
          for skill in skillMatches])
      except BaseException:
        pass

    return knowledges

  def _getCloseMatches(
      self, skillName: str, skills: Set[Skill],
      precision: float = 70) -> List[Skill]:
    return [
      skill for skill in skills if fuzz.ratio(
        skillName,
        skill.name) >= precision]

  def _makeHTMLTree(self, freelancer: Freelancer) -> str:
    knowledges = self.freelancerQueryService.ListKnowledges(freelancer)
    skillTree = self.skillQueryService.LoadRolesKnowledgeTree(freelancer.roleInterests)
    tree = self.freelancerKnowledgeTreeService.MakeTreeEdit(
      knowledges, skillTree)
    knowledgeTree = SkillTreeViewAdapter(tree).root
    HtmlTree = ''
    for child in knowledgeTree.children:
      HtmlTree += self._makeHTMLTreeBranch(child)
    return HtmlTree

  def _makeHTMLTreeBranch(self, node):
    html = ''

    if node.isKnowledge:
      html += f'''<li><div id='knowledge-line-{node.key}' class='knowledge-line pre-marked'>''' if node.isPremarked else f'''<li><div id='knowledge-line-{node.key}' class='knowledge-line'>'''
      html += f'''<input type='checkbox' id='{node.code}-box' '''
      html += '''checked>''' if node.isScoredOrPremarked else ''' disabled>'''
      html += f'''<label id='{node.code}' '''
      html += '''class='scored pre-marked' style='background:none;' ''' if node.isPremarked else ''' class='scored' ''' if node.isScoredOrPremarked else '''class='no-scored' '''
      html += f'''>{node.name}:</label>'''
      html += f'''<ul class='knowledge-options'>'''
      html += f'''<form> '''
      # {% csrf_token %}
      html += f'''<li>'''
      html += f'''<input type='hidden' name='knowledge-key-{node.key}' value='{node.key}'/>'''
      html += f'''<input type='hidden' name='knowledge-name-{node.key}' value='{node.name}'/>'''
      html += f'''<input type='hidden' name='current-score-{node.key}' value='{node.score}'/>'''
      html += f'''<input type='radio' name='new-score-{node.key}' value='1' id='{node.key}-score1' '''
      html += f'''onclick='OnKnowledgeClick(this, `{node.key}`, `{node.name}`, `{node.code}` )' '''
      html += '''checked''' if node.isBeginner else ''' '''
      html += f'''/><label for='{node.key}-score1'> <span id='{node.key}-emote1' '''
      html += '''class='input-knowledge scored' ''' if node.isBeginner else '''class='input-knowledge' '''
      html += f'''>±1 <br> año</span></label></li>'''

      html += f'''<li>'''
      html += f'''<input type='radio' name='new-score-{node.key}' value='2' id='{node.key}-score2' '''
      html += f'''onclick='OnKnowledgeClick(this, `{node.key}`, `{node.name}`, `{node.code}` )' '''
      html += '''checked''' if node.isJunior else ''' '''
      html += f'''/><label for='{node.key}-score2'> <span id='{node.key}-emote2' '''
      html += '''class='input-knowledge scored' ''' if node.isJunior else '''class='input-knowledge' '''
      html += f'''>+2 <br> años</span></label></li>'''

      html += f'''<li>'''
      html += f'''<input type='radio' name='new-score-{node.key}' value='3' id='{node.key}-score3' '''
      html += f'''onclick='OnKnowledgeClick(this, `{node.key}`, `{node.name}`, `{node.code}` )' '''
      html += 'checked' if node.isMiddle else ''
      html += f'''/><label for='{node.key}-score3'> <span id='{node.key}-emote3' '''
      html += '''class='input-knowledge scored' ''' if node.isMiddle else '''class='input-knowledge' '''
      html += f'''>+3 <br> años</span></label></li>'''

      html += f'''<li>'''
      html += f'''<input type='radio' name='new-score-{node.key}' value='4' id='{node.key}-score4' '''
      html += f'''onclick='OnKnowledgeClick(this, `{node.key}`, `{node.name}`, `{node.code}` )' '''
      html += '''checked''' if node.isSenior else ''' '''
      html += f'''/><label for='{node.key}-score4'> <span id='{node.key}-emote4' '''
      html += '''class='input-knowledge scored' ''' if node.isSenior else '''class='input-knowledge' '''
      html += f'''>+4 <br> años</span></label></li>'''

      if node.isPremarked:
        html += f'''<li id='{node.key}-pre-marked-li' class='trash-icon-container'>'''
        html += f'''<input type='radio' name='new-score-{node.key}' value='-1' id='{node.key}-score-1' '''
        html += f'''onclick='OnKnowledgeClick(this, `{node.key}`, `{node.name}`, `{node.code}` )' '''
        html += f'''/><label for='{node.key}-score-1'> <img id='{node.key}-emote-1' '''
        html += f'''class='input-trash' src='{imgs.TRASH_ICON}' /></label></li>'''

      html += '''</form> </ul> </div></li>'''

    else:
      html += '''<li class='line-group'>'''
      html += '''<input type='checkbox' '''
      html += '''class='selector-open' ''' if node.hasScoredOrPremarkedChild else '''class='selector-close' '''
      html += f'''id={node.GetId}>'''
      html += f'''<input type='checkbox' class='group-checkbox' id='{node.code}-box' disabled '''

      html += '''checked''' if node.hasScoredOrPremarkedChild else ''' '''
      html += f'''><label for={node.GetId} id='{node.code}' '''
      html += '''class='group-name scored' ''' if node.hasScoredOrPremarkedChild else '''class='group-name no-scored' '''
      html += f'''>{node.name}'''
      html += '''<span class='pre-marked-indicator'>*</span></label>''' if node.hasPremarkedChild else '''</label>'''
      html += f'''<ul class='interior'>''' if not node.hasScoredOrPremarkedChild else '''<ul>'''

      for child in node.children:
        html += self._makeHTMLTreeBranch(child)

      html += '''</ul> </li>'''

    return html
