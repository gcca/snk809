from abc import abstractmethod
from typing import List

from neom.ddd.shared import Entity, Repository, ValueObject

from sinek.domain.model.candidate import Candidate, CandidateId
from sinek.domain.shared import NotFoundError


class TMMS24Answer(ValueObject):
  number: int
  score: str


class TMMS24Record(Entity):
  candidateId: CandidateId
  answers: List[TMMS24Answer]


class TMMS24RecordRepository(Repository):

  @abstractmethod
  def Find(self, candidate: Candidate):
    ...

  @abstractmethod
  def Store(self, discRecord: TMMS24Record):
    ...


class TMMS24RecordNotFoundError(NotFoundError):
  pass
