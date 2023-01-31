from datetime import datetime, timezone

from django.test import TestCase

from sinek.domain.model.candidate import CandidateId
from sinek.domain.model.freelancer import (
  CV,
  AcceptanceAvailability,
  Condition,
  ConditionBuilder,
  Email,
  EnglishProficiency,
  File,
  Freelancer,
  FreelancerNotFoundError,
  FullTime,
  HalfTime,
  Network,
  Phone,
  Residence,
  Tag,
  Url)
from sinek.domain.model.personality_test.complex import (
  ComplexAnswer, ComplexRecord, ComplexRecordNotFoundError)
from sinek.infrastructure.persistence.orm.complexrecord import \
  ComplexRecordRepositoryORM
from sinek.infrastructure.persistence.orm.freelancer import (
  CVRepositoryORM, FileRepositoryORM, FreelancerRepositoryORM)
from sinek.infrastructure.persistence.orm.models import \
  CandidateComplexAnswers as ORMCandidateComplexAnswers
from sinek.infrastructure.persistence.orm.models import FreelancerRoleTag as ORMFreelancerRoleTag
from sinek.infrastructure.persistence.orm.models import \
  CandidateComplexRecord as ORMCandidateComplexRecord
from sinek.infrastructure.persistence.orm.models import \
  Freelancer as ORMFreelancer
from sinek.infrastructure.persistence.orm.models import \
  FreelancerBusinessTag as ORMFreelancerBusinessTag
from sinek.infrastructure.persistence.orm.models import \
  FreelancerNetwork as ORMFreelancerNetwork
from sinek.infrastructure.persistence.orm.models import \
  FreelancerProjectTag as ORMFreelancerProjectTag
from sinek.infrastructure.persistence.orm.models import \
  FreelancerJobTag as ORMFreelancerJobTag
from sinek.infrastructure.persistence.orm.models import \
  FreelancerWorklifeTag as ORMFreelancerWorklifeTag
from sinek.infrastructure.persistence.orm.models import Upload as ORMUpload
from sinek.infrastructure.persistence.orm.initiative import InitiativeGoogleSheetRepositoryORM, Initiative, InitiativeCode


