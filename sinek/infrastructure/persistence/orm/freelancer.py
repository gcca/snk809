from datetime import datetime, timedelta, timezone
from typing import List, Set, Tuple

from django.db.models.query import QuerySet

from sinek.domain.model.skill import Skill, Knowledge as SkillKnowledge
from sinek.domain.model.freelancer import (
  CV, AcceptanceAvailability, Condition, CVNotFoundError, CVRepository, Email, EnglishProficiency, File, FileNotFoundError,
  FileRepository, Freelancer, GoogleId, FreelancerCommandService,
  FreelancerNotFoundError, FreelancerQueryService, ConditionBuilder,
  FreelancerRepository, Knowledge, Network, Phone, Residence, Tag, Url, Talent,
  FullTime, HalfTime, Initial, Condition)
from sinek.domain.service import FreelancerExperienceService, FreelancerPeriodService

from .models import Freelancer as ORMFreelancer
from .models import FreelancerBusinessTag as ORMBusinessTag
from .models import FreelancerKnowledge as ORMKnowledge
from .models import FreelancerSkill as ORMSkill
from .models import FreelancerNetwork as ORMNetwork
from .models import FreelancerProjectTag as ORMProjectTag
from .models import FreelancerRoleTag as ORMRoleTag
from .models import FreelancerJobTag as ORMFreelanceJobTag
from .models import FreelancerWorklifeTag as ORMFreelancerWorklifeTag
from .models import Upload as ORMUpload

__all__ = [
  'FreelancerRepositoryORM',
  'CVRepositoryORM',
  'FileRepositoryORM',
  'FreelancerQueryServiceORM'
  'FreelancerCommandServiceORM']


