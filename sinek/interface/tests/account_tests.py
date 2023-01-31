from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from neom.core.ioc import AutoWire, Wired, wire
from neom.ddd.staff import Email

from sinek.application.account import UserRoleService
from sinek.domain.model.accountmanager import (AccountManager,
                                               AccountManagerRepository)
from sinek.domain.model.candidate import (Candidate, CandidateId,
                                          CandidateNotFoundError,
                                          CandidateRepository)
from sinek.domain.model.hunter import Hunter, HunterRepository

# TODO: Actualizar este test con el nuevo flujo de freelancer signin


class AccountTestCase(TestCase):
  """
  def setUp(self):
    self.client = Client()

  def test_new_google_signin_with_error(self):
    response = self.client.get('/luci/account/google-login/', {
      'code': 'dummy-code',
      'error': 'dummy-error'
    })
    self.assertRedirects(response, '/luci/account/signin/')

  def test_new_google_signin_without_code(self):
    response = self.client.get('/luci/account/google-login/')
    self.assertRedirects(response, '/luci/account/signin/')

  @wire
  @patch('requests.post')
  @patch('requests.get')
  def test_new_google_signin(
      self,
      getMock: MagicMock,
      postMock: MagicMock,
      candidateRepository: Wired[CandidateRepository]):
    responseTokenMock = MagicMock()
    responseTokenMock.ok = True
    responseTokenMock.json.return_value.get.return_value = 'dummy-token'
    postMock.return_value = responseTokenMock

    responseEmailMock = MagicMock()
    responseEmailMock.json.return_value = {'email': 'dummy@mail.com'}
    getMock.return_value = responseEmailMock

    response = self.client.get('/luci/account/google-login/', {
      'code': 'dummy-code',
    })
    self.assertRedirects(response, '/luci/account/google-candidate/')

    postMock.assert_called_once()
    getMock.assert_called_once()

    self.assertEquals(postMock.call_args.kwargs['data']['code'], 'dummy-code')

    responseTokenMock.json.assert_called_once()
    responseTokenMock.json.return_value.get.assert_called_once_with(
      'access_token')

    self.assertEquals(getMock.call_args.kwargs,
                      {'params': {'access_token': 'dummy-token'}})

    self.assertRaises(
      CandidateNotFoundError,
      lambda: candidateRepository.Find(
        CandidateId('dummy@mail.com')))
  """


@AutoWire
class UserRoleTestCase(TestCase):

  userRoleService: UserRoleService

  def setUp(self):
    self.client = Client()

  @wire
  def test_hunter_signin(self, hunterRepository: Wired[HunterRepository]):
    hunter = Hunter(name='foo')
    hunterRepository.Store(hunter)
    self.userRoleService.CreateUser(hunter, 'bar')

    data = {'username': 'foo', 'password': 'bar'}
    response = self.client.post('/luci/account/signin/', data)
    self.assertRedirects(response, '/luci/hunter/dashboard/')

  @wire
  def test_candidate_signin(
      self,
      candidateRepository: Wired[CandidateRepository]):
    candidate = Candidate(
      candidateId=CandidateId('foo@mail.com'),
      name='foo',
      gender=Candidate.Gender.MALE)
    candidateRepository.Store(candidate)
    self.userRoleService.CreateUser(candidate, 'bar')

    data = {'username': 'foo@mail.com', 'password': 'bar'}
    response = self.client.post('/luci/account/signin/', data)
    self.assertRedirects(response, '/luci/candidate/dashboard/')

  @wire
  def test_accountmanager_signin(
      self, accountManagerRepository: Wired[AccountManagerRepository]):
    accountManager = AccountManager(
      name='Manager', email=Email('manager@neo.com'))
    accountManagerRepository.Store(accountManager)
    self.userRoleService.CreateUser(accountManager, 'bar')

    data = {'username': 'manager@neo.com', 'password': 'bar'}
    response = self.client.post('/luci/account/signin/', data)
    self.assertRedirects(
      response,
      '/luci/accountmanager/dashboard-freelancer/')
