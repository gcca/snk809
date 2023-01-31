import math
from typing import List, Tuple
from datetime import datetime

from neom.core.ioc import AutoWire

from django.http import QueryDict

from sinek.application.service import GoogleDriveService
from sinek.domain.model.freelancer import (Email, Freelancer,
                                           FreelancerQueryService,
                                           FreelancerRepository)
from sinek.domain.model.project import Project
from sinek.domain.model.skill import Root, SkillQueryService
from sinek.domain.model.initiative import Initiative, Contact, CompanyCode, InitiativeQueryService, InitiativeRepository
from sinek.domain.service import (FreelancerExperienceService,
                                  FreelancerPeriodService,
                                  FreelancerCountTreeService,
                                  FreelancerKnowledgeTreeService,
                                  ProfileService, ProjectService,
                                  InitiativeCreationService)
from sinek.interface.site.parts.freelancer.adapter import ProfileViewAdapter
from sinek.interface.site.parts.accountmanager.adapter import CountedTreeViewAdapter

from .adapter import FreelancerRankViewAdapter, InitiativeViewAdapter, ProjectViewAdapter
from .forms import ProjectForm


@AutoWire
class ProjectFacade:

  projectService: ProjectService

  # TODO: Agregar datos para agregar account manager como FK
  def CreateProject(self, form: ProjectForm):
    projectName = form['name'].value()
    project = Project(name=projectName)
    self.projectService.Create(project)

  def ListAllProjects(self) -> List[Project]:
    projects = self.projectService.ListAll()
    return [ProjectViewAdapter(project) for project in projects]


@AutoWire
class FreelancerFacade:

  freelancerRepository: FreelancerRepository
  freelancerQueryService: FreelancerQueryService
  profileService: ProfileService
  freelancerKnowledgeTreeService: FreelancerKnowledgeTreeService
  skillQueryService: SkillQueryService

  def ListPagFreelancers(
      self,
      pagination: int,
      limit: int = 10) -> List[Freelancer]:
    freelancers = None

  def getFreelancerProfile(
      self, email: str) -> Tuple[ProfileViewAdapter, Root]:
    freelancer = self.freelancerRepository.Find(Email(email))
    cv, files = self.profileService.GetProfile(freelancer)
    knowledges = self.freelancerQueryService.ListKnowledges(freelancer)
    skillTree = self.skillQueryService.LoadKnowledgeTree()
    tree = self.freelancerKnowledgeTreeService.MakeTree(
      knowledges.copy(), skillTree)
    return ProfileViewAdapter(freelancer, cv, files, knowledges), tree


@AutoWire
class FindFreelancersServiceFacade:
  freelancerExperienceService: FreelancerExperienceService
  freelancerQueryService: FreelancerQueryService
  profileService: ProfileService
  skillQueryService: SkillQueryService

  # TODO: El facade debería retornar una lista de adapters
  def ComputeRanks(
      self,
      name: str,
      businesses: List[str],
      projects: List[str],
      knowledges: List[str],
      pagination: int = 1,
      limit: int = 10) -> List[str]:

    allBusinesses = self.freelancerQueryService.ListAllBusinesses()
    allProjects = self.freelancerQueryService.ListAllProjects()
    allKnowledges = self.skillQueryService.ListAllKnowledges()

    # TODO: No está en el figma pero proximamente se deberá filtrar por CONDITION
    # TODO: neom no permite usar valores por defecto
    freelancerExperiences = self.freelancerQueryService.FindToComputeCompatibility(
      name, pagination, 10)

    businesses = set(businesses)
    projects = set(projects)
    knowledges = set(knowledges)

    criteria = FreelancerExperienceService.Criteria(businesses=businesses,
                                                    projects=projects,
                                                    knowledges=knowledges)

    counter = self.freelancerQueryService.CounterFreelancers(name)
    listCounter = list(range(1, math.ceil(counter / limit) + 1))

    ranks = self.freelancerExperienceService.ComputeRanks(
      freelancerExperiences, criteria)
    freelancerRankAdapters = [
      self._MakeFreelancerRankAdapter(rank) for rank in ranks]

    numberFreelancers = self.freelancerQueryService.CounterFreelancers()

    return allBusinesses, allProjects, allKnowledges, freelancerRankAdapters, listCounter, numberFreelancers

  def _MakeFreelancerRankAdapter(
      self, rank: FreelancerExperienceService.Rank) -> str:
    cv, files = self.profileService.GetProfile(rank.freelancer)
    return FreelancerRankViewAdapter(rank, cv, files)


