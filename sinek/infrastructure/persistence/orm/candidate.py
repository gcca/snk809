from typing import List


from sinek.domain.model.candidate import (Candidate, CandidateId,
                                          CandidateNotFoundError,
                                          CandidateRepository)

from .models import Candidate as ORMCandidate


class CandidateRepositoryORM(CandidateRepository):

  def Find(self, id: CandidateId) -> Candidate:

    if not isinstance(id, CandidateId):
      raise TypeError('candidateId must be a CandidateId,'
                      f' not {type(id)}')

    try:
      ormCandidate = ORMCandidate.objects.get(email=id.email)
    except ORMCandidate.DoesNotExist as error:
      raise CandidateNotFoundError(
          f'No candidate "{id.email}"') from error

    return self._makeFrom(ormCandidate)

  def All(self) -> List[Candidate]:
    ormCandidates = ORMCandidate.objects.all()
    candidates = [self._makeFrom(candidate)
                  for candidate in ormCandidates]

    return candidates

  def Store(self, candidate: Candidate):
    try:
      ormCandidate = ORMCandidate.objects.get(email=candidate.email)
    except ORMCandidate.DoesNotExist:
      ormCandidate = ORMCandidate()

    # TODO: Añadir campos adicionales
    ormCandidate.name = candidate.name
    ormCandidate.email = candidate.email
    ormCandidate.gender = candidate.gender.value
    #ormCandidate.mobile = candidate.mobile
    ormCandidate.save()

  def _makeFrom(self, ormCandidate: ORMCandidate) -> Candidate:
    candidateId = CandidateId(ormCandidate.email)
    return Candidate(
        candidateId=candidateId,
        name=ormCandidate.name,
        gender=self._getDomainGender(ormCandidate)
    )

  def _getDomainGender(self, ormCandidate: ORMCandidate) -> Candidate.Gender:
    if ORMCandidate.GenderId.Male == ormCandidate.gender:
      return Candidate.Gender.MALE
    if ORMCandidate.GenderId.Female == ormCandidate.gender:
      return Candidate.Gender.FEMALE
    raise ValueError(
        f'Invalid GenderId {ormCandidate.gender} for \
          Candidate with email {ormCandidate.email}')
