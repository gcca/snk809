from django.views.generic.base import TemplateView

from sinek.interface.site import imgs


class TermsAndConditionsView(TemplateView):
  template_name = 'desktop/legal-info/terms-and-conditions.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['imgs'] = imgs
    return context


class DataPolicyView(TemplateView):
  template_name = 'desktop/legal-info/data-policy.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['imgs'] = imgs
    return context


class CookiesPolicyView(TemplateView):
  template_name = 'desktop/legal-info/cookies-policy.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['imgs'] = imgs
    return context
