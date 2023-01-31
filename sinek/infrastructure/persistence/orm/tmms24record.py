
from sinek.domain.model.candidate import CandidateId
from sinek.domain.model.personality_test.tmms24 import (
  TMMS24Answer, TMMS24Record, TMMS24RecordNotFoundError,
  TMMS24RecordRepository)

from .models import CandidateTMMS24Answers as ORMCandidateTMMS24Answers


class TMMS24RecordRepositoryORM(TMMS24RecordRepository):

  def Find(self, candidateId: CandidateId) -> TMMS24Record:
    ormCandidateTMMS24Answers = ORMCandidateTMMS24Answers.objects.filter(
      candidateId=candidateId.email)

    if not ormCandidateTMMS24Answers:
      raise TMMS24RecordNotFoundError(f'candidate id: {candidateId.email}')

    answers = [
      TMMS24Answer(
        number=answer.number,
        score=answer.score) for answer in ormCandidateTMMS24Answers]

    candidateId = CandidateId(candidateId.email)
    return TMMS24Record(candidateId=candidateId, answers=answers)

  def Store(self, record: TMMS24Record):

    to_create = []
    to_update = []

    [
      to_update.append(
        _make_from_to_update(
          record.candidateId,
          answer)) if ORMCandidateTMMS24Answers.objects.filter(
        candidateId=record.candidateId.email,
        number=answer.number).exists() else to_create.append(
          _make_from(
            record.candidateId,
            answer)) for answer in record.answers]

    if to_create:
      ORMCandidateTMMS24Answers.objects.bulk_create(to_create)
    if to_update:
      ORMCandidateTMMS24Answers.objects.bulk_update(to_update, ['score'])


def _make_from(
    candidateId: CandidateId,
    answer: TMMS24Answer) -> ORMCandidateTMMS24Answers:
  return ORMCandidateTMMS24Answers(
    candidateId=candidateId.email,
    number=answer.number,
    score=answer.score)


def _make_from_to_update(candidateId: CandidateId,
                         answer: TMMS24Answer) -> ORMCandidateTMMS24Answers:
  ormCandidateTMMS24Answer = ORMCandidateTMMS24Answers.objects.get(
    candidateId=candidateId.email, number=answer.number)
  ormCandidateTMMS24Answer.score = answer.score
  return ormCandidateTMMS24Answer
