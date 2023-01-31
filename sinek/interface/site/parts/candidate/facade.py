from datetime import datetime, timezone
from typing import List, Tuple

from neom.core.ioc import AutoWire

from sinek.domain.model.candidate import CandidateId
from sinek.domain.model.personality_test.anchor import (AnchorAnswer,
                                                        AnchorRecord)
from sinek.domain.model.personality_test.complex import (ComplexAnswer,
                                                         ComplexRecord)
from sinek.domain.model.personality_test.disc import DiscAnswer, DiscRecord
from sinek.domain.model.personality_test.tmms24 import (TMMS24Answer,
                                                        TMMS24Record)
from sinek.domain.service import (RecordAnchorAnswersService,
                                  RecordComplexAnswersService,
                                  RecordDISCAnswersService,
                                  RecordTMMS24AnswersService)

from .forms import (AnchorTestForm, ComplexTestForm, DISCTestForm,
                    TMMS24TestForm)


@AutoWire
class RecordDISCAnswersServiceFacade:

  recordDISCAnswersService: RecordDISCAnswersService
  orderDisc = {
    1: (2, 4, 1, 3),
    2: (1, 4, 2, 3),
    3: (4, 1, 3, 2),
    4: (4, 1, 3, 2),
    5: (3, 2, 4, 1),
    6: (4, 1, 3, 2),
    7: (2, 4, 1, 3),
    8: (1, 4, 2, 3),
    9: (4, 1, 3, 2),
    10: (2, 1, 3, 4),
    11: (1, 2, 4, 3),
    12: (4, 3, 2, 1),
    13: (4, 2, 3, 1),
    14: (4, 3, 2, 1),
    15: (1, 2, 3, 4),
    16: (3, 1, 2, 4),
    17: (4, 2, 1, 3),
    18: (2, 4, 1, 3),
    19: (2, 3, 4, 1),
    20: (4, 3, 1, 2),
    21: (3, 1, 4, 2),
    22: (3, 2, 1, 4),
    23: (1, 2, 3, 4),
    24: (2, 1, 3, 4),
  }

  def Record(self, email: str, form: DISCTestForm):
    answers = self._makeAnswers(form)
    candidateId = CandidateId(email)
    self.recordDISCAnswersService.Record(candidateId, answers)

  def _makeAnswers(self, form: DISCTestForm) -> List[DiscAnswer]:
    numberQuestions = 24
    return [
      self._makeDiscAnswer(
        i, form) for i in range(
        1, numberQuestions + 1)]

  def _makeDiscAnswer(self, number: str, form: DISCTestForm) -> DiscAnswer:
    plusSelected = form.cleaned_data['answer_' + str(number) + '_plus']
    minusSelected = form.cleaned_data['answer_' + str(number) + '_minus']
    return DiscAnswer(number=number,
                      plus=self.orderDisc[number][int(plusSelected) - 1],
                      minus=self.orderDisc[number][int(minusSelected) - 1])


@AutoWire
class RecordTMMS24AnswersServiceFacade:

  recordTMMS24AnswersService: RecordTMMS24AnswersService

  def Record(self, email: str, form: TMMS24TestForm):
    answers = self._makeAnswers(form)
    candidateId = CandidateId(email)
    self.recordTMMS24AnswersService.Record(candidateId, answers)

  def _makeAnswers(self, form: TMMS24TestForm) -> List[TMMS24Answer]:
    numberQuestions = 24
    return [
      self._makeTMMS24Answer(
        i, form) for i in range(
        1, numberQuestions + 1)]

  def _makeTMMS24Answer(self, number: str, form: DISCTestForm) -> TMMS24Answer:
    return TMMS24Answer(number=number,
                        score=form.cleaned_data['answer_' + str(number)])


@AutoWire
class RecordAnchorAnswersServiceFacade:

  recordAnchorAnswersService: RecordAnchorAnswersService

  def Record(self, email: str, form: AnchorTestForm):
    answers = self._makeAnswers(form)
    favourites = self._makeFavourites(form)
    candidateId = CandidateId(email)
    self.recordAnchorAnswersService.Record(candidateId, answers, favourites)

  def _makeAnswers(self, form: AnchorTestForm) -> List[AnchorAnswer]:
    numberQuestions = 40
    return [
      self._makeAnchorAnswer(
        i, form) for i in range(
        1, numberQuestions + 1)]

  def _makeAnchorAnswer(
      self,
      number: str,
      form: AnchorTestForm) -> AnchorAnswer:
    return AnchorAnswer(number=number,
                        score=form.cleaned_data['answer_' + str(number)])

  def _makeFavourites(self, form: AnchorTestForm) -> Tuple[int, int, int]:
    return (form.cleaned_data['favourite_1'],
            form.cleaned_data['favourite_2'],
            form.cleaned_data['favourite_3'])


@AutoWire
class RecordComplexAnswersServiceFacade:

  recordComplexAnswersService: RecordComplexAnswersService

  def Record(self, email: str, form: ComplexTestForm, session):
    initialTime = datetime.fromtimestamp(session['initialTime'], timezone.utc)
    currentTime = datetime.now(timezone.utc)
    answers = self._makeAnswers(form)
    candidateId = CandidateId(email)
    self.recordComplexAnswersService.Record(
      candidateId, answers, initialTime, currentTime)

  def _makeAnswers(self, form: ComplexTestForm) -> List[ComplexAnswer]:
    numberQuestions = 25
    return [
      self._makeComplexAnswer(i, form) for i in range(1, numberQuestions + 1)]

  def _makeComplexAnswer(
      self,
      number: str,
      form: ComplexTestForm) -> AnchorAnswer:
    return ComplexAnswer(number=number,
                         combination=(
                           form.cleaned_data['answer_' + str(number) + '_a'],
                           form.cleaned_data['answer_' + str(number) + '_b'],
                           form.cleaned_data['answer_' + str(number) + '_c']
                         )
                         )