@AutoWire
class DashboardFreelancersFacade:

  freelancerRepository: FreelancerRepository
  freelancerQueryService: FreelancerQueryService
  skillQueryService: SkillQueryService
  freelancerCountTreeService: FreelancerCountTreeService
  freelancerPeriodService: FreelancerPeriodService

  def Load(self, layers: List[bool], start: str,
           end: str) -> CountedTreeViewAdapter:

    # TODO: Usar un IntEnum
    # mapPeriod = {
    #   '0': FreelancerPeriodService.Yearly(),
    #   '1': FreelancerPeriodService.Monthly(),
    #   '2': FreelancerPeriodService.Weekly()
    # }

    #period = mapPeriod[periodKey]

    startDate = datetime.strptime(start, '%Y-%m-%d')
    endDate = datetime.strptime(end, '%Y-%m-%d')
    period = FreelancerPeriodService.Custom(startDate, endDate)

    #periodRate = self.freelancerPeriodService.GetChangeRate(period)
    freelancers = self.freelancerPeriodService.ListFreelancersByPeriod(period)
    periodRate = FreelancerPeriodService.RatePeriodResult(
      cantCurrentAffiliates=len(freelancers),
      cantPreviousAffiliates=0, rate=0, scale=0)

    skillTree = self.skillQueryService.LoadKnowledgeTree()
    countedTree = CountedTreeViewAdapter(skillTree).root

    for freelancer in freelancers:
      knowledges = self.freelancerQueryService.ListKnowledges(freelancer)
      freelancerShort = self.freelancerCountTreeService.FreelancerShort(
        freelancer.email.address, freelancer.name)
      self.freelancerCountTreeService.UpdateCount(
        countedTree, knowledges, freelancerShort, layers)

    return countedTree, periodRate


@AutoWire
class NewInitiativeServiceFacade:

  initiativeQueryService: InitiativeQueryService
  initiativeRepository: InitiativeRepository
  initiativeCreationService: InitiativeCreationService
  googleDriveService: GoogleDriveService

  def LoadInformation(self):
    return self.initiativeCreationService.ListCompanyWorkers()

  def CreateInitiative(self, initiativeDTO: QueryDict):
    accountCode = initiativeDTO['account']
    contactName = initiativeDTO['contact']
    workKind = initiativeDTO['workKind']
    name = initiativeDTO['name']
    goal = initiativeDTO['goal']
    amount = initiativeDTO['amount']
    submission = initiativeDTO['submission']
    successRate = initiativeDTO['successRate']

    submissionDate = datetime.strptime(submission, '%Y-%m-%d').date()

    contact = Contact(contactName)

    companyFolderInformation = self.initiativeCreationService.GetCompanyFolderInformation(
      CompanyCode(code=accountCode))
    initiativeCode = self.initiativeQueryService.FindNextInitiativeCode(
      companyFolderInformation.company.code)

    try:
      initiativeFolderId = self.googleDriveService.CreateInitiativeFolder(
        initiativeCode, name, companyFolderInformation.initiativeFolderId)
      initiative = Initiative(
        code=initiativeCode,
        company=companyFolderInformation.company,
        contact=contact,
        name=name,
        amount=amount,
        goal=goal,
        submission=submissionDate,
        workKind=Initiative.WorkKind[workKind],
        state=Initiative.State.FORTH_COMING,
        successRate=successRate,
        folderId=initiativeFolderId)
      self.initiativeRepository.Store(initiative)
    except BaseException:
      raise ValueError


@AutoWire
class InitiativeListFacade:
  initiativeQueryService: InitiativeQueryService

  def LoadInitiatives(self):
    initiatives = self.initiativeQueryService.ListForthComingAndDispatchedInitiatives()
    return [InitiativeViewAdapter(initiative) for initiative in initiatives]