class FreelancerRepositoryORM(FreelancerRepository):

  def All(self) -> List[Freelancer]:
    ormFreelancers = ORMFreelancer.objects.all()
    freelancers = [_makeFromORM(freelancer) for freelancer in ormFreelancers]
    return freelancers

  def Find(self, email: Email) -> Freelancer:
    try:
      ormFreelancer = ORMFreelancer.objects.get(email=str(email))
    except ORMFreelancer.DoesNotExist as error:
      raise FreelancerNotFoundError(f'No freelancer "{email}"') from error
    return _makeFromORM(ormFreelancer)

  def Store(self, freelancer: Freelancer):
    try:
      ormFreelancer = ORMFreelancer.objects.get(email=str(freelancer.email))
    except ORMFreelancer.DoesNotExist:
      ormFreelancer = ORMFreelancer()

    # TODO: crear un método para completar el objeto ORM
    ormFreelancer.email = str(freelancer.email)
    ormFreelancer.name = freelancer.name
    ormFreelancer.countryCode = freelancer.phone.countryCode
    ormFreelancer.phone = freelancer.phone.number

    if isinstance(freelancer.condition, Initial):
      ormFreelancer.condition = ORMFreelancer.ConditionChoices.INITIAL
    elif isinstance(freelancer.condition, Talent) and isinstance(freelancer.condition, FullTime):
      ormFreelancer.condition = ORMFreelancer.ConditionChoices.TALENTANDFULLTIME
    elif isinstance(freelancer.condition, Talent) and isinstance(freelancer.condition, HalfTime):
      ormFreelancer.condition = ORMFreelancer.ConditionChoices.TALENTANDHALFTIME
    elif isinstance(freelancer.condition, Talent):
      ormFreelancer.condition = ORMFreelancer.ConditionChoices.TALENT
    elif isinstance(freelancer.condition, HalfTime):
      ormFreelancer.condition = ORMFreelancer.ConditionChoices.HALFTIME
    elif isinstance(freelancer.condition, FullTime):
      ormFreelancer.condition = ORMFreelancer.ConditionChoices.FULLTIME

    if isinstance(freelancer.condition, HalfTime):
      ormFreelancer.experience = freelancer.condition.experience.value
      ormFreelancer.availability = freelancer.condition.availability

    if isinstance(freelancer.condition, Talent):
      ormFreelancer.minimum, ormFreelancer.maxIncome = freelancer.condition.incomeRange
      ormFreelancer.disponibility = freelancer.condition.disponibility.value
      ormFreelancer.modality = freelancer.condition.modality.value
      ormFreelancer.expectative = freelancer.condition.expectative

    ormFreelancer.location = freelancer.residence.location
    ormFreelancer.country = freelancer.residence.country

    ormFreelancer.wouldChangeCity = freelancer.acceptanceAvailability.wouldChangeCity
    ormFreelancer.wouldChangeCountry = freelancer.acceptanceAvailability.wouldChangeCountry
    ormFreelancer.interviewAvailability = freelancer.acceptanceAvailability.interviewAvailability
    ormFreelancer.jobSwitchTime = freelancer.acceptanceAvailability.jobSwitchTime.value
    ormFreelancer.englishSpeakingSkills = freelancer.englishProficiency.speaking.value
    ormFreelancer.englishWritingSkills = freelancer.englishProficiency.writing.value
    
    ormFreelancer.isOnboarded = freelancer.isOnboarded

    ormFreelancer.save()

    ormFreelancer.businessTags.all().delete()
    ormBusinessTags = [ORMBusinessTag(name=tag.name, freelancer=ormFreelancer)
                       for tag in freelancer.businesses]
    ormFreelancer.businessTags.bulk_create(ormBusinessTags)

    ormFreelancer.projectTags.all().delete()
    ormProjectTags = [ORMProjectTag(name=tag.name, freelancer=ormFreelancer)
                      for tag in freelancer.projects]
    ormFreelancer.projectTags.bulk_create(ormProjectTags)

    ormFreelancer.links.all().delete()
    ormUrls = [
      ORMNetwork(
        freelancer=ormFreelancer,
        url=str(network.url)) for network in freelancer.networks]
  
    ormFreelancer.links.bulk_create(ormUrls)

    ormFreelancer.jobPreferences.all().delete()
    ormJobTags = [ORMFreelanceJobTag(name=tag.name, freelancer=ormFreelancer) for tag in freelancer.jobPreferences]
    ormFreelancer.jobPreferences.bulk_create(ormJobTags)

    ormFreelancer.worklifePreferences.all().delete()
    ormWorklifeTags = [ORMFreelancerWorklifeTag(name=tag.name, freelancer=ormFreelancer) for tag in freelancer.worklifePreferences]
    ormFreelancer.worklifePreferences.bulk_create(ormWorklifeTags)

    ormFreelancer.roleInterests.all().delete()
    ormRoleTags = [ORMRoleTag(name=tag.name, freelancer=ormFreelancer) for tag in freelancer.roleInterests]
    ormFreelancer.roleInterests.bulk_create(ormRoleTags)


def _makeFromORM(ormFreelancer: ORMFreelancer) -> Freelancer:
  return Freelancer(
    email=Email(ormFreelancer.email),
    name=ormFreelancer.name,
    phone=Phone(
      Phone.CountryCode(
        ormFreelancer.countryCode),
      ormFreelancer.phone),
    condition=_makeCondition(ormFreelancer.condition, ormFreelancer.experience,
                             ormFreelancer.availability, (ormFreelancer.minimum, ormFreelancer.maxIncome), ormFreelancer.disponibility,
                             ormFreelancer.modality, ormFreelancer.expectative),
    residence=_makeResidence(ormFreelancer.location, ormFreelancer.country),
    networks=_makeUrls(ormFreelancer.links.all()),
    businesses=_makeBusinesses(ormFreelancer.businessTags.all()),
    projects=_makeProjects(ormFreelancer.projectTags.all()),
    acceptanceAvailability=_makeAcceptanceAvailability(
      ormFreelancer.wouldChangeCountry,
      ormFreelancer.wouldChangeCity,
      ormFreelancer.interviewAvailability,
      ormFreelancer.jobSwitchTime,),
    englishProficiency=_makeEnglishProficiency(ormFreelancer.englishSpeakingSkills, ormFreelancer.englishWritingSkills),
    roleInterests=_makeRoleInterests(ormFreelancer.roleInterests.all()),
    jobPreferences=_makeJobPreferences(ormFreelancer.jobPreferences.all()),
    worklifePreferences=_makeWorklifePreferences(ormFreelancer.worklifePreferences.all()),
    isOnboarded=ormFreelancer.isOnboarded,)

