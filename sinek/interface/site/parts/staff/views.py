from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

from .common import StaffViewBase
from .forms import NewAccountManagerForm, NewHunterForm


class DashboardView(StaffViewBase, TemplateView):
  template_name = 'desktop/staff/dashboard.html'


class NewHunterView(StaffViewBase, FormView):
  template_name = 'desktop/staff/new-hunter.html'
  form_class = NewHunterForm
  success_url = reverse_lazy('site:staff:dashboard')

  def form_valid(self, form: NewHunterForm) -> HttpResponse:
    from .facade import StaffServiceFacade
    facade = StaffServiceFacade()
    facade.CreateHunter(form)
    return super().form_valid(form)


class NewAccountManagerView(StaffViewBase, FormView):
  template_name = 'desktop/staff/new-accountmanager.html'
  form_class = NewAccountManagerForm
  success_url = reverse_lazy('site:staff:dashboard')

  def form_valid(self, form: NewHunterForm) -> HttpResponse:
    from .facade import StaffServiceFacade
    facade = StaffServiceFacade()
    facade.CreateAccountManager(form)
    return super().form_valid(form)
