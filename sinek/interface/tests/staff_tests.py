from django.test import Client, TestCase
from neom.core.ioc import Wired, wire

from devtools.populators.users import populate as PopulateUsers
from sinek.domain.model.hunter import Hunter, HunterRepository


class StaffTestCase(TestCase):

  def setUp(self):
    PopulateUsers()
    self.client = Client()

  @wire
  def test_dashboard_disallowed(self):
    response = self.client.get('/luci/staff/dashboard/', follow=True)
    self.assertRedirects(response, '/luci/account/signin/')

  @wire
  def test_dashboard_allowed(self):
    self.client.login(username='staff', password='staff')
    response = self.client.get('/luci/staff/dashboard/')
    self.assertEqual(response.status_code, 200)

  @wire
  def test_new_hunter(self, hunterRepository: Wired[HunterRepository]):
    self.client.login(username='staff', password='staff')
    data = {
      'username': 'dummy-usr',
      'password': 'dummy-pwd',
      'name': 'dummy foo'
    }
    response = self.client.post('/luci/staff/new-hunter/', data)

    hunter = hunterRepository.Find('dummy foo')

    self.assertEqual(hunter.name, 'dummy foo')
