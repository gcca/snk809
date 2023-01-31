from abc import abstractmethod
from typing import List, Tuple

from neom.ddd.shared import Entity, Repository, ValueObject

from sinek.domain.model.candidate import CandidateId
from sinek.domain.shared import NotFoundError


class AnchorAnswer(ValueObject):
  number: int
  score: str


class AnchorRecord(Entity):
  candidateId: CandidateId
  answers: List[AnchorAnswer]
  relevants: Tuple[int, int, int]


class AnchorRecordRepository(Repository):

  @abstractmethod
  def Find(self, candidateId: CandidateId):
    ...

  @abstractmethod
  def Store(self, discRecord: AnchorRecord):
    ...


class AnchorRecordNotFoundError(NotFoundError):
  pass
