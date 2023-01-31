from abc import abstractmethod
from datetime import datetime, timezone
import json

from django.core.exceptions import RequestAborted
from django.http import Http404, HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from neom.core.ioc import AutoWire
from pydrive2.files import ApiRequestError

from sinek.domain.model.freelancer import (
  Talent,
  ConditionBuilder,
  Email,
  Freelancer,
  HalfTime,
  FreelancerCommandService,
  CV,
  FreelancerNotFoundError,
  Tag,
  FreelancerRepository,
  Phone,
  Residence,
  File,
  FileRepository,
  GoogleId,
  Knowledge,
  CVRepository,
  Network,
  Url,
  AcceptanceAvailability,
  EnglishProficiency)
from sinek.domain.model.skill import Knowledge as SkillKnowledge
from sinek.interface.site.parts.freelancer.common import FreelancerViewBase
from sinek.domain.service import AutoKnowledgeService
from sinek.application.service import GoogleDriveService


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class ProfileSectionView(FreelancerViewBase, View):
  freelancerRepository: FreelancerRepository
  autoKnowledgeService: AutoKnowledgeService

  def post(self, request: HttpRequest) -> HttpResponse:

    freelancer = self.freelancer
    payload = json.loads(request.body)

    self.Update(freelancer, payload)

    try:
      self.freelancerRepository.Store(freelancer)
    # TODO: quitar Exception. Usar concreto
    except Exception as error:
      raise RequestAborted from error

    return HttpResponse('{"status": "OK"}')

  @abstractmethod
  def Update(self, freelancer: Freelancer, payload: dict):
    raise NotImplementedError()


class PersonalUpdateView(ProfileSectionView):
  def Update(self, freelancer: Freelancer, payload: dict):
    freelancer.name = payload['name']
    phoneCountryCode = Phone.CountryCode[payload['phoneCountryCode']]
    freelancer.phone = Phone.RemakeMake(phoneCountryCode, payload['phone'])
    location = payload['location']
    country = payload['country']
    freelancer.residence = Residence(location=location, country=country)
    wouldChangeCountry = eval(payload['wouldChangeCountry'])
    wouldChangeCity = eval(payload['wouldChangeCity'])
    interviewAvailability = eval(payload['interviewAvailability'])
    jobSwitchTime = AcceptanceAvailability.JobSwitchTime[payload['jobSwitchTime']]
    writing = EnglishProficiency.EnglishSkill[payload['writing']]
    speaking = EnglishProficiency.EnglishSkill[payload['speaking']]

    freelancer.acceptanceAvailability=AcceptanceAvailability(
        wouldChangeCountry=wouldChangeCountry,
        wouldChangeCity=wouldChangeCity,
        interviewAvailability=interviewAvailability,
        jobSwitchTime=jobSwitchTime)
    freelancer.englishProficiency=EnglishProficiency(
      writing=writing, speaking=speaking)


class InterestUpdateView(ProfileSectionView):
  def Update(self, freelancer: Freelancer, payload: dict):
    isTalent = payload['isTalent']
    isLancer = payload['isLancer']

    conditionBuilder = ConditionBuilder()

    if isTalent:
      incomeRange = (payload['minimum'], payload['maximum'])
      disponibility = Talent.Disponibility(int(payload['timeDisponibility']))
      modality = Talent.Modality(int(payload['modality']))
      conditionBuilder.AsTalent(incomeRange, disponibility, modality, None)

    if isLancer:
      isHalfTime = payload['isHalfTime']
      isFullTime = payload['isFullTime']

      if isHalfTime:
        experience = HalfTime.Experience(int(payload['experience']))
        availability = payload['availability']
        conditionBuilder.AsHalfTime(availability, experience)

      if isFullTime:
        conditionBuilder.AsFullTime()

    if not isTalent and not isLancer:
      conditionBuilder.AsInitial()

    freelancer.condition = conditionBuilder.Build()

    jobPreferences = {Tag(preference) for preference in payload['jobPreferences']}
    freelancer.jobPreferences.clear()
    freelancer.jobPreferences.update(jobPreferences)

    worklifePreferences = {Tag(preference) for preference in payload['worklifePreferences']}
    freelancer.worklifePreferences.clear()
    freelancer.worklifePreferences.update(worklifePreferences)


