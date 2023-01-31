from abc import abstractmethod
from datetime import datetime, timezone

from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from neom.core.ioc import AutoWire

from sinek.domain.model.freelancer import (CVRepository, Email, FileRepository,
                                           Freelancer, FreelancerNotFoundError,
                                           FreelancerRepository)
from sinek.interface.site import imgs
from sinek.interface.site.parts.common.adapter import SkillTreeViewAdapter
from sinek.domain.model.initiative import (InitiativeRepository,
  InitiativeQueryService, Initiative, InitiativeCode, Contact, CompanyCode)

from .common import AccountManagerViewBase
from .facade import (
  FindFreelancersServiceFacade,
  FreelancerFacade,
  InitiativeListFacade,
  ProjectFacade,
  DashboardFreelancersFacade,
  NewInitiativeServiceFacade)
from .forms import ProjectForm
from .adapter import InitiativeViewAdapter


class DashboardView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/dashboard.html'

  def get_context_data(self, **kwargs):
    projectFacade = ProjectFacade()
    context = super().get_context_data(**kwargs)

    projects = projectFacade.ListAllProjects()
    context['projects'] = projects
    return context


class CreateProjectView(AccountManagerViewBase, FormView):
  template_name = 'desktop/accountmanager/create-project.html'
  form_class = ProjectForm
  success_url = reverse_lazy('site:accountmanager:dashboard')

  def form_valid(self, form):
    projectFacade = ProjectFacade()
    # TODO: Agregar datos para agregar account manager como FK
    projectFacade.CreateProject(form)
    return super().form_valid(form)


class FreelancerListView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/freelancer-list.html'

  def get_context_data(self, **kwargs):
    findFreelancersServiceFacade = FindFreelancersServiceFacade()
    context = super().get_context_data(**kwargs)

    allBusinesses, allProjects, allKnowledges, freelancerRankAdapters,\
      paginationList, numberFreelancers = findFreelancersServiceFacade.\
        ComputeRanks('', [], [], [], 1)

    context['managerEmail'] = self.request.user.email

    context['businesses'] = allBusinesses
    context['projects'] = allProjects
    context['knowledges'] = allKnowledges

    context['imgs'] = imgs
    context['paginations'] = paginationList
    context['currentPage'] = 1
    context['freelancers'] = freelancerRankAdapters
    context['numberFreelancers'] = numberFreelancers
    context['numberResults'] = numberFreelancers

    return context

  def post(self, request, *args, **kwargs):
    findFreelancersServiceFacade = FindFreelancersServiceFacade()
    context = self.get_context_data(**kwargs)

    name = request.POST['name']
    selectedBusinesses = request.POST.getlist('businesses')
    selectedProjects = request.POST.getlist('projects')
    selectedKnowledges = request.POST.getlist('knowledges')
    currentPage = int(request.POST['page'])

    allBusinesses, allProjects, allKnowledges, freelancerRankAdapters,\
      paginationList, numberFreelancers = findFreelancersServiceFacade.\
        ComputeRanks(name, selectedBusinesses, selectedProjects,
          selectedKnowledges, currentPage)

    context['freelancerName'] = name
    context['selectedBusinesses'] = selectedBusinesses
    context['selectedProjects'] = selectedProjects
    context['selectedKnowledges'] = selectedKnowledges

    context['businesses'] = allBusinesses
    context['projects'] = allProjects
    context['knowledges'] = allKnowledges
    context['imgs'] = imgs
    context['paginations'] = paginationList
    context['currentPage'] = currentPage
    context['freelancers'] = freelancerRankAdapters
    context['numberResults'] = numberFreelancers

    return self.render_to_response(context)


class FreelancerInfoView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/freelancer-info.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    email = self.kwargs['email']
    freelancerFacade = FreelancerFacade()

    profile, knowledgeTree = freelancerFacade.getFreelancerProfile(email)

    context.update({
      'managerEmail': self.request.user.email,
      'profile': profile,
      'imgs': imgs,
      'tree': SkillTreeViewAdapter(knowledgeTree).root
    })

    return context


@AutoWire
class UploadView(AccountManagerViewBase, View):

  freelancerRepository: FreelancerRepository

  def get(self, request, *args, **kwargs):
    freelancer = self._getFreelancer(self.kwargs['email'])
    return self.Update(freelancer, request, args, kwargs)

  @abstractmethod
  def Update(self, freelancer, *args, **kwargs):
    raise NotImplementedError()

  def _getFreelancer(self, username: str) -> Freelancer:
    email = Email(username)
    try:
      freelancer = self.freelancerRepository.Find(email)
    except FreelancerNotFoundError as error:
      raise Http404('Invalid freelancer email') from error

    return freelancer


@AutoWire
class FileOpenView(UploadView):

  fileRepository: FileRepository

  def Update(self, freelancer: Freelancer, request, *args, **kwargs):
    fileName = self.kwargs['fileName']
    try:
      file = self.fileRepository.Find(freelancer, fileName)
    except BaseException:
      return FileNotFoundError

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    response.write(file.blob)

    return response


@AutoWire
class CVOpenView(UploadView):

  cvRepository: CVRepository

  def Update(self, freelancer: Freelancer, request, *args, **kwargs):
    try:
      cv = self.cvRepository.Find(freelancer)
    except BaseException:
      return FileNotFoundError

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.name}"'
    response.write(cv.blob)

    return response


