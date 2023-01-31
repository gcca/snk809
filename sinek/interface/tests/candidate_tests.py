from datetime import datetime, timezone

from django.test import Client, TestCase
from neom.core.ioc import Wired, wire

from sinek.application.account import UserRoleService
from sinek.domain.model.candidate import (Candidate, CandidateId,
                                          CandidateRepository)
from sinek.domain.model.personality_test.anchor import (
  AnchorAnswer, AnchorRecord, AnchorRecordNotFoundError,
  AnchorRecordRepository)
from sinek.domain.model.personality_test.complex import (
  ComplexAnswer, ComplexRecord, ComplexRecordNotFoundError,
  ComplexRecordRepository)
from sinek.domain.model.personality_test.disc import (DiscAnswer, DiscRecord,
                                                      DiscRecordNotFoundError,
                                                      DiscRecordRepository)
from sinek.domain.model.personality_test.tmms24 import (
  TMMS24Answer, TMMS24Record, TMMS24RecordNotFoundError,
  TMMS24RecordRepository)


class CandidateTestCase(TestCase):

  @wire
  def setUp(
      self,
      candidateRepository: Wired[CandidateRepository],
      userRoleService: Wired[UserRoleService]):
    self.client = Client()

    candidateId = CandidateId('loki@vh.la')
    candidate = Candidate(
      name='loki',
      candidateId=candidateId,
      gender=Candidate.Gender.MALE)
    candidateRepository.Store(candidate)

    userRoleService.CreateUser(candidate, '123')

  def test_dummy_dashboard(self):
    self.client.login(username='loki@vh.la', password='123')
    response = self.client.get('/luci/candidate/dashboard/')

    candidateChecklist = response.context['candidateView']

    self.assertEqual(candidateChecklist.candidateName, 'loki')
    self.assertEqual(candidateChecklist.candidateEmail, 'loki@vh.la')
    self.assertEqual(candidateChecklist.discCompleted, False)
    self.assertEqual(candidateChecklist.tmms24Completed, False)

  @wire
  def test_record_disc(
      self,
      discRecordRepository: Wired[DiscRecordRepository]):
    self.client.login(username='loki@vh.la', password='123')

    candidateId = CandidateId('loki@vh.la')
    self.assertRaises(
      DiscRecordNotFoundError,
      lambda: discRecordRepository.Find(candidateId))

    data = {
      'answer_1_minus': '1',
      'answer_1_plus': '1',
      'answer_2_minus': '1',
      'answer_2_plus': '1',
      'answer_3_minus': '1',
      'answer_3_plus ': '1',
      'answer_4_minus': '1',
      'answer_4_plus ': '1',
      'answer_5_minus': '1',
      'answer_5_plus ': '1',
      'answer_6_minus': '1',
      'answer_6_plus ': '1',
      'answer_7_minus': '1',
      'answer_7_plus ': '1',
      'answer_8_minus': '1',
      'answer_8_plus ': '1',
      'answer_9_minus': '1',
      'answer_9_plus ': '1',
      'answer_10_minus': '1',
      'answer_10_plus': '1',
      'answer_11_minus': '1',
      'answer_11_plus': '1',
      'answer_12_minus': '1',
      'answer_12_plus': '1',
      'answer_13_minus': '1',
      'answer_13_plus': '1',
      'answer_14_minus': '1',
      'answer_14_plus': '1',
      'answer_15_minus': '1',
      'answer_15_plus': '1',
      'answer_16_minus': '1',
      'answer_16_plus': '1',
      'answer_17_minus': '1',
      'answer_17_plus': '1',
      'answer_18_minus': '1',
      'answer_18_plus': '1',
      'answer_19_minus': '1',
      'answer_19_plus': '1',
      'answer_20_minus': '1',
      'answer_20_plus': '1',
      'answer_21_minus': '1',
      'answer_21_plus': '1',
      'answer_22_minus': '1',
      'answer_22_plus': '1',
      'answer_23_minus': '1',
      'answer_23_plus': '1',
      'answer_24_minus': '1',
      'answer_24_plus': '1',
    }

    response = self.client.post('/luci/candidate/test/1/', data)

    record = discRecordRepository.Find(candidateId)
    self.assertIsNotNone(record.answers)

  @wire
  def test_is_disc_completed(
      self,
      discRecordRepository: Wired[DiscRecordRepository]):

    answers = [DiscAnswer(number=i, plus=1, minus=2) for i in range(1, 25)]
    candidateId = CandidateId('loki@vh.la')
    discRecord = DiscRecord(candidateId=candidateId, answers=answers)

    discRecordRepository.Store(discRecord)

    self.client.login(username='loki@vh.la', password='123')

    response = self.client.get('/luci/candidate/test/1/')
    self.assertRedirects(response, '/luci/candidate/test/success/')

  @wire
  def test_record_tmms24(
      self,
      tmms24RecordRepository: Wired[TMMS24RecordRepository]):
    self.client.login(username='loki@vh.la', password='123')

    candidateId = CandidateId('loki@vh.la')
    self.assertRaises(
      TMMS24RecordNotFoundError,
      lambda: tmms24RecordRepository.Find(candidateId)
    )

    data = {
      'answer_1': '1',
      'answer_2': '1',
      'answer_3': '1',
      'answer_4': '1',
      'answer_5': '1',
      'answer_6': '1',
      'answer_7': '1',
      'answer_8': '1',
      'answer_9': '1',
      'answer_10': '1',
      'answer_11': '1',
      'answer_12': '1',
      'answer_13': '1',
      'answer_14': '1',
      'answer_15': '1',
      'answer_16': '1',
      'answer_17': '1',
      'answer_18': '1',
      'answer_19': '1',
      'answer_20': '1',
      'answer_21': '1',
      'answer_22': '1',
      'answer_23': '1',
      'answer_24': '1',
    }

    response = self.client.post('/luci/candidate/test/2/', data)

    record = tmms24RecordRepository.Find(candidateId)
    self.assertIsNotNone(record.answers)

  @wire
  def test_record_anchor(
      self,
      anchorRecordRepository: Wired[AnchorRecordRepository]):
    self.client.login(username='loki@vh.la', password='123')

    candidateId = CandidateId('loki@vh.la')
    self.assertRaises(
      AnchorRecordNotFoundError,
      lambda: anchorRecordRepository.Find(candidateId))

    data = {
      'answer_1': '1',
      'answer_2': '1',
      'answer_3': '1',
      'answer_4': '1',
      'answer_5': '1',
      'answer_6': '1',
      'answer_7': '1',
      'answer_8': '1',
      'answer_9': '1',
      'answer_10': '1',
      'answer_11': '1',
      'answer_12': '1',
      'answer_13': '1',
      'answer_14': '1',
      'answer_15': '1',
      'answer_16': '1',
      'answer_17': '1',
      'answer_18': '1',
      'answer_19': '1',
      'answer_20': '1',
      'answer_21': '1',
      'answer_22': '1',
      'answer_23': '1',
      'answer_24': '1',
      'answer_25': '1',
      'answer_26': '1',
      'answer_27': '1',
      'answer_28': '1',
      'answer_29': '1',
      'answer_30': '1',
      'answer_31': '1',
      'answer_32': '1',
      'answer_33': '1',
      'answer_34': '1',
      'answer_35': '1',
      'answer_36': '1',
      'answer_37': '1',
      'answer_38': '1',
      'answer_39': '1',
      'answer_40': '1',
      'favourite_1': '1',
      'favourite_2': '1',
      'favourite_3': '1',
    }

    response = self.client.post('/luci/candidate/test/3/', data)

    record = anchorRecordRepository.Find(candidateId)
    self.assertIsNotNone(record)

  @wire
  def test_record_complex(
      self,
      complexRecordRepository: Wired[ComplexRecordRepository]):
    self.client.login(username='loki@vh.la', password='123')

    candidateId = CandidateId('loki@vh.la')
    self.assertRaises(
      ComplexRecordNotFoundError,
      lambda: complexRecordRepository.Find(candidateId))

    data = {
      'answer_1_a': True,
      'answer_1_b': True,
      'answer_1_c': True,
      'answer_2_a': True,
      'answer_2_b': True,
      'answer_2_c': True,
      'answer_3_a': True,
      'answer_3_b': True,
      'answer_3_c': True,
      'answer_4_a': True,
      'answer_4_b': True,
      'answer_4_c': True,
      'answer_5_a': True,
      'answer_5_b': True,
      'answer_5_c': True,
      'answer_6_a': True,
      'answer_6_b': True,
      'answer_6_c': True,
      'answer_7_a': True,
      'answer_7_b': True,
      'answer_7_c': True,
      'answer_8_a': True,
      'answer_8_b': True,
      'answer_8_c': True,
      'answer_9_a': True,
      'answer_9_b': True,
      'answer_9_c': True,
      'answer_10_a': True,
      'answer_10_b': True,
      'answer_10_c': True,
      'answer_11_a': True,
      'answer_11_b': True,
      'answer_11_c': True,
      'answer_12_a': True,
      'answer_12_b': True,
      'answer_12_c': True,
      'answer_13_a': True,
      'answer_13_b': True,
      'answer_13_c': True,
      'answer_14_a': True,
      'answer_14_b': True,
      'answer_14_c': True,
      'answer_15_a': True,
      'answer_15_b': True,
      'answer_15_c': True,
      'answer_16_a': True,
      'answer_16_b': True,
      'answer_16_c': True,
      'answer_17_a': True,
      'answer_17_b': True,
      'answer_17_c': True,
      'answer_18_a': True,
      'answer_18_b': True,
      'answer_18_c': True,
      'answer_19_a': True,
      'answer_19_b': True,
      'answer_19_c': True,
      'answer_20_a': True,
      'answer_20_b': True,
      'answer_20_c': True,
      'answer_21_a': True,
      'answer_21_b': True,
      'answer_21_c': True,
      'answer_22_a': True,
      'answer_22_b': True,
      'answer_22_c': True,
      'answer_23_a': True,
      'answer_23_b': True,
      'answer_23_c': True,
      'answer_24_a': True,
      'answer_24_b': True,
      'answer_24_c': True,
      'answer_25_a': True,
      'answer_25_b': True,
      'answer_25_c': True,
    }

    self.client.get('/luci/candidate/test/4/')
    response = self.client.post('/luci/candidate/test/4/', data)

    record = complexRecordRepository.Find(candidateId)
    self.assertIsNotNone(record)

  @wire
  def test_is_complex_completed(
      self, complexRecordRepository: Wired[ComplexRecordRepository]):

    answers = [
      ComplexAnswer(
        number=i,
        combination=(
          True,
          True,
          True)) for i in range(
        1,
        26)]
    candidateId = CandidateId('loki@vh.la')
    complexRecord = ComplexRecord(
      candidateId=candidateId,
      answers=answers,
      start=datetime(2022, 12, 13, 12, 12, 12, tzinfo=timezone.utc),
      finish=datetime(2022, 12, 13, 12, 15, 12, tzinfo=timezone.utc))

    complexRecordRepository.Store(complexRecord)

    self.client.login(username='loki@vh.la', password='123')

    response = self.client.get('/luci/candidate/test/4/')

    self.assertRedirects(response, '/luci/candidate/test/success/')

  def test_not_completed_complex(self):
    self.client.login(username='loki@vh.la', password='123')
    response = self.client.get('/luci/candidate/test/4/')

    complexQuestions = response.context['questions']

    self.assertEqual(len(complexQuestions), 25)

  @wire
  def test_is_tmms24_completed(
      self, tmms24RecordRepository: Wired[TMMS24RecordRepository]):

    answers = [TMMS24Answer(number=i, score=3) for i in range(1, 25)]

    candidateId = CandidateId('loki@vh.la')
    tmms24Record = TMMS24Record(candidateId=candidateId, answers=answers)

    tmms24RecordRepository.Store(tmms24Record)

    self.client.login(username='loki@vh.la', password='123')

    response = self.client.get('/luci/candidate/test/2/')
    self.assertRedirects(response, '/luci/candidate/test/success/')

  @wire
  def test_is_anchor_completed(
      self, anchorRecordRepository: Wired[AnchorRecordRepository]):

    answers = [AnchorAnswer(number=i, score=3) for i in range(1, 41)]
    relevants = (1, 2, 3)
    candidateId = CandidateId('loki@vh.la')
    anchorRecord = AnchorRecord(
      candidateId=candidateId,
      answers=answers,
      relevants=relevants)

    anchorRecordRepository.Store(anchorRecord)

    self.client.login(username='loki@vh.la', password='123')

    response = self.client.get('/luci/candidate/test/3/')

    self.assertRedirects(response, '/luci/candidate/test/success/')

  def test_not_completed_disc(self):
    self.client.login(username='loki@vh.la', password='123')
    response = self.client.get('/luci/candidate/test/1/')

    discQuestions = response.context['discQuestions']

    self.assertEqual(len(discQuestions), 24)