class ProjectUpdateView(ProfileSectionView):
  def Update(self, freelancer: Freelancer, payload: dict):
    projects = {Tag(project) for project in payload}
    freelancer.projects.clear()
    freelancer.projects.update(projects)


class BusinessUpdateView(ProfileSectionView):
  def Update(self, freelancer: Freelancer, payload: dict):
    businesses = {Tag(business) for business in payload}
    freelancer.businesses.clear()
    freelancer.businesses.update(businesses)


class NetworkUpdateView(ProfileSectionView):
  def Update(self, freelancer: Freelancer, payload: dict):
    networkValue = payload['network']
    urlValue = payload['url']

    from sinek.domain.model.freelancer import Network, Url

    try:
      network = Network.Kind(int(networkValue))
    except ValueError:
      # network es un valor inválido para el Enum
      raise RequestAborted

    # TODO: atrapar exception del link
    url = Url(urlValue)

    network = Network(url)
    freelancer.networks.append(network)


class NetworkDeleteView(ProfileSectionView):
  def Update(self, freelancer: Freelancer, payload: dict):
    networkUrl = payload['url']
    for network in freelancer.networks:
      if network.url.value == networkUrl:
        freelancer.networks.remove(network)


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(FreelancerViewBase, View):

  freelancerRepository: FreelancerRepository
  fileRepository: FileRepository
  googleDriveService: GoogleDriveService

  def post(self, request: HttpRequest):
    archivos = request.FILES.getlist('files[]')

    freelancer = self._getFreelancer(self.request.user.username)

    portfolio = []

    for item in archivos:
      file = File(
        googleId=GoogleId(id=''),
        freelancer=freelancer, name=item.name,
        created=datetime.now(
          timezone.utc),
        blob=item.file.read())

      portfolio.append(file)

    # TODO: Rehacer todo este código para que no ocurra que se cuelgue en drive
    # Y no en BD
    try:
      uploads = self.googleDriveService.UploadFreelancerPortfolio(portfolio)
    except Exception as error:
      raise RequestAborted from error

    for i in range(len(portfolio)):
      portfolio[i].googleId = GoogleId(id=uploads[i].googleId)
      self.fileRepository.Store(portfolio[i])

    archivosJson = '['
    for upload in uploads:
      archivosJson += '{"path":"' + upload.path + '", "name":"' + \
        upload.name + '", "id":"' + upload.googleId + '"},'
    archivosJson = archivosJson[:-1]
    archivosJson += ']'

    return HttpResponse('{"status": "OK", "archivos": ' + archivosJson + ' }')

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class FileDeleteView(FreelancerViewBase, View):
  googleDriveService: GoogleDriveService
  freelancerRepository: FreelancerRepository
  fileRepository: FileRepository

  def post(self, request):
    freelancer = self._getFreelancer(self.request.user.username)

    payload = json.loads(request.body)
    fileId = payload['googleId']
    googleId = GoogleId(id=fileId)

    try:
      self.fileRepository.Drop(freelancer, googleId)
    except BaseException:
      # El archivo no le pertenece al freelancer o no existe
      return HttpResponse('{"status": "ERROR"}')

    self.googleDriveService.RemoveFreelancerUpload(googleId)

    return HttpResponse('{"status": "OK"}')

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class KnowledgeUpdateView(FreelancerViewBase, View):

  freelancerRepository: FreelancerRepository
  freelancerCommandService: FreelancerCommandService

  def post(self, request):
    freelancer = self._getFreelancer(self.request.user.username)

    payload = json.loads(request.body)
    knowledgeKey = payload['key']
    knowledgeName = payload['name']
    knowledgeScore = int(payload['score'])
    knowledge = Knowledge(
      key=knowledgeKey,
      name=knowledgeName,
      score=Knowledge.Score(knowledgeScore))

    # TODO: Agregar un try-catch
    self.freelancerCommandService.StoreKnowledge(freelancer, knowledge)
    return HttpResponse('{"status": "OK"}')

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class KnowledgeDeleteView(FreelancerViewBase, View):

  freelancerRepository: FreelancerRepository
  freelancerCommandService: FreelancerCommandService

  def post(self, request, *args, **kwargs):
    freelancer = self._getFreelancer(self.request.user.username)

    payload = json.loads(request.body)
    knowledgeKey = payload['key']
    knowledgeName = payload['name']

    knowledge = SkillKnowledge(key=knowledgeKey, name=knowledgeName)
    # TODO: Agregar un try-catch
    self.freelancerCommandService.DropKnowledge(freelancer, knowledge)
    return HttpResponse('{"status": "OK"}')

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class CVDeleteView(FreelancerViewBase, View):

  googleDriveService: GoogleDriveService
  cvRepository: CVRepository
  freelancerRepository: FreelancerRepository

  def post(self, request, *args, **kwargs):
    freelancer = self._getFreelancer(self.request.user.username)

    payload = json.loads(request.body)
    fileId = payload['googleId']

    googleId = GoogleId(id=fileId)

    try:
      self.googleDriveService.RemoveFreelancerUpload(googleId)
    except ApiRequestError:
      return HttpResponse('{"status": "ERROR"}')

    self.cvRepository.Drop(freelancer, googleId)
    return HttpResponse('{"status": "OK"}')

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class CVUploadView(FreelancerViewBase, View):

  freelancerRepository: FreelancerRepository
  cvRepository: CVRepository
  googleDriveService: GoogleDriveService

  def post(self, request: HttpRequest):
    archivo = request.FILES.get('archivo')

    freelancer = self._getFreelancer(self.request.user.username)

    cv = CV(
      googleId=GoogleId(id=''),
      freelancer=freelancer, name=archivo.name,
      created=datetime.now(
        timezone.utc),
      blob=archivo.file.read())

    try:
      upload = self.googleDriveService.UploadFreelancerCV(cv)
    except Exception as error:
      raise RequestAborted from error

    cv.googleId = GoogleId(id=upload.googleId)
    self.cvRepository.Store(cv)
    return HttpResponse(
      '{"status": "OK", "path":"' +
      upload.path +
      '", "name":"' +
      upload.name +
      '", "id":"' +
      upload.googleId +
      '"}')

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class PortfolioAutoSkillsView(FreelancerViewBase, View):

  autoKnowledgeService: AutoKnowledgeService
  cvRepository: CVRepository
  freelancerRepository: FreelancerRepository

  def get(self, request: HttpRequest):
    freelancer = self._getFreelancer(self.request.user.username)
    cvs = self.cvRepository.FindBy(freelancer)
    tree = self.autoKnowledgeService.UpdateKnowledgesFromPortfolio(
      cvs, freelancer)

    if tree:
      return HttpResponse(
        '{"status": "OK", "updateTree": "True", "tree": "' + tree + '"}')

    return HttpResponse('{"status": "OK", "updateTree": "False"}')

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@method_decorator(csrf_exempt, name='dispatch')
class StepView(FreelancerViewBase, View):
  freelancerRepository: FreelancerRepository
  autoKnowledgeService: AutoKnowledgeService

  def post(self, request: HttpRequest) -> HttpResponse:

    freelancer = self.freelancer
    payload = json.loads(request.body)

    self.Update(freelancer, payload)

    try:
      self.freelancerRepository.Store(freelancer)
    # TODO: quitar Exception. Usar concreto
    except Exception as error:
      raise RequestAborted from error

    return HttpResponse('{"status": "OK"}')

  @abstractmethod
  def Update(self, freelancer: Freelancer, payload: dict):
    raise NotImplementedError()