class FreelancerDashboardView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/dashboard-freelancer.html'

  def get_context_data(self, **kwargs):
    today = datetime.now(timezone.utc)
    start = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')
    context = super().get_context_data(**kwargs)
    dashboardFreelancersFacade = DashboardFreelancersFacade()
    countedTree, periodRate = dashboardFreelancersFacade.Load(
      (False, False, False, True), start, end)

    context.update({
      'start': start,
      'end': end,
      'tree': countedTree,
      'layer1': False,
      'layer2': False,
      'layer3': False,
      'layer4': True,
      'periodRate': periodRate,
      'imgs': imgs
    })

    return context

  def post(self, request, *args, **kwargs):
    dashboardFreelancersFacade = DashboardFreelancersFacade()
    #periodKey = request.POST['period']
    start = request.POST['start']
    end = request.POST['end']
    layer1 = True if request.POST.get('tree-option-1', False) else False
    layer2 = True if request.POST.get('tree-option-2', False) else False
    layer3 = True if request.POST.get('tree-option-3', False) else False
    layer4 = True if request.POST.get('tree-option-4', False) else False

    countedTree, periodRate = dashboardFreelancersFacade.Load(
      layers=(layer1, layer2, layer3, layer4), start=start, end=end)

    context = {
      'start': start,
      'end': end,
      # 'period': periodKey,
      'layer1': layer1,
      'layer2': layer2,
      'layer3': layer3,
      'layer4': layer4,
      'tree': countedTree,
      'periodRate': periodRate,
      'imgs': imgs
    }

    return self.render_to_response(context)


@AutoWire
class InitiativeListView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/initiative-list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    initiativeListFacade = InitiativeListFacade()
    initiatives = initiativeListFacade.LoadInitiatives()

    context['initiatives'] = initiatives
    context['imgs'] = imgs

    return context


@AutoWire
class NewInitiativeView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/new-initiative.html'

  initiativeQueryService: InitiativeQueryService

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    newInitiativeFacade = NewInitiativeServiceFacade()

    companyWorkers = newInitiativeFacade.LoadInformation()

    workKindChoices = (
      (Initiative.WorkKind.DIGITAL_PRODUCT.name, 'Proyecto digital'),
      (Initiative.WorkKind.BAG_HOURS.name, 'Bolsa de horas'),
      (Initiative.WorkKind.MAN_POWER.name, 'Manpower'),
      (Initiative.WorkKind.RECRUITMENT.name, 'Reclutamiento'),
      (Initiative.WorkKind.SELECTION.name, 'Selección'),
      (Initiative.WorkKind.RS.name, 'R&S'),
    )

    context['companyWorkers'] = companyWorkers
    context['workKinds'] = workKindChoices
    context['imgs'] = imgs

    return context

  def post(self, request):
    newInitiativeFacade = NewInitiativeServiceFacade()

    newInitiativeFacade.CreateInitiative(request.POST)

    return redirect(reverse('site:accountmanager:initiative-list'))


@AutoWire
class QuotationView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/quotation.html'

  initiativeRepository: InitiativeRepository

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    initiativeId = self.kwargs['initiativeCode']
    initiativeCode = InitiativeCode(code=initiativeId)

    initiativeFounded = self.initiativeRepository.Find(initiativeCode)

    initiative = InitiativeViewAdapter(initiativeFounded)

    statesChoices = (
      (Initiative.State.FORTH_COMING.name, '0. En preparación'),
      (Initiative.State.DISPATCHED.name, '1. Enviada'),
      (Initiative.State.EARNED.name, '2. Ganada'),
      (Initiative.State.LOST.name, '3. Perdida'),
    )

    context['initiative'] = initiative
    context['states'] = statesChoices
    context['imgs'] = imgs

    return context

  def post(self, request):
    # TODO: Pensar lógica de la cotización
    return redirect(reverse('site:accountmanager:initiative-list'))


@AutoWire
class QuotationSectionView(AccountManagerViewBase, TemplateView):
  template_name = 'desktop/accountmanager/quotation.html'

  initiativeQueryService: InitiativeQueryService
  initiativeRepository: InitiativeRepository

  def post(self, request):
    self.Update(request.POST)
    return redirect(reverse('site:accountmanager:initiative-list'))

  @abstractmethod
  def Update(self, request: QueryDict):
    raise NotImplementedError()


class InitiativeUpdateView(QuotationSectionView):

  def Update(self, request: QueryDict):
    initiativeId = request['initiativeCode']
    accountCode = request['account']
    contactName = request['contact']
    workKind = request['workKind']
    folderId = request['folderId']
    name = request['name']
    goal = request['goal']
    state = request['state']
    amount = request['amount']
    submission = request['submission']
    successRate = request['successRate']

    submissionDate = datetime.strptime(submission, '%Y-%m-%d').date()

    contact = Contact(contactName)
    companyFolderInformation = self.initiativeQueryService.FindCompany(
      CompanyCode(
        code=accountCode))

    initiativeCode = InitiativeCode(code=initiativeId)

    initiative = Initiative(
      code=initiativeCode,
      company=companyFolderInformation.company,
      contact=contact,
      name=name,
      amount=amount,
      goal=goal,
      submission=submissionDate,
      workKind=Initiative.WorkKind[workKind],
      state=Initiative.State[state],
      successRate=successRate,
      folderId=folderId)

    self.initiativeRepository.Store(initiative)