class FreelancerRepositoryTestCase(TestCase):

  def setUp(self):
    self.repository = FreelancerRepositoryORM()

  def test_unsuccess_find(self):
    self.assertRaises(
      FreelancerNotFoundError,
      lambda: self.repository.Find('yo@neoma.das'))

  def test_success_find(self):
    ormFreelancer = ORMFreelancer(
      condition=ORMFreelancer.ConditionChoices.FULLTIME,
      country='Perú',
      countryCode=Phone.CountryCode.PER,
      location='Lima',
      email='yo@neoma.das',
      name='yo',
      phone=12345,
      wouldChangeCountry=False,
      wouldChangeCity=False,
      interviewAvailability=True,
      isOnboarded=False,)
    ormFreelancer.save()

    ormFreelancerBusinessTags = [
      ORMFreelancerBusinessTag(name='business 1', freelancer=ormFreelancer),
      ORMFreelancerBusinessTag(name='business 2', freelancer=ormFreelancer),
      ORMFreelancerBusinessTag(name='business 3', freelancer=ormFreelancer)]
    ormFreelancer.businessTags.bulk_create(ormFreelancerBusinessTags)

    ormFreelancerProjectTags = [
      ORMFreelancerProjectTag(name='proj 1', freelancer=ormFreelancer),
      ORMFreelancerProjectTag(name='proj 2', freelancer=ormFreelancer)
    ]
    ormFreelancer.projectTags.bulk_create(ormFreelancerProjectTags)

    ormFreelancerNetworks = [
      ORMFreelancerNetwork(freelancer=ormFreelancer, url='foo.com'),
      ORMFreelancerNetwork(freelancer=ormFreelancer, url='bar.com')]
    ormFreelancer.links.bulk_create(ormFreelancerNetworks)

    ormFreelancerRoleTags = [
      ORMFreelancerRoleTag(name='Backend', freelancer=ormFreelancer),
      ORMFreelancerRoleTag(name='Devops', freelancer=ormFreelancer)]
    ormFreelancer.roleInterests.bulk_create(ormFreelancerRoleTags)

    ormFreelancerJobTags = [
      ORMFreelancerJobTag(
        name='Donde puedo ser creativo y autónomo.',
        freelancer=ormFreelancer),
      ORMFreelancerJobTag(
        name='Estructurados y sistemáticos.',
        freelancer=ormFreelancer),
    ]
    ormFreelancer.jobPreferences.bulk_create(ormFreelancerJobTags)

    ormFreelancerWorklifeTags = [
      ORMFreelancerWorklifeTag(
        name='Ser reconocido por la calidad de mi trabajo.',
        freelancer=ormFreelancer),
      ORMFreelancerWorklifeTag(
        name='Transparencia total.',
        freelancer=ormFreelancer),
    ]
    ormFreelancer.worklifePreferences.bulk_create(ormFreelancerWorklifeTags)

    # test

    freelancer = self.repository.Find('yo@neoma.das')

    self.assertIsInstance(freelancer.condition, FullTime)
    self.assertEqual(freelancer.residence.country, 'Perú')
    self.assertEqual(freelancer.residence.location, 'Lima')
    self.assertEqual(freelancer.email, Email('yo@neoma.das'))
    self.assertEqual(freelancer.name, 'yo')
    self.assertEqual(freelancer.phone.number, '12345')
    self.assertEqual(freelancer.acceptanceAvailability.wouldChangeCountry, False)
    self.assertEqual(freelancer.acceptanceAvailability.wouldChangeCity, False)
    self.assertEqual(freelancer.acceptanceAvailability.interviewAvailability, True)
    self.assertListEqual(freelancer.networks, [
      Network(Url('foo.com')), Network(Url('bar.com'))])
    self.assertSetEqual(
      freelancer.businesses, {
        Tag('business 1'), Tag('business 2'), Tag('business 3')})
    self.assertSetEqual(freelancer.projects, {Tag('proj 1'), Tag('proj 2')})
    self.assertSetEqual(freelancer.jobPreferences, {
      Tag('Donde puedo ser creativo y autónomo.'),
      Tag('Estructurados y sistemáticos.')
    })
    self.assertSetEqual(freelancer.worklifePreferences, {
      Tag('Ser reconocido por la calidad de mi trabajo.'),
      Tag('Transparencia total.')
    })
    self.assertSetEqual(freelancer.roleInterests, {
      Tag('Backend'), Tag('Devops')
    })

  def test_store_for_create(self):
    businesses = [Tag(name='b 1'), Tag(name='b 2')]
    projects = [Tag(name='p 1')]
    networks = [Network(Url('foo.com')), Network(Url('bar.com'))]
    condition = ConditionBuilder().AsHalfTime(5, HalfTime.Experience.HIGH).Build()
    residence = Residence('Lima', 'Peru')
    roleInterests = [Tag(name='Backend')]
    worklifePreferences = [Tag(name='Que el trabajo no interfiera para nada en mi vida actual.'),
      Tag(name='Tener la oportunidad de conocer nuevas personas.'),
      Tag(name='Recibir constate feedback para saber si voy por buen camino.'),
    ]
    jobPreferences = [Tag(name='Donde puedo ser creativo y autónomo.'),
      Tag(name='Estructurados y sistemáticos.'),
    ]
    acceptanceAvailability = AcceptanceAvailability(
      wouldChangeCountry=False,
      wouldChangeCity=True,
      interviewAvailability=True,
      jobSwitchTime=AcceptanceAvailability.JobSwitchTime.GT_12M)
    englishProficiency = EnglishProficiency(
      writing=EnglishProficiency.EnglishSkill.ADVANCED,
      speaking=EnglishProficiency.EnglishSkill.BEGINNER)

    phone = Phone(Phone.CountryCode.PER, '12345')

    freelancer = Freelancer(
      email=Email('yo@neoma.das'),
      name='yo',
      phone=phone,
      businesses=businesses,
      projects=projects,
      networks=networks,
      condition=condition,
      residence=residence,
      jobPreferences=jobPreferences,
      worklifePreferences=worklifePreferences,
      roleInterests=roleInterests,
      acceptanceAvailability=acceptanceAvailability,
      englishProficiency=englishProficiency,
      isOnboarded=False,)

    self.repository.Store(freelancer)

    # test

    ormFreelancer = ORMFreelancer.objects.get(email='yo@neoma.das')

    self.assertEqual(ormFreelancer.name, 'yo')
    self.assertEqual(ormFreelancer.phone, '12345')
    self.assertIsNone(ormFreelancer.minimum)
    self.assertIsNone(ormFreelancer.maxIncome)
    self.assertListEqual(
      [t.name for t in ormFreelancer.businessTags.all()], ['b 1', 'b 2'])
    self.assertListEqual(
      [t.name for t in ormFreelancer.projectTags.all()], ['p 1'])
    self.assertListEqual(
      [l.url for l in ormFreelancer.links.all()],
      ['foo.com', 'bar.com'])

    # TODO test_store_for_update  check ORMxTag was clean


