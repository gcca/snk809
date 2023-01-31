from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from sinek.interface.site import imgs
from sinek.interface.site.parts.common.adapter import SkillTreeViewAdapter
from sinek.infrastructure.persistence.orm.worklifepreferences_data import INITIAL_WORKLIFE_PREFERENCES
from sinek.infrastructure.persistence.orm.jobpreferences_data import INITIAL_JOB_PREFERENCES


from .common import FreelancerViewBase
from .facade import ProfileServiceFacade
from .forms import (BusinessForm, NetworkForm, PersonalForm,
                    ProjectForm, UploadForm)


class ProfileWizardView(FreelancerViewBase, TemplateView):
  template_name = 'desktop/freelancer/profile-wizard.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    profileServiceFacade = ProfileServiceFacade()

    profile, businesses, projects, knowledgeTree = profileServiceFacade.Load(
      self.request.user.email)
    context.update({
      'profile': profile,
      'imgs': imgs,
      'personalForm': PersonalForm(initial={
        'name': profile.name,
        'countryCode': profile.residence.country,
        'phoneCountryCode': profile.phone.countryCode.name,
        'phone': profile.phoneNumber
      }),
      'networkForm': NetworkForm(),
      'businessForm': BusinessForm(),
      'projectForm': ProjectForm(),
      'businessList': businesses,
      'projectList': projects,
      'uploadForm': UploadForm(),
      # 'tree': knowledgeTree
      'tree': SkillTreeViewAdapter(knowledgeTree).root,
      'worklifePreferences': INITIAL_WORKLIFE_PREFERENCES,
      'jobPreferences': INITIAL_JOB_PREFERENCES
    })
    return context

class ProfileView(FreelancerViewBase, TemplateView):
  template_name = 'desktop/freelancer/profile.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    profileServiceFacade = ProfileServiceFacade()

    profile, businesses, projects, knowledgeTree = profileServiceFacade.Load(
      self.request.user.email)
    context.update({
      'profile': profile,
      'imgs': imgs,
      'personalForm': PersonalForm(initial={
        'name': profile.name,
        'countryCode': profile.residence.country,
        'phoneCountryCode': profile.phone.countryCode.name,
        'phone': profile.phoneNumber
      }),
      'networkForm': NetworkForm(),
      'businessForm': BusinessForm(),
      'projectForm': ProjectForm(),
      'businessList': businesses,
      'projectList': projects,
      'uploadForm': UploadForm(),
      # 'tree': knowledgeTree
      'tree': SkillTreeViewAdapter(knowledgeTree).root,
      'worklifePreferences': INITIAL_WORKLIFE_PREFERENCES,
      'jobPreferences': INITIAL_JOB_PREFERENCES,
    })
    return context