def _makeWorklifePreferences(worklifePreferences: QuerySet) -> Set[Tag]:
  return { Tag(name=worklifePreference.name) for worklifePreference in worklifePreferences }

def _makeJobPreferences(jobPreferences: QuerySet) -> Set[Tag]:
  return { Tag(name=jobPreference.name) for jobPreference in jobPreferences }

def _makeAcceptanceAvailability(wouldChangeCountry: bool, wouldChangeCity: bool,
                                interviewAvailability: bool, jobSwitchTime: int) -> AcceptanceAvailability:
  return AcceptanceAvailability(
    wouldChangeCountry=wouldChangeCountry,
    wouldChangeCity=wouldChangeCity,
    interviewAvailability=interviewAvailability,
    jobSwitchTime=AcceptanceAvailability.JobSwitchTime(jobSwitchTime),
  )

def _makeEnglishProficiency(speakingSkill: int, writingSkill: int) -> EnglishProficiency:
  return EnglishProficiency(
    speaking=EnglishProficiency.EnglishSkill(speakingSkill),
    writing=EnglishProficiency.EnglishSkill(writingSkill)
  )

def _makeRoleInterests(roleTags: QuerySet) -> Set[Tag]:
  return {Tag(name=role.name) for role in roleTags}

def _makeUrls(ormUrls: List[ORMNetwork]) -> List[Network]:
  return [_makeNetwork(ormUrl) for ormUrl in ormUrls]

def _makeNetwork(ormUrl: ORMNetwork) -> Network:
  return Network(Url(ormUrl.url))

def _makeBusinesses(ormBusinesses: QuerySet) -> Set[Tag]:
  return {Tag(name=ormBusiness.name) for ormBusiness in ormBusinesses}

def _makeProjects(projects: QuerySet) -> Set[Tag]:
  return {Tag(name=project.name) for project in projects}

def _makeCondition(
    condition: str,
    experience: int,
    availability: int,
    incomeRange: tuple,
    disponibility: int,
    modality: int,
    expectative: str) -> Condition:

  conditionBuilder = ConditionBuilder()

  if condition == ORMFreelancer.ConditionChoices.INITIAL:
    conditionBuilder.AsInitial()
  elif condition == ORMFreelancer.ConditionChoices.FULLTIME:
    conditionBuilder.AsFullTime()
  elif condition == ORMFreelancer.ConditionChoices.HALFTIME:
    conditionBuilder.AsHalfTime(
      availability=availability, experience=HalfTime.Experience(experience))
  elif condition == ORMFreelancer.ConditionChoices.TALENT:
    conditionBuilder.AsTalent(
      incomeRange=incomeRange, disponibility=Talent.Disponibility(disponibility),
      modality=Talent.Modality(modality), expectative=expectative)
  elif condition == ORMFreelancer.ConditionChoices.TALENTANDFULLTIME:
    conditionBuilder.AsTalent(
      incomeRange=incomeRange, disponibility=Talent.Disponibility(disponibility),
      modality=Talent.Modality(modality), expectative=expectative).AsFullTime()
  elif condition == ORMFreelancer.ConditionChoices.TALENTANDHALFTIME:
    conditionBuilder.AsTalent(
      incomeRange=incomeRange, disponibility=Talent.Disponibility(disponibility),
      modality=Talent.Modality(modality), expectative=expectative).AsHalfTime(
        availability=availability, experience=HalfTime.Experience(experience))

  return conditionBuilder.Build()

def _makeResidence(ormLocation: str, ormCountry: str) -> Residence:
  return Residence(location=ormLocation, country=ormCountry)


# -----------------------------------------------------------------------------

