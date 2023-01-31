import re
from abc import abstractmethod
from enum import IntEnum, unique
from typing import List

from neom.ddd.shared import Identity, Repository

from sinek.domain.shared import NotFoundError

from .role import Role


class CandidateId(Identity):

  EMAIL_RE = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

  def __init__(self, email: str):
    if email is None:
      raise TypeError('null email')

    if not re.fullmatch(self.EMAIL_RE, email):
      raise ValueError(f'{email} is an invalid email')

    self.email = email

  def __str__(self):
    return self.email


class Candidate(Role):

  @unique
  class Gender(IntEnum):
    MALE = 0
    FEMALE = 1

    def IsMale(self):
      return self.value == self.MALE

    def IsFemale(self):
      return self.value == self.FEMALE

  candidateId: CandidateId
  name: str
  gender: Gender

  @property
  def email(self):
    return self.candidateId.email

  @staticmethod
  def IsCandidate():
    return True


class CandidateRepository(Repository):

  @abstractmethod
  def Find(self, candidateId: CandidateId) -> Candidate:
    """
    Raises:
      CandidateNotFoundError when does not exists a candidate with the given id
    """

  @abstractmethod
  def All(self) -> List[Candidate]:
    """
    Returns a list with the candidates or an empty list
    when does not exists candidates
    """

  @abstractmethod
  def Store(self, candidate: Candidate):
    pass


class CandidateNotFoundError(NotFoundError):
  pass
