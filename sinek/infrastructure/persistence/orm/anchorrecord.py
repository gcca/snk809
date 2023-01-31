from sinek.domain.model.candidate import CandidateId
from sinek.domain.model.personality_test.anchor import (
    AnchorAnswer, AnchorRecord, AnchorRecordNotFoundError,
    AnchorRecordRepository)

from .models import CandidateAnchorAnswers as ORMCandidateAnchorAnswers
from .models import CandidateAnchorRecord as ORMCandidateAnchorRecord


class AnchorRecordRepositoryORM(AnchorRecordRepository):

  def Find(self, candidateId: CandidateId) -> AnchorRecord:
    try:
      ormCandidateAnchorRecord = ORMCandidateAnchorRecord.objects.get(
        candidateId=candidateId.email)
    except ORMCandidateAnchorRecord.DoesNotExist as error:
      raise AnchorRecordNotFoundError(
        f'candidate id: {candidateId}') from error

    ormCandidateAnchorAnswers = ormCandidateAnchorRecord.anchoranswers_set.all()

    answers = [
      AnchorAnswer(
        number=answer.number,
        score=answer.score)
      for answer in ormCandidateAnchorAnswers]

    return AnchorRecord(candidateId=candidateId,
                        answers=answers,
                        relevants=(ormCandidateAnchorRecord.relevant1,
                                   ormCandidateAnchorRecord.relevant2,
                                   ormCandidateAnchorRecord.relevant3))

  def Store(self, discRecord: AnchorRecord):
    if ORMCandidateAnchorRecord.objects.filter(
        candidateId=str(discRecord.candidateId)).exists():
      ormCandidateAnchorRecord = ORMCandidateAnchorRecord.objects.get(
        candidateId=str(discRecord.candidateId))

      ormCandidateAnchorRecord.relevant1 = discRecord.relevants[0]
      ormCandidateAnchorRecord.relevant2 = discRecord.relevants[1]
      ormCandidateAnchorRecord.relevant3 = discRecord.relevants[2]
    else:
      ormCandidateAnchorRecord = ORMCandidateAnchorRecord.objects.create(
        candidateId=str(discRecord.candidateId),
        relevant1=discRecord.relevants[0],
        relevant2=discRecord.relevants[1],
        relevant3=discRecord.relevants[2])

    ormCandidateAnchorRecord.anchoranswers_set.all().delete()

    ORMCandidateAnchorAnswers.objects.bulk_create(_MakeFrom(
      ormCandidateAnchorRecord, answer) for answer in discRecord.answers)


def _MakeFrom(ormRecord: ORMCandidateAnchorRecord,
              answer: AnchorAnswer) -> ORMCandidateAnchorAnswers:
  return ORMCandidateAnchorAnswers(
    anchorRecord=ormRecord,
    number=answer.number,
    score=answer.score
  )
