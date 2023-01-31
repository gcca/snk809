from abc import abstractmethod
from typing import List

from neom.ddd.shared import Entity, Repository, ValueObject

from sinek.domain.model.candidate import CandidateId
from sinek.domain.shared import NotFoundError


class DiscAnswer(ValueObject):
  number: int
  plus: str
  minus: str


class DiscRecord(Entity):
  candidateId: CandidateId
  answers: List[DiscAnswer]


class DiscRecordRepository(Repository):

  @abstractmethod
  def Find(self, candidateId: CandidateId):
    ...

  @abstractmethod
  def Store(self, discRecord: DiscRecord):
    ...


class DiscRecordNotFoundError(NotFoundError):
  pass
