from sinek.domain.model.candidate import CandidateId
from sinek.domain.model.personality_test.complex import (
    ComplexAnswer, ComplexRecord, ComplexRecordNotFoundError,
    ComplexRecordRepository)

from .models import CandidateComplexAnswers as ORMCandidateComplexAnswers
from .models import CandidateComplexRecord as ORMCandidateComplexRecord


class ComplexRecordRepositoryORM(ComplexRecordRepository):

  def Find(self, candidateId: CandidateId) -> ComplexRecord:
    try:
      ormCandidateComplexRecord = ORMCandidateComplexRecord.objects.get(
        candidateId=candidateId.email)
    except ORMCandidateComplexRecord.DoesNotExist as error:
      raise ComplexRecordNotFoundError(
        f'candidate id: {candidateId}') from error

    ormCandidateComplexAnswers = ormCandidateComplexRecord.\
      complexanswers_set.all()

    answers = [
      ComplexAnswer(
        number=answer.number,
        combination=(answer.option_a, answer.option_b, answer.option_c))
      for answer in ormCandidateComplexAnswers]

    return ComplexRecord(
      candidateId,
      answers,
      ormCandidateComplexRecord.start,
      ormCandidateComplexRecord.finish)

  def Store(self, complexRecord: ComplexRecord):
    if ORMCandidateComplexRecord.objects.filter(
        candidateId=str(complexRecord.candidateId)).exists():
      ormCandidateComplexRecord = ORMCandidateComplexRecord.objects.get(
        candidateId=str(complexRecord.candidateId))

      ormCandidateComplexRecord.start = complexRecord.start
      ormCandidateComplexRecord.finish = complexRecord.finish
    else:
      ormCandidateComplexRecord = ORMCandidateComplexRecord.objects.create(
        candidateId=str(complexRecord.candidateId), start=complexRecord.start,
        finish=complexRecord.finish)

    ormCandidateComplexRecord.complexanswers_set.all().delete()

    ORMCandidateComplexAnswers.objects.bulk_create(_MakeFrom(
      ormCandidateComplexRecord, answer) for answer in complexRecord.answers)


def _MakeFrom(
    ormRecord: ORMCandidateComplexRecord,
    answer: ComplexAnswer) -> ORMCandidateComplexAnswers:
  return ORMCandidateComplexAnswers(
    number=answer.number,
    option_a=answer.combination[0],
    option_b=answer.combination[1],
    option_c=answer.combination[2],
    complexRecord=ormRecord)
