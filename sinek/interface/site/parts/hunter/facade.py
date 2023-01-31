from typing import List, Tuple

from neom.core.ioc import AutoWire

from sinek.application.account import UserRoleService
from sinek.domain.model.candidate import (Candidate, CandidateId,
                                          CandidateRepository)
from sinek.domain.model.personality_test.anchor import AnchorRecordRepository
from sinek.domain.model.personality_test.complex import ComplexRecordRepository
from sinek.domain.model.personality_test.disc import DiscRecordRepository
from sinek.domain.model.personality_test.tmms24 import TMMS24RecordRepository
from sinek.domain.service import (AffiliationService, AnchorEvaluationService,
                                  CandidateTestChecklistService,
                                  ComplexEvaluationService,
                                  DISCEvaluationService,
                                  TMMS24EvaluationService)
from sinek.interface.site.parts.hunter.adapter import (
  AnchorResultViewAdapter, ChecklistViewAdapter, ComplexResultViewAdapter,
  DISCResultViewAdapter, TMMS24ResultViewAdapter)


from .forms import AffiliationForm


@AutoWire
class AffiliationServiceFacade:

  affiliationService: AffiliationService
  userRoleService: UserRoleService

  def Affiliate(self, form: AffiliationForm):
    candidateName = form['name'].value()
    candidateEmail = form['email'].value()
    candidateGender = form['gender'].value()

    candidateId = CandidateId(candidateEmail)
    candidate = Candidate(
      name=candidateName,
      candidateId=candidateId,
      gender=Candidate.Gender(int(candidateGender)))
    self.affiliationService.Affiliate(candidate)

    # TODO: get password from user browser
    self.userRoleService.CreateUser(candidate, candidate.email)


@AutoWire
class DiscEvaluationServiceFacade:

  discEvaluationService: DISCEvaluationService

  candidateRepository: CandidateRepository
  discRecordRepository: DiscRecordRepository

  def Evaluate(
      self, candidateEmail: str) -> Tuple[DISCResultViewAdapter, Candidate]:
    candidateId = CandidateId(candidateEmail)
    candidate = self.candidateRepository.Find(candidateId)
    record = self.discRecordRepository.Find(candidateId)
    result = self.discEvaluationService.Evaluate(record)
    return DISCResultViewAdapter(result), candidate


@AutoWire
class Tmms24EvaluationServiceFacade:

  tmms24EvaluationService: TMMS24EvaluationService

  candidateRepository: CandidateRepository
  tmms24RecordRepository: TMMS24RecordRepository

  def Evaluate(
      self, candidateEmail: str) -> Tuple[TMMS24ResultViewAdapter, Candidate]:
    candidateId = CandidateId(candidateEmail)
    candidate = self.candidateRepository.Find(candidateId)
    record = self.tmms24RecordRepository.Find(candidate)
    result = self.tmms24EvaluationService.Evaluate(candidate, record)
    return TMMS24ResultViewAdapter(result), candidate


@AutoWire
class CandidateTestChecklistServiceFacade:

  candidateTestChecklistService: CandidateTestChecklistService

  def ListForAllCandidates(self) -> List[ChecklistViewAdapter]:
    checklists = self.candidateTestChecklistService.ListForAllCandidates()
    return [ChecklistViewAdapter(checklist) for checklist in checklists]

  def ListForOneCandidate(self, email: str) -> ChecklistViewAdapter:
    candidateId = CandidateId(email)
    checklist = self.candidateTestChecklistService.ListForOneCandidate(
      candidateId)
    return ChecklistViewAdapter(checklist)


@AutoWire
class AnchorEvaluationServiceFacade:

  anchorEvaluationService: AnchorEvaluationService

  candidateRepository: CandidateRepository
  anchorRecordRepository: AnchorRecordRepository

  def Evaluate(self, candidateEmail: str):
    candidateId = CandidateId(candidateEmail)
    candidate = self.candidateRepository.Find(candidateId)
    record = self.anchorRecordRepository.Find(candidateId)
    result = self.anchorEvaluationService.Evaluate(record)
    return AnchorResultViewAdapter(result), candidate


@AutoWire
class ComplexEvaluationServiceFacade:

  complexEvaluationService: ComplexEvaluationService

  candidateRepository: CandidateRepository
  complexRecordRepository: ComplexRecordRepository

  def Evaluate(self, candidateEmail: str):
    candidateId = CandidateId(candidateEmail)
    candidate = self.candidateRepository.Find(candidateId)
    record = self.complexRecordRepository.Find(candidateId)
    result = self.complexEvaluationService.Evaluate(record)
    return ComplexResultViewAdapter(result), candidate
