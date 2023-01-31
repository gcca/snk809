from datetime import datetime, timezone
from itertools import combinations
from typing import List, Tuple

from django.test import Client, TestCase
from neom.core.ioc import Wired, wire

from sinek.application.account import UserRoleService
from sinek.domain.model.candidate import (Candidate, CandidateId,
                                          CandidateNotFoundError,
                                          CandidateRepository)
from sinek.domain.model.hunter import Hunter, HunterRepository
from sinek.domain.model.personality_test.anchor import (AnchorAnswer,
                                                        AnchorRecord,
                                                        AnchorRecordRepository)
from sinek.domain.model.personality_test.complex import (
  ComplexAnswer, ComplexRecord, ComplexRecordRepository)
from sinek.domain.model.personality_test.disc import (DiscAnswer, DiscRecord,
                                                      DiscRecordRepository)
from sinek.domain.model.personality_test.tmms24 import (TMMS24Answer,
                                                        TMMS24Record,
                                                        TMMS24RecordRepository)


class HunterTestCase(TestCase):

  @wire
  def setUp(
      self,
      candidateRepository: Wired[CandidateRepository],
      hunterRepository: Wired[HunterRepository],
      userRoleService: Wired[UserRoleService]):
    self.client = Client()

    candidateId = CandidateId('thor@vh.la')
    candidate = Candidate(
      name='thor',
      candidateId=candidateId,
      gender=Candidate.Gender.FEMALE)
    candidateRepository.Store(candidate)

    hunter = Hunter(name='hunter')
    hunterRepository.Store(hunter)

    userRoleService.CreateUser(candidate, candidate.email)
    userRoleService.CreateUser(hunter, hunter.name)

  def test_dashboard_candidate_list(self):
    self.client.login(username='hunter', password='hunter')
    response = self.client.get('/luci/hunter/dashboard/')

    candidatesChecklists = response.context['candidates']

    candidateChecklist = candidatesChecklists[0]

    self.assertEqual(candidateChecklist.candidateName, 'thor')
    self.assertEqual(candidateChecklist.candidateEmail, 'thor@vh.la')

  def test_candidate_details(self):
    self.client.login(username='hunter', password='hunter')
    response = self.client.get('/luci/hunter/candidate/thor@vh.la/')

    candidateChecklist = response.context['check']

    self.assertEqual(candidateChecklist.candidateName, 'thor')
    self.assertEqual(candidateChecklist.candidateEmail, 'thor@vh.la')
    self.assertEqual(candidateChecklist.discCompleted, False)
    self.assertEqual(candidateChecklist.tmms24Completed, False)
    self.assertEqual(candidateChecklist.anchorCompleted, False)

  def test_candidate_disc_case_1(self):
    answers = [DiscAnswer(number=i, plus=1, minus=1) for i in range(1, 25)]
    results = (0, 0, 0, 0, 'PATRONES UNIFORMES')
    self.Test_disc.test_candidate_disc_result(
      self=self, answers=answers, results=results)

  def test_candidate_disc_case_2(self):
    n = self.Test_disc.discnumber
    answers = [
      DiscAnswer(number=1, plus=n['i'], minus=n['c']),
      DiscAnswer(number=2, plus=n['s'], minus=n['i']),
      DiscAnswer(number=3, plus=n['c'], minus=n['i']),
      DiscAnswer(number=4, plus=n['s'], minus=n['d']),
      DiscAnswer(number=5, plus=n['c'], minus=n['d']),
      DiscAnswer(number=6, plus=n['s'], minus=n['c']),
      DiscAnswer(number=7, plus=n['i'], minus=n['s']),
      DiscAnswer(number=8, plus=n['c'], minus=n['i']),
      DiscAnswer(number=9, plus=n['c'], minus=n['i']),
      DiscAnswer(number=10, plus=n['i'], minus=n['c']),
      DiscAnswer(number=11, plus=n['i'], minus=n['c']),
      DiscAnswer(number=12, plus=n['c'], minus=n['s']),
      DiscAnswer(number=13, plus=n['i'], minus=n['s']),
      DiscAnswer(number=14, plus=n['i'], minus=n['d']),
      DiscAnswer(number=15, plus=n['c'], minus=n['s']),
      DiscAnswer(number=16, plus=n['d'], minus=n['i']),
      DiscAnswer(number=17, plus=n['s'], minus=n['c']),
      DiscAnswer(number=18, plus=n['c'], minus=n['i']),
      DiscAnswer(number=19, plus=n['d'], minus=n['c']),
      DiscAnswer(number=20, plus=n['d'], minus=n['c']),
      DiscAnswer(number=21, plus=n['d'], minus=n['c']),
      DiscAnswer(number=22, plus=n['d'], minus=n['c']),
      DiscAnswer(number=23, plus=n['d'], minus=n['c']),
      DiscAnswer(number=24, plus=n['c'], minus=n['s'])
    ]
    results = (3, 0, -1, -2, 'ORGANIZADOR')
    self.Test_disc.test_candidate_disc_result(
      self=self, answers=answers, results=results)

  def test_candidate_disc_case_3(self):
    n = self.Test_disc.discnumber
    answers = [
      DiscAnswer(number=1, plus=n['s'], minus=n['c']),
      DiscAnswer(number=2, plus=n['c'], minus=n['s']),
      DiscAnswer(number=3, plus=n['c'], minus=n['d']),
      DiscAnswer(number=4, plus=n['s'], minus=n['d']),
      DiscAnswer(number=5, plus=n['i'], minus=n['c']),
      DiscAnswer(number=6, plus=n['d'], minus=n['i']),
      DiscAnswer(number=7, plus=n['i'], minus=n['s']),
      DiscAnswer(number=8, plus=n['s'], minus=n['c']),
      DiscAnswer(number=9, plus=n['c'], minus=n['i']),
      DiscAnswer(number=10, plus=n['d'], minus=n['c']),
      DiscAnswer(number=11, plus=n['c'], minus=n['i']),
      DiscAnswer(number=12, plus=n['c'], minus=n['s']),
      DiscAnswer(number=13, plus=n['c'], minus=n['i']),
      DiscAnswer(number=14, plus=n['d'], minus=n['c']),
      DiscAnswer(number=15, plus=n['d'], minus=n['i']),
      DiscAnswer(number=16, plus=n['s'], minus=n['c']),
      DiscAnswer(number=17, plus=n['d'], minus=n['c']),
      DiscAnswer(number=18, plus=n['d'], minus=n['s']),
      DiscAnswer(number=19, plus=n['d'], minus=n['c']),
      DiscAnswer(number=20, plus=n['i'], minus=n['d']),
      DiscAnswer(number=21, plus=n['d'], minus=n['s']),
      DiscAnswer(number=22, plus=n['c'], minus=n['i']),
      DiscAnswer(number=23, plus=n['d'], minus=n['c']),
      DiscAnswer(number=24, plus=n['s'], minus=n['i'])]
    results = (6, -4, 0, -2, 'DIRECTOR')
    self.Test_disc.test_candidate_disc_result(
      self=self, answers=answers, results=results)

  class Test_disc:

    discnumber = {
      'd': 1,
      'i': 2,
      's': 3,
      'c': 4
    }

    @wire
    def test_candidate_disc_result(
        self, discRecordRepository: Wired[DiscRecordRepository],
        answers: List[DiscAnswer],
        results: Tuple[int, int, int, int, str]):
      self.client.login(username='hunter', password='hunter')

      response = self.client.get(
        '/luci/hunter/candidate/thor@vh.la/personality_test/disc')
      self.assertRedirects(response, '/luci/hunter/candidate/thor@vh.la/')

      candidateId = CandidateId('thor@vh.la')
      discRecord = DiscRecord(candidateId=candidateId, answers=answers)

      discRecordRepository.Store(discRecord)

      response = self.client.get(
        '/luci/hunter/candidate/thor@vh.la/personality_test/disc')
      discResult = response.context['result']
      self.assertEqual(discResult.result.compounds[0], results[0])
      self.assertEqual(discResult.result.compounds[1], results[1])
      self.assertEqual(discResult.result.compounds[2], results[2])
      self.assertEqual(discResult.result.compounds[3], results[3])
      self.assertEqual(discResult.personalityText, results[4])

  @wire
  def test_candidate_tmms24_result(
      self, tmms24RecordRepository: Wired[TMMS24RecordRepository]):
    self.client.login(username='hunter', password='hunter')

    response = self.client.get(
      '/luci/hunter/candidate/thor@vh.la/personality_test/tmms24')
    self.assertRedirects(response, '/luci/hunter/candidate/thor@vh.la/')

    answers = [TMMS24Answer(number=i, score=1) for i in range(1, 25)]
    candidateId = CandidateId('thor@vh.la')
    tmms24Record = TMMS24Record(candidateId=candidateId, answers=answers)

    tmms24RecordRepository.Store(tmms24Record)

    response = self.client.get(
      '/luci/hunter/candidate/thor@vh.la/personality_test/tmms24')
    tmms24Result = response.context['result']
    self.assertEqual(tmms24Result.atencionResultText, 'INADECUADO')
    self.assertEqual(tmms24Result.claridadResultText, 'INADECUADO')
    self.assertEqual(tmms24Result.reparacionResultText, 'INADECUADO')

  @wire
  def test_candidate_anchor_result(
      self, anchorRecordRepository: Wired[AnchorRecordRepository]):
    self.client.login(username='hunter', password='hunter')

    response = self.client.get(
      '/luci/hunter/candidate/thor@vh.la/personality_test/anchor')
    self.assertRedirects(response, '/luci/hunter/candidate/thor@vh.la/')

    answers = [AnchorAnswer(number=1, score=3),
               AnchorAnswer(number=2, score=4),
               AnchorAnswer(number=3, score=5),
               AnchorAnswer(number=4, score=6),
               AnchorAnswer(number=5, score=3),
               AnchorAnswer(number=6, score=2),
               AnchorAnswer(number=7, score=2),
               AnchorAnswer(number=8, score=2),
               AnchorAnswer(number=9, score=4),
               AnchorAnswer(number=10, score=5),
               AnchorAnswer(number=11, score=5),
               AnchorAnswer(number=12, score=4),
               AnchorAnswer(number=13, score=4),
               AnchorAnswer(number=14, score=4),
               AnchorAnswer(number=15, score=4),
               AnchorAnswer(number=16, score=4),
               AnchorAnswer(number=17, score=4),
               AnchorAnswer(number=18, score=4),
               AnchorAnswer(number=19, score=4),
               AnchorAnswer(number=20, score=5),
               AnchorAnswer(number=21, score=5),
               AnchorAnswer(number=22, score=5),
               AnchorAnswer(number=23, score=5),
               AnchorAnswer(number=24, score=5),
               AnchorAnswer(number=25, score=6),
               AnchorAnswer(number=26, score=6),
               AnchorAnswer(number=27, score=6),
               AnchorAnswer(number=28, score=3),
               AnchorAnswer(number=29, score=2),
               AnchorAnswer(number=30, score=3),
               AnchorAnswer(number=31, score=3),
               AnchorAnswer(number=32, score=2),
               AnchorAnswer(number=33, score=3),
               AnchorAnswer(number=34, score=4),
               AnchorAnswer(number=35, score=4),
               AnchorAnswer(number=36, score=5),
               AnchorAnswer(number=37, score=1),
               AnchorAnswer(number=38, score=1),
               AnchorAnswer(number=39, score=4),
               AnchorAnswer(number=40, score=3)]
    candidateId = CandidateId('thor@vh.la')
    anchorRecord = AnchorRecord(
      candidateId=candidateId,
      answers=answers,
      relevants=(
        7,
        12,
        35))

    anchorRecordRepository.Store(anchorRecord)

    response = self.client.get(
      '/luci/hunter/candidate/thor@vh.la/personality_test/anchor')
    anchorResult = response.context['result']

    self.assertEqual(anchorResult.firstResultText, 'Autonomía')
    self.assertEqual(anchorResult.secondResultText, 'Seguridad y estabilidad')
    self.assertEqual(
      anchorResult.thirdResultText,
      'Dirección General')
    self.assertEqual(
      anchorResult.totalsResultText, [
        20, 23, 28, 27, 15, 15, 22, 16])

  def test_candidate_complex_case_1(self):
    answers = [ComplexAnswer(number=1, combination=(True, True, False)),
               ComplexAnswer(number=2, combination=(False, True, False)),
               ComplexAnswer(number=3, combination=(False, False, False)),
               ComplexAnswer(number=4, combination=(False, False, True)),
               ComplexAnswer(number=5, combination=(False, False, False)),
               ComplexAnswer(number=6, combination=(False, False, False)),
               ComplexAnswer(number=7, combination=(False, False, False)),
               ComplexAnswer(number=8, combination=(False, False, False)),
               ComplexAnswer(number=9, combination=(False, False, False)),
               ComplexAnswer(number=10, combination=(False, False, False)),
               ComplexAnswer(number=11, combination=(False, False, False)),
               ComplexAnswer(number=12, combination=(False, False, False)),
               ComplexAnswer(number=13, combination=(False, False, False)),
               ComplexAnswer(number=14, combination=(False, False, False)),
               ComplexAnswer(number=15, combination=(False, False, False)),
               ComplexAnswer(number=16, combination=(False, False, False)),
               ComplexAnswer(number=17, combination=(False, False, False)),
               ComplexAnswer(number=18, combination=(False, False, False)),
               ComplexAnswer(number=19, combination=(False, False, False)),
               ComplexAnswer(number=20, combination=(False, False, False)),
               ComplexAnswer(number=21, combination=(False, False, False)),
               ComplexAnswer(number=22, combination=(False, False, False)),
               ComplexAnswer(number=23, combination=(False, False, False)),
               ComplexAnswer(number=24, combination=(False, False, False)),
               ComplexAnswer(number=25, combination=(False, False, False))]
    results = ('Inferior', 16, 43)
    self.Test_complex.test_candidate_complex_result(
      self=self, answers=answers, results=results)

  def test_candidate_complex_case_2(self):
    answers = [ComplexAnswer(number=1, combination=(False, False, False)),
               ComplexAnswer(number=2, combination=(False, False, False)),
               ComplexAnswer(number=3, combination=(False, True, False)),
               ComplexAnswer(number=4, combination=(False, False, False)),
               ComplexAnswer(number=5, combination=(False, False, False)),
               ComplexAnswer(number=6, combination=(False, False, False)),
               ComplexAnswer(number=7, combination=(True, False, False)),
               ComplexAnswer(number=8, combination=(False, False, False)),
               ComplexAnswer(number=9, combination=(False, False, False)),
               ComplexAnswer(number=10, combination=(False, False, False)),
               ComplexAnswer(number=11, combination=(False, False, False)),
               ComplexAnswer(number=12, combination=(False, False, False)),
               ComplexAnswer(number=13, combination=(False, False, True)),
               ComplexAnswer(number=14, combination=(False, False, False)),
               ComplexAnswer(number=15, combination=(False, False, False)),
               ComplexAnswer(number=16, combination=(False, False, False)),
               ComplexAnswer(number=17, combination=(False, False, True)),
               ComplexAnswer(number=18, combination=(False, False, False)),
               ComplexAnswer(number=19, combination=(False, False, False)),
               ComplexAnswer(number=20, combination=(False, False, False)),
               ComplexAnswer(number=21, combination=(False, False, False)),
               ComplexAnswer(number=22, combination=(False, False, False)),
               ComplexAnswer(number=23, combination=(False, False, False)),
               ComplexAnswer(number=24, combination=(False, False, False)),
               ComplexAnswer(number=25, combination=(False, False, False))]
    results = ('Inferior', 17, 39)
    self.Test_complex.test_candidate_complex_result(
      self=self, answers=answers, results=results)

  def test_candidate_complex_case_3(self):
    answers = [ComplexAnswer(number=1, combination=(True, False, True)),
               ComplexAnswer(number=2, combination=(False, True, False)),
               ComplexAnswer(number=3, combination=(True, False, False)),
               ComplexAnswer(number=4, combination=(False, False, False)),
               ComplexAnswer(number=5, combination=(False, False, True)),
               ComplexAnswer(number=6, combination=(True, False, False)),
               ComplexAnswer(number=7, combination=(False, False, True)),
               ComplexAnswer(number=8, combination=(False, False, False)),
               ComplexAnswer(number=9, combination=(False, False, False)),
               ComplexAnswer(number=10, combination=(True, False, False)),
               ComplexAnswer(number=11, combination=(False, False, True)),
               ComplexAnswer(number=12, combination=(False, False, False)),
               ComplexAnswer(number=13, combination=(False, True, False)),
               ComplexAnswer(number=14, combination=(False, False, False)),
               ComplexAnswer(number=15, combination=(False, False, True)),
               ComplexAnswer(number=16, combination=(False, False, False)),
               ComplexAnswer(number=17, combination=(False, False, False)),
               ComplexAnswer(number=18, combination=(False, False, False)),
               ComplexAnswer(number=19, combination=(True, False, True)),
               ComplexAnswer(number=20, combination=(True, True, False)),
               ComplexAnswer(number=21, combination=(False, False, True)),
               ComplexAnswer(number=22, combination=(False, False, True)),
               ComplexAnswer(number=23, combination=(True, False, False)),
               ComplexAnswer(number=24, combination=(False, False, False)),
               ComplexAnswer(number=25, combination=(True, True, False))]
    results = ('Adecuado', 0, 100)
    self.Test_complex.test_candidate_complex_result(
      self=self, answers=answers, results=results)

  class Test_complex:
    @wire
    def test_candidate_complex_result(
        self, complexRecordRepository: Wired[ComplexRecordRepository],
        answers: List[ComplexAnswer],
        results: Tuple[str, int, int]):
      self.client.login(username='hunter', password='hunter')

      response = self.client.get(
        '/luci/hunter/candidate/thor@vh.la/personality_test/complex')
      self.assertRedirects(response, '/luci/hunter/candidate/thor@vh.la/')

      candidateId = CandidateId('thor@vh.la')
      complexRecord = ComplexRecord(
        candidateId=candidateId,
        answers=answers,
        start=datetime(2022, 12, 12, 12, 12, 12, tzinfo=timezone.utc),
        finish=datetime(2022, 12, 12, 12, 16, 12, tzinfo=timezone.utc))
      complexRecordRepository.Store(complexRecord)

      response = self.client.get(
        '/luci/hunter/candidate/thor@vh.la/personality_test/complex')
      complexResult = response.context['result']

      self.assertEqual(complexResult.levelResultText, results[0])
      self.assertEqual(complexResult.pointsResultText, results[1])
      self.assertEqual(complexResult.percentageResultText, results[2])

  @wire
  def test_candidate_affiliation(
      self, candidateRepository: Wired[CandidateRepository]):
    self.client.login(username='hunter', password='hunter')

    candidateId = CandidateId(email='loki@asgard.com')
    self.assertRaises(
      CandidateNotFoundError,
      lambda: candidateRepository.Find(candidateId))

    data = {
      'name': 'loki',
      'email': 'loki@asgard.com',
      'gender': 0
    }

    response = self.client.post('/luci/hunter/affiliation/', data)

    self.assertRedirects(response, '/luci/hunter/dashboard/')

    candidate = candidateRepository.Find(candidateId)

    self.assertEqual(candidate.name, 'loki')
    self.assertEqual(candidate.email, 'loki@asgard.com')
    self.assertEqual(candidate.gender, 0)
