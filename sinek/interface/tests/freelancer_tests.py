from datetime import datetime, timezone
from typing import NamedTuple
from unittest import skip

from django.test import Client, TestCase
from neom.core.ioc import AutoWire

from sinek.application.account import UserRoleService
from sinek.domain.model.freelancer import *
from sinek.domain.model.freelancer import (
  CV, CVRepository, Email, File, FileRepository, Freelancer,
  FreelancerRepository, GoogleId, Network, Tag, Url)
from sinek.infrastructure.persistence.orm.models import \
  FreelancerSkill as FreelancerSkillORM
from sinek.infrastructure.persistence.orm.models import Upload as ORMUpload


@AutoWire
class FreelancerTestCase(TestCase):

  userRoleService: UserRoleService
  freelancerRepository: FreelancerRepository
  cvRepository: CVRepository
  fileRepository: FileRepository

  def setUp(self):
    networks = [
      Network(Url('http://my.github.com/test')),
      Network(Url('http://my.linkedin.com/test'))
    ]
    businesses = [Tag('Cementerios'), Tag('Cementaras')]
    projects = [Tag('ERP'), Tag('Drupal')]
    condition = ConditionBuilder().AsHalfTime(5, HalfTime.Experience.HIGH).Build()
    residence = Residence('Lima', 'Peru')
    phone = Phone(Phone.CountryCode.PER, '12345')
    
    roleInterests = [Tag(name='Backend')]
    acceptanceAvailability = AcceptanceAvailability(
      wouldChangeCountry=False,
      wouldChangeCity=True,
      interviewAvailability=True,
      jobSwitchTime=AcceptanceAvailability.JobSwitchTime.GT_12M)
    englishProficiency = EnglishProficiency(
      writing=EnglishProficiency.EnglishSkill.ADVANCED,
      speaking=EnglishProficiency.EnglishSkill.BEGINNER)
    worklifePreferences = [Tag(name='Que el trabajo no interfiera para nada en mi vida actual.'),
      Tag(name='Tener la oportunidad de conocer nuevas personas.'),
      Tag(name='Recibir constate feedback para saber si voy por buen camino.'),
    ]
    jobPreferences = [Tag(name='Donde puedo ser creativo y autónomo.'),
      Tag(name='Estructurados y sistemáticos.'),
    ]
    
    freelancer = Freelancer(email='free@lancer.dev',
                            name='Free Lancer',
                            phone=phone,
                            condition=condition,
                            residence=residence,
                            networks=networks,
                            businesses=businesses,
                            projects=projects,
                            roleInterests=roleInterests,
                            acceptanceAvailability=acceptanceAvailability,
                            englishProficiency=englishProficiency,
                            worklifePreferences=worklifePreferences,
                            jobPreferences=jobPreferences,
                            isOnboarded=True)

    self.freelancerRepository.Store(freelancer)
    self.userRoleService.CreateUser(freelancer, '123')

    # uploads

    cv = CV(
      googleId=GoogleId(id=''),
      freelancer=freelancer,
      name='cv.pdf',
      created=datetime.now(timezone.utc),
      blob=b'')

    self.cvRepository.Store(cv)

    files = [
      File(googleId='', freelancer=freelancer, name='pf1.pdf', created=datetime.now(
        timezone.utc), blob=b''),
      File(googleId='', freelancer=freelancer, name='demo1.txt', created=datetime.now(
        timezone.utc), blob=b''),
      File(googleId='', freelancer=freelancer, name='demo2.txt', created=datetime.now(
        timezone.utc), blob=b''),
    ]

    for file in files:
      self.fileRepository.Store(file)

    self.client = Client()

  # TODO: reutilizar estos Tests pero para la versión actual de RC
  """
  def test_show_profile(self):
    self.client.login(username='free@lancer.dev', password='123')
    response = self.client.get('/luci/freelancer/profile/')

    va = response.context['profile']  # view adapter

    self.assertEqual(va.email, 'free@lancer.dev')
    self.assertEqual(va.name, 'Free Lancer')
    self.assertEqual(va.phone.number, '12345')

    self.assertListEqual(va.networks, [
      ('github', 'http://my.github.com/test'),
      ('linkedin', 'http://my.linkedin.com/test')])

    # TODO: Aserto con ListEqual sale error por orden den los elementos
    self.assertCountEqual(va.businesses, ['Cementerios', 'Cementaras'])
    self.assertCountEqual(va.projects, ['Drupal', 'ERP'])

    self.assertEqual(len(va.attachCVs), 1)
    self.assertIn('cv.pdf', [cv.name for cv in va.attachCVs])
    self.assertCountEqual(
      [f.name for f in va.attachFiles],
      ['pf1.pdf', 'demo1.txt', 'demo2.txt'])

  @skip('/luci/freelancer/profile/personal/ must be removed since unused')
  def test_update_personal(self):
    self.client.login(username='free@lancer.dev', password='123')

    data = {
      'name': 'New Dummy',
      'phone': '999 000 888',
      'location': 'Lima',
      'country': 'Perú',
      'condition': '1',
      'countryCode': 'PER'
    }

    response = self.client.post('/luci/freelancer/profile/personal/', data)

    self.assertRedirects(response, '/luci/freelancer/profile/')

    freelancer = self.freelancerRepository.Find(Email('free@lancer.dev'))

    self.assertEqual(freelancer.name, 'New Dummy')
    self.assertEqual(freelancer.phone, '999 000 888')

  def test_update_network(self):
    self.client.login(username='free@lancer.dev', password='123')

    data = {
      'network': str(Network.Kind.GITHUB.value),
      'url': 'https://free.github.com/lancer'
    }

    response = self.client.post('/luci/freelancer/profile/network/', data)

    self.assertRedirects(response, '/luci/freelancer/profile/')

    freelancer = self.freelancerRepository.Find(Email('free@lancer.dev'))

    self.assertListEqual(freelancer.networks, [
      Network(Url('http://my.github.com/test')),
      Network(Url('http://my.linkedin.com/test')),
      Network(Url('https://free.github.com/lancer'))
    ])

  def test_update_businesses(self):
    self.client.login(username='free@lancer.dev', password='123')

    data = {
      'name': 'Funerarias'
    }

    response = self.client.post('/luci/freelancer/profile/business/', data)

    self.assertRedirects(response, '/luci/freelancer/profile/')

    freelancer = self.freelancerRepository.Find(Email('free@lancer.dev'))

    self.assertSetEqual(
      freelancer.businesses, {
        Tag('Cementerios'), Tag('Cementaras'), Tag('Funerarias')})

  def test_update_projects(self):
    self.client.login(username='free@lancer.dev', password='123')

    data = {
      'name': 'CMM'
    }

    response = self.client.post('/luci/freelancer/profile/project/', data)

    self.assertRedirects(response, '/luci/freelancer/profile/')

    freelancer = self.freelancerRepository.Find(Email('free@lancer.dev'))

    self.assertSetEqual(
      freelancer.projects, {
        Tag('ERP'), Tag('Drupal'), Tag('CMM')})

  """