class CVRepositoryORM(CVRepository):

  def Find(self, freelancer: Freelancer) -> CV:
    try:
      ormUpload = ORMUpload.objects.get(
        freelancer__email=freelancer.email,
        kind=ORMUpload.KindChoices.CV)
    except ORMFreelancer.DoesNotExist as error:
      raise FreelancerNotFoundError() from error
    except ORMUpload.DoesNotExist as error:
      raise CVNotFoundError() from error

    upload = CV(
      googleId=GoogleId(id=ormUpload.googleId),
      freelancer=freelancer,
      name=ormUpload.name,
      created=ormUpload.created,
      blob=ormUpload.binary)

    return upload

  def Store(self, cv: CV):
    try:
      ormUpload = ORMUpload.objects.get(
        name=cv.name, freelancer__email=cv.freelancer.email,
        kind=ORMUpload.KindChoices.CV)
    except ORMUpload.DoesNotExist:
      ormUpload = ORMUpload()

    try:
      ormUpload.freelancer = ORMFreelancer.objects.get(
        email=str(cv.freelancer.email))
    except ORMFreelancer.DoesNotExist:
      raise ValueError('No possible store upload. No freelancer')

    ormUpload.googleId = str(cv.googleId)
    ormUpload.name = cv.name
    ormUpload.created = cv.created
    ormUpload.kind = ORMUpload.KindChoices.CV
    #ormUpload.binary = cv.blob

    ormUpload.save()

  def Drop(self, freelancer: Freelancer, googleId: GoogleId):
    try:
      ormUpload = ORMUpload.objects.get(
        freelancer__email=freelancer.email,
        googleId=str(googleId),
        kind=ORMUpload.KindChoices.CV)
    except ORMFreelancer.DoesNotExist as error:
      raise FreelancerNotFoundError() from error
    except ORMUpload.DoesNotExist as error:
      raise CVNotFoundError() from error

    ormUpload.delete()

  def FindBy(self, freelancer: Freelancer) -> List[CV]:
    ormUploads = ORMUpload.objects.filter(
      freelancer__email=freelancer.email,
      kind=ORMUpload.KindChoices.CV)
    return [CV(googleId=GoogleId(id=ormUpload.googleId), freelancer=freelancer,
               name=ormUpload.name,
               created=ormUpload.created,
               blob=ormUpload.binary)
            for ormUpload in ormUploads]


class FileRepositoryORM(FileRepository):

  def Find(self, freelancer: Freelancer, fileName: str) -> File:
    try:
      ormUpload = ORMUpload.objects.get(
        name=fileName,
        freelancer__email=freelancer.email,
        kind=ORMUpload.KindChoices.OTHER)
    except ORMFreelancer.DoesNotExist as error:
      raise FreelancerNotFoundError() from error
    except ORMUpload.DoesNotExist as error:
      raise FileNotFoundError() from error

    upload = File(
      googleId=GoogleId(id=ormUpload.googleId),
      freelancer=freelancer,
      name=ormUpload.name,
      created=ormUpload.created,
      blob=ormUpload.binary)

    return upload

  def Store(self, file: File):
    # TODO: Agregué el created porque cuando se cuelgan 2 archivos con el mismo nombre
    # es reemplazado. Se debe refactorizar
    try:
      ormUpload = ORMUpload.objects.get(
        name=file.name, freelancer__email=file.freelancer.email,
        created=file.created, kind=ORMUpload.KindChoices.OTHER)
    except ORMUpload.DoesNotExist:
      ormUpload = ORMUpload()

    try:
      ormUpload.freelancer = ORMFreelancer.objects.get(
        email=str(file.freelancer.email))
    except ORMFreelancer.DoesNotExist:
      # TODO
      raise ValueError('No possible store upload. No freelancer')

    ormUpload.googleId = str(file.googleId)
    ormUpload.name = file.name
    ormUpload.created = file.created
    ormUpload.kind = ORMUpload.KindChoices.OTHER
    #ormUpload.binary = file.blob

    ormUpload.save()

  # TODO: Temporal. Remover y usar el query set. Ver UploadRepository interface
  def FindBy(self, freelancer: Freelancer) -> List[File]:
    ormUploads = ORMUpload.objects.filter(
      freelancer__email=freelancer.email,
      kind=ORMUpload.KindChoices.OTHER)
    return [
      File(
        googleId=GoogleId(
          id=ormUpload.googleId),
        freelancer=freelancer,
        name=ormUpload.name,
        created=ormUpload.created,
        blob=ormUpload.binary) for ormUpload in ormUploads]

  def Drop(self, freelancer: Freelancer, googleId: GoogleId):
    try:
      ormUpload = ORMUpload.objects.get(
        freelancer__email=freelancer.email,
        googleId=str(googleId),
        kind=ORMUpload.KindChoices.OTHER)
    except ORMFreelancer.DoesNotExist as error:
      raise FreelancerNotFoundError() from error
    except ORMUpload.DoesNotExist as error:
      raise FileNotFoundError() from error

    ormUpload.delete()


