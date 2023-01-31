from abc import abstractmethod
from datetime import datetime, timedelta
from typing import List, Tuple

from neom.ddd.shared import Entity, Repository, ValueObject

from sinek.domain.model.candidate import CandidateId
from sinek.domain.shared import NotFoundError


class ComplexAnswer(ValueObject):
  number: int
  combination: Tuple[bool, bool, bool]


class ComplexRecord(Entity):
  def __init__(self, candidateId: CandidateId, answers: List[ComplexAnswer],
               start: datetime, finish: datetime):
    if finish - start > timedelta(seconds=485):
      raise ValueError(
        f'Completion time "{finish-start}" has exceeded the expected.')

    self.candidateId = candidateId
    self.answers = answers
    self.start = start
    self.finish = finish


class ComplexRecordRepository(Repository):

  @abstractmethod
  def Find(self, candidateId: CandidateId):
    ...

  @abstractmethod
  def Store(self, complexRecord: ComplexRecord):
    ...


class ComplexRecordNotFoundError(NotFoundError):
  pass