class UploadRepositoryTestCase(TestCase):

  def setUp(self):
    self.cvRepository = CVRepositoryORM()
    self.fileRepository = FileRepositoryORM()

  def test_find(self):
    businesses = [Tag(name='b 1'), Tag(name='b 2')]
    projects = [Tag(name='p 1')]
    networks = []
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


    freelancer = Freelancer(
      condition=condition,
      residence=residence,
      email=Email('yo@neoma.das'),
      name='yo',
      phone=phone,
      businesses=businesses,
      projects=projects,
      networks=networks,
      roleInterests=roleInterests,
      acceptanceAvailability=acceptanceAvailability,
      englishProficiency=englishProficiency,
      worklifePreferences=worklifePreferences,
      jobPreferences=jobPreferences,
      isOnboarded=False,)

    FreelancerRepositoryORM().Store(freelancer)

    ormFreelancer = ORMFreelancer.objects.get(email='yo@neoma.das')

    # binary

    from io import SEEK_SET, StringIO

    stringIo = StringIO()
    stringIo.write('¡Hola mundo!')
    stringIo.seek(0, SEEK_SET)

    # TODO: Use another KIND
    ormUpload = ORMUpload(
      name='cv.txt',
      kind=1,
      created=datetime.now(timezone.utc),
      binary=stringIo.read().encode(),
      freelancer=ormFreelancer)
    ormUpload.save()

    ormUpload = ORMUpload(
      name='hello.txt',
      kind=0,
      created=datetime.now(timezone.utc),
      binary=stringIo.read().encode(),
      freelancer=ormFreelancer)
    ormUpload.save()

    # test
    cv = self.cvRepository.Find(freelancer)
    self.assertEqual(cv.blob.decode(), '¡Hola mundo!')
    # TODO: validate freelancer identity using repository

  def test_store(self):
    from io import SEEK_SET, StringIO

    stringIo = StringIO()
    stringIo.write('¡Hola mundo!')
    stringIo.seek(0, SEEK_SET)

    # TODO: FALTA TODO


class IniciativeRepositoryTestCase(TestCase):

  def setUp(self):
    self.initiativeRepository = InitiativeGoogleSheetRepositoryORM()

  def test_get_all(self):
    self.initiativeRepository.All()
    initiativeCode = InitiativeCode('NEOMD-MYC-PE-GRJJC-INI-22018')
    initiativeFounded = self.initiativeRepository.Find(initiativeCode)

    initiativeFounded.code = InitiativeCode('PRUEBA')
    print(self.initiativeRepository.Store(initiativeFounded))


class FreelancerUploadIntegrationTestCase(TestCase):

  def setUp(self):
    self.freelancerRepository = FreelancerRepositoryORM()
    #self.uploadRepository = UploadRepositoryORM()

  def test_get_labels(self):
    pass
    # freelance = Freelancer(...)  # sin uploads

    # uploads = [Upload(name='hola.txt'), Upload(...)]
    # for upload in uploads:
    # self.uploadRepository.Store(upload)

    # # test

    # freelance = self.freelancerRepository.Find(...)

    # self.assertEqual(freelance.uploadLabels[0].name, 'hola.txt')