class FreelancerCommandServiceORM(FreelancerCommandService):

  def StoreKnowledge(self, freelancer: Freelancer, knowledge: Knowledge):
    # TODO: Utilizar solo el ORMKnowledge, no esta reconociendo el
    # freelancer__email
    ormFreelancer = ORMFreelancer.objects.get(email=str(freelancer.email))
    ORMKnowledge.objects.update_or_create(
      freelancer=ormFreelancer,
      skill_id=knowledge.key,
      defaults={'value': knowledge.score.value})

  def DropKnowledge(self, freelancer: Freelancer, knowledge: SkillKnowledge):
    ormKnowledge = ORMKnowledge.objects.get(
      freelancer__email=str(freelancer.email),
      skill_id=knowledge.key, skill__name=knowledge.name)
    ormKnowledge.delete()

  def DropBusiness(self, freelancer: Freelancer, tag: Tag):
    ormBusinessTag = ORMBusinessTag.objects.get(
      freelancer__email=str(freelancer.email), name=tag.name)
    ormBusinessTag.delete()

  def DropProject(self, freelancer: Freelancer, tag: Tag):
    ormProjectTag = ORMProjectTag.objects.get(
      freelancer__email=str(freelancer.email), name=tag.name)
    ormProjectTag.delete()

  def DropPremarkedKnowledges(self, freelancer: Freelancer):
    ormKnowledges = ORMKnowledge.objects.filter(
      freelancer__email=str(freelancer.email),
      value=Knowledge.Score.PREMARKED)
    ormKnowledges.delete()


class FreelancerQueryServiceORM(FreelancerQueryService):

  def ListAllBusinesses(self) -> Set[str]:
    from .businesstag_data import INITIAL_BUSINESSES
    return INITIAL_BUSINESSES

  def ListAllProjects(self) -> Set[str]:
    from .projecttag_data import INITIAL_PROJECTS
    return INITIAL_PROJECTS

  def ListKnowledges(self, freelancer: Freelancer) -> List[Knowledge]:
    return [
      Knowledge(
        key=knowledge.skill.id,
        name=knowledge.skill.name,
        score=Knowledge.Score(
          knowledge.value)) for knowledge in ORMKnowledge.objects.filter(
        freelancer__email=str(
          freelancer.email))]

  def ListKnowledgesNotScored(self, freelancer: Freelancer) -> Set[Skill]:
    # TODO: Listar skills que no tengan children y sean descendientes de
    # la rama del rol del freelancer
    skills = {
      Skill(key=skillORM.id, name=skillORM.name)
      for skillORM in ORMSkill.objects.filter(children=None)}
    knowledges = {
      Skill(
        key=knowledge.skill.id, name=knowledge.skill.name)
      for knowledge in ORMKnowledge.objects.filter(
        freelancer__email=str(freelancer.email))}
    return skills - knowledges

  def CounterFreelancers(self, name: str = '') -> int:
    return len(ORMFreelancer.objects.filter(name__icontains=name))

  def ListFreelancersByPeriod(
      self,
      period: FreelancerPeriodService.Period) -> List[Freelancer]:
    currentPeriodsVisitor = CurrentPeriodVisitor()
    ormFreelancers = period.GetAffiliates(currentPeriodsVisitor)
    return [_makeFromORM(freelancer) for freelancer in ormFreelancers]

  def ListFreelancersByTwoLastPeriod(
      self, period: FreelancerPeriodService.Period) -> Tuple[List[Freelancer], List[Freelancer]]:
    twoPeriodsVisitor = TwoPeriodsVisitor()
    ormPreviousPeriodFreelancers, ormCurrentPeriodFreelancers = period.GetAffiliates(
      twoPeriodsVisitor)
    previousFreelancers = [_makeFromORM(freelancer)
                           for freelancer in ormPreviousPeriodFreelancers]
    currentFreelancers = [_makeFromORM(freelancer)
                          for freelancer in ormCurrentPeriodFreelancers]
    return previousFreelancers, currentFreelancers

  def FindToComputeCompatibility(self, name: str, pagination: int,
                                 limit: int = 10) -> List[FreelancerExperienceService.FreelancerExperience]:
    offset = (pagination - 1) * limit
    ormFreelancers = ORMFreelancer.objects.all()
    if name:
      ormFreelancers = ormFreelancers.filter(name__icontains=name)
    return [_makeExperience(ormFreelancer)
            for ormFreelancer in ormFreelancers[offset:offset + limit]]

  def ListPagFreelancers(
      self,
      pagination: int,
      limit: int = 10) -> List[Freelancer]:
    offset = (pagination - 1) * limit
    return [
      _makeFromORM(ormFreelancer) for ormFreelancer in ORMFreelancer.objects.all()[
        offset:offset + limit]]

  def HasPremarkeds(self, freelancer: Freelancer) -> bool:
    return ORMKnowledge.objects.filter(
      freelancer__email=freelancer.email,
      value=Knowledge.score.PREMARKED).exists()


