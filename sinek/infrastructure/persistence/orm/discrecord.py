from sinek.domain.model.candidate import CandidateId
from sinek.domain.model.personality_test.disc import (DiscAnswer, DiscRecord,
                                                      DiscRecordNotFoundError,
                                                      DiscRecordRepository)

from .models import CandidateDiscAnswers as ORMCandidateDiscAnswers


class DiscRecordRepositoryORM(DiscRecordRepository):

  def Find(self, candidateId: CandidateId) -> DiscRecord:
    ormCandidateDiscAnswers = ORMCandidateDiscAnswers.objects.filter(
      candidateId=candidateId.email)

    if not ormCandidateDiscAnswers:
      raise DiscRecordNotFoundError(f'candidate id: {candidateId}')

    answers = [
      DiscAnswer(
        number=answer.number,
        plus=answer.plus,
        minus=answer.minus) for answer in ormCandidateDiscAnswers]

    return DiscRecord(candidateId=candidateId, answers=answers)

  def Store(self, discRecord: DiscRecord):

    to_create = []
    to_update = []

    # wtf o_ O
    [
      to_update.append(
        _make_from_to_update(
          discRecord.candidateId,
          answer)) if ORMCandidateDiscAnswers.objects.filter(
        candidateId=discRecord.candidateId.email,
        number=answer.number).exists() else to_create.append(
          _make_from(
            discRecord.candidateId,
            answer)) for answer in discRecord.answers]

    if to_create:
      ORMCandidateDiscAnswers.objects.bulk_create(to_create)
    if to_update:
      ORMCandidateDiscAnswers.objects.bulk_update(to_update, ['plus', 'minus'])


def _make_from(candidateId: CandidateId,
               answer: DiscAnswer) -> ORMCandidateDiscAnswers:
  return ORMCandidateDiscAnswers(
    candidateId=candidateId.email,
    number=answer.number,
    plus=answer.plus,
    minus=answer.minus)


def _make_from_to_update(candidateId: CandidateId,
                         answer: DiscAnswer) -> ORMCandidateDiscAnswers:
  ormCandidateDiscAnswer = ORMCandidateDiscAnswers.objects.get(
    candidateId=candidateId.email, number=answer.number)
  ormCandidateDiscAnswer.plus = answer.plus
  ormCandidateDiscAnswer.minus = answer.minus
  return ormCandidateDiscAnswer