class ComplexRecordRepositoryTestCase(TestCase):

  def setUp(self):
    self.repository = ComplexRecordRepositoryORM()

  def test_unsuccess_find(self):
    self.assertRaises(
      ComplexRecordNotFoundError,
      lambda: self.repository.Find(
        CandidateId('yo@neoma.das')))

  def test_success_find(self):
    start = datetime(2022, 12, 12, 20, 10, 10, tzinfo=timezone.utc)
    finish = datetime(2022, 12, 12, 20, 13, 10, tzinfo=timezone.utc)

    ormCandidateComplexRecord = ORMCandidateComplexRecord(
      candidateId='yo@neoma.das', start=start, finish=finish)
    ormCandidateComplexRecord.save()

    ORMCandidateComplexAnswers.objects.create(
      complexRecord=ormCandidateComplexRecord,
      number=1,
      option_a=True,
      option_b=False,
      option_c=False)
    ORMCandidateComplexAnswers.objects.create(
      complexRecord=ormCandidateComplexRecord,
      number=2,
      option_a=True,
      option_b=False,
      option_c=False)

    complexRecord = self.repository.Find(CandidateId('yo@neoma.das'))

    self.assertEqual(str(complexRecord.candidateId), 'yo@neoma.das')
    self.assertEqual(complexRecord.start, datetime(
      2022, 12, 12, 20, 10, 10, tzinfo=timezone.utc))
    self.assertEqual(complexRecord.finish, datetime(
      2022, 12, 12, 20, 13, 10, tzinfo=timezone.utc))
    self.assertEqual(len(complexRecord.answers), 2)

  def test_store_for_create(self):
    self.StoreDummyRecord()

    ormRecord = ORMCandidateComplexRecord.objects.get(
      candidateId=CandidateId('yo@neoma.das'))

    expectedStart = datetime(2022, 12, 12, 12, 12, 12, tzinfo=timezone.utc)
    expectedFinish = datetime(2022, 12, 12, 12, 15, 12, tzinfo=timezone.utc)

    self.assertEqual(ormRecord.start, expectedStart)
    self.assertEqual(ormRecord.finish, expectedFinish)
    ormAnswers = list(ormRecord.complexanswers_set.all())

    self.assertEqual(ormAnswers[0].number, 1)
    self.assertEqual(ormAnswers[1].number, 2)

    self.assertEqual(
      (ormAnswers[0].option_a,
       ormAnswers[0].option_b,
       ormAnswers[0].option_c),
      (True,
       False,
       True))
    self.assertEqual(
      (ormAnswers[1].option_a,
       ormAnswers[1].option_b,
       ormAnswers[1].option_c),
      (True,
       False,
       True))

  def test_store_for_update(self):
    self.StoreDummyRecord()

    record = self.repository.Find(CandidateId('yo@neoma.das'))

    record.start = datetime(2022, 12, 13, 12, 12, 12, tzinfo=timezone.utc)
    record.finish = datetime(2022, 12, 13, 12, 15, 12, tzinfo=timezone.utc)

    record.answers[0].number = 3
    record.answers[1].number = 4

    record.answers[0].combination = False, True, False
    record.answers[1].combination = False, True, False

    self.repository.Store(record)

    # validation

    ormRecord = ORMCandidateComplexRecord.objects.get(
      candidateId=CandidateId('yo@neoma.das'))

    expectedStart = datetime(2022, 12, 12, 12, 12, 12, tzinfo=timezone.utc)
    expectedFinish = datetime(2022, 12, 12, 12, 15, 12, tzinfo=timezone.utc)

    self.assertEqual(ormRecord.start, expectedStart)
    self.assertEqual(ormRecord.finish, expectedFinish)
    ormAnswers = list(ormRecord.complexanswers_set.all())

    self.assertEqual(ormAnswers[0].number, 3)
    self.assertEqual(ormAnswers[1].number, 4)

    self.assertEqual(
      (ormAnswers[0].option_a,
       ormAnswers[0].option_b,
       ormAnswers[0].option_c),
      (False,
       True,
       False))
    self.assertEqual(
      (ormAnswers[1].option_a,
       ormAnswers[1].option_b,
       ormAnswers[1].option_c),
      (False,
       True,
       False))

  def StoreDummyRecord(self):
    answers = [
      ComplexAnswer(number=1, combination=(True, False, True)),
      ComplexAnswer(number=2, combination=(True, False, True)),
    ]

    record = ComplexRecord(
      candidateId=CandidateId('yo@neoma.das'),
      answers=answers,
      start=datetime(2022, 12, 12, 12, 12, 12, tzinfo=timezone.utc),
      finish=datetime(2022, 12, 12, 12, 15, 12, tzinfo=timezone.utc))

    self.repository.Store(record)