def _makeExperience(
    ormFreelancer: ORMFreelancer) -> FreelancerExperienceService.FreelancerExperience:
  knowledges = [
    Knowledge(ormKnowledge.id, ormKnowledge.skill.name, ormKnowledge.value)
    for ormKnowledge in ormFreelancer.knowledges.all()]
  freelancer = _makeFromORM(ormFreelancer)
  return FreelancerExperienceService.FreelancerExperience(
    freelancer=freelancer, knowledges=knowledges)


class CurrentPeriodVisitor(FreelancerPeriodService.PeriodVisitor):

  today = datetime.now(timezone.utc)

  def GetYearAffiliates(self):
    return ORMFreelancer.objects.filter(
      role__user__date_joined__year=self.today.year)

  def GetMonthAffiliates(self):
    return ORMFreelancer.objects.filter(
      role__user__date_joined__year=self.today.year,
      role__user__date_joined__month=self.today.month)

  def GetWeekAffiliates(self):
    currentRange = [
      self.today -
      timedelta(
        days=self.today.weekday()),
      self.today]
    return ORMFreelancer.objects.filter(
      role__user__date_joined__range=currentRange)

  def GetCustomPeriodAffiliates(self, period: FreelancerPeriodService.Custom):
    return ORMFreelancer.objects.filter(
      role__user__date_joined__range=[
        period.start, period.end])


class TwoPeriodsVisitor(FreelancerPeriodService.PeriodVisitor):

  today = datetime.now(timezone.utc)

  def GetYearAffiliates(self):
    previous = ORMFreelancer.objects.filter(
      role__user__date_joined__year=self.today.year - 1)
    current = ORMFreelancer.objects.filter(
      role__user__date_joined__year=self.today.year)
    return previous, current

  def GetMonthAffiliates(self):
    previous = ORMFreelancer.objects.filter(
      role__user__date_joined__year=self.today.year,
      role__user__date_joined__month=self.today.month - 1)
    current = ORMFreelancer.objects.filter(
      role__user__date_joined__year=self.today.year,
      role__user__date_joined__month=self.today.month)
    return previous, current

  def GetWeekAffiliates(self):
    previousRange = [
      self.today -
      timedelta(
        days=self.today.weekday() +
        7),
      self.today -
      timedelta(
        days=self.today.weekday() +
        1)]
    currentRange = [
      self.today -
      timedelta(
        days=self.today.weekday()),
      self.today]
    previous = ORMFreelancer.objects.filter(
      role__user__date_joined__range=previousRange)
    current = ORMFreelancer.objects.filter(
      role__user__date_joined__range=currentRange)
    return previous, current