class FirstStepView(StepView):
  def Update(self, freelancer: Freelancer, payload: dict):
    freelancer.name = payload['name']
    phoneCountryCode = Phone.CountryCode[payload['phoneCountryCode']]
    freelancer.phone = Phone.RemakeMake(phoneCountryCode, payload['phone'])
    location = payload['location']
    country = payload['country']
    freelancer.residence = Residence(location=location, country=country)
    wouldChangeCountry = eval(payload['wouldChangeCountry'])
    wouldChangeCity = eval(payload['wouldChangeCity'])
    interviewAvailability = eval(payload['interviewAvailability'])
    jobSwitchTime = AcceptanceAvailability.JobSwitchTime[payload['jobSwitchTime']]
    writing = EnglishProficiency.EnglishSkill[payload['writing']]
    speaking = EnglishProficiency.EnglishSkill[payload['speaking']]

    urlValue = payload['linkedin']

    # TODO: atrapar exception del link
    url = Url(urlValue)

    network = Network(url)

    # TODO: Esto eliminará los otros Networks que hayan colocado
    # los freelancers en producción
    freelancer.networks = [network]

    freelancer.acceptanceAvailability=AcceptanceAvailability(
        wouldChangeCountry=wouldChangeCountry,
        wouldChangeCity=wouldChangeCity,
        interviewAvailability=interviewAvailability,
        jobSwitchTime=jobSwitchTime)
    freelancer.englishProficiency=EnglishProficiency(
      writing=writing, speaking=speaking)


class SecondStepView(StepView):
  def Update(self, freelancer: Freelancer, payload: dict):
    roles = {Tag(role) for role in payload['roles']}
    freelancer.roleInterests.clear()
    freelancer.roleInterests.update(roles)

    isTalent = payload['isTalent']
    isLancer = payload['isLancer']

    conditionBuilder = ConditionBuilder()

    if isTalent:
      incomeRange = (payload['minimum'], payload['maximum'])
      disponibility = Talent.Disponibility(int(payload['timeDisponibility']))
      modality = Talent.Modality(int(payload['modality']))
      conditionBuilder.AsTalent(incomeRange, disponibility, modality, None)

    if isLancer:
      isHalfTime = payload['isHalfTime']
      isFullTime = payload['isFullTime']

      if isHalfTime:
        experience = HalfTime.Experience(int(payload['experience']))
        availability = payload['availability']
        conditionBuilder.AsHalfTime(availability, experience)

      if isFullTime:
        conditionBuilder.AsFullTime()

    if not isTalent and not isLancer:
      conditionBuilder.AsInitial()

    freelancer.condition = conditionBuilder.Build()


class ThirdStepView(StepView):
  def Update(self, freelancer: Freelancer, payload: dict):
    pass


@AutoWire
@method_decorator(csrf_exempt, name='dispatch')
class CVUploadWizardView(FreelancerViewBase, View):

  autoKnowledgeService: AutoKnowledgeService
  cvRepository: CVRepository
  freelancerRepository: FreelancerRepository
  freelancerCommandService: FreelancerCommandService
  googleDriveService: GoogleDriveService

  def post(self, request: HttpRequest):
    archivo = request.FILES.get('archivo')

    freelancer = self.freelancer

    self.freelancerCommandService.DropPremarkedKnowledges(freelancer)
    self._clearCVs(freelancer)

    cv = CV(
      googleId=GoogleId(id=''),
      freelancer=freelancer, name=archivo.name,
      created=datetime.now(
        timezone.utc),
      blob=archivo.file.read())

    try:
      upload = self.googleDriveService.UploadFreelancerCV(cv)
    except Exception as error:
      raise RequestAborted from error

    cv.googleId = GoogleId(id=upload.googleId)
    self.cvRepository.Store(cv)

    tree = self.autoKnowledgeService.UpdateKnowledgesFromPortfolio(
      [cv], freelancer)

    if tree:
      return HttpResponse(
        '{"status": "OK", "updateTree": "True", "tree": "' + tree + '", "path":"' +
        upload.path +
        '", "name":"' +
        upload.name +
        '", "id":"' +
        upload.googleId +
        '"}')

    return HttpResponse('{"status": "OK", "updateTree": "False"}')

  def _clearCVs(self, freelancer: Freelancer):
    cvs = self.cvRepository.FindBy(freelancer)
    for c in cvs:
      try:
        self.googleDriveService.RemoveFreelancerUpload(c.googleId)
        self.cvRepository.Drop(freelancer, c.googleId)
      except ApiRequestError:
        print('ERROR')
        return HttpResponse('{"status": "ERROR"}')


class FourthStepView(StepView):
  def Update(self, freelancer: Freelancer, payload: dict):
    projects = {Tag(project) for project in payload['projects']}
    freelancer.projects.clear()
    freelancer.projects.update(projects)

    businesses = {Tag(business) for business in payload['businesses']}
    freelancer.businesses.clear()
    freelancer.businesses.update(businesses)

    # TODO: Validar que solo haya agregado el número máx permitido de preferences

    jobPreferences = {Tag(preference) for preference in payload['jobPreferences']}
    freelancer.jobPreferences.clear()
    freelancer.jobPreferences.update(jobPreferences)

    worklifePreferences = {Tag(preference) for preference in payload['worklifePreferences']}
    freelancer.worklifePreferences.clear()
    freelancer.worklifePreferences.update(worklifePreferences)

    # TODO: Realizar este cambio de estado verificando que haya
    # llenado todos los datos anteriores
    freelancer.isOnboarded = True
