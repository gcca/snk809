from collections import OrderedDict
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied, RequestAborted
from django.forms import Form
from django.http import (HttpRequest, HttpResponse, HttpResponseRedirect,
                         QueryDict)
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from neom.core.ioc import AutoWire, Wired, wire

from sinek.application.account import UserRoleService
from sinek.domain.model.freelancer import (Email, FreelancerNotFoundError,
                                           FreelancerRepository)
from sinek.interface.site import imgs
from sinek.interface.site.parts.account.forms import NewFreelancerForm

from .facade import FreelancerFacade


class SignInView(LoginView):
  template_name = 'desktop/account/signin.html'
  redirect_authenticated_user = True

  def get_context_data(self, **kwargs) -> dict:
    context = super().get_context_data(**kwargs)

    googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth'
    redirectUri = reverse('site:account:google-login')

    params = OrderedDict((
      ('response_type', 'code'),
      ('client_id', f'{settings.GOOGLE_OAUTH2_CLIENT_ID}'),
      ('redirect_uri', f'{settings.GOOGLE_OAUTH2_BASE_DOMAIN_URL}{redirectUri}'),
      ('prompt', 'select_account'),
      ('access_type', 'offline'),
      ('scope', ('https://www.googleapis.com/auth/userinfo.email'
                 '+https://www.googleapis.com/auth/userinfo.profile')),
    ))
    urlparams = urlencode(params, safe='+')
    context['google_url'] = f'{googleAuthUrl}?{urlparams}'

    context['imgs'] = imgs

    return context

  @wire
  def get_success_url(self, userRoleService: Wired[UserRoleService]):
    try:
      return userRoleService.ResolveDashboardUrl(self.request.user)
    except AttributeError:
      # TODO: log user bad signin
      raise PermissionDenied


@AutoWire
class SignUpView(FormView):
  freelancerRepository: FreelancerRepository
  userRoleService: UserRoleService

  template_name = 'desktop/account/signup.html'
  form_class = NewFreelancerForm
  success_url = reverse_lazy('site:account:signin')

  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect(self.userRoleService.ResolveDashboardUrl(request.user))
    return super(SignUpView, self).dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs) -> dict:
    context = super().get_context_data(**kwargs)

    googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth'
    redirectUri = reverse('site:account:google-login')

    params = OrderedDict((
      ('response_type', 'code'),
      ('client_id', f'{settings.GOOGLE_OAUTH2_CLIENT_ID}'),
      ('redirect_uri', f'{settings.GOOGLE_OAUTH2_BASE_DOMAIN_URL}{redirectUri}'),
      ('prompt', 'select_account'),
      ('access_type', 'offline'),
      ('scope', ('https://www.googleapis.com/auth/userinfo.email'
                 '+https://www.googleapis.com/auth/userinfo.profile')),
    ))
    urlparams = urlencode(params, safe='+')
    context['google_url'] = f'{googleAuthUrl}?{urlparams}'

    context['imgs'] = imgs

    return context

  def form_valid(self, form: Form) -> HttpResponse:
    context = super().get_context_data(form=form)

    username = form['username'].value()
    password = form['password'].value()
    credentials = {'username': username, 'password': password}

    try:
      email = Email(form['username'].value())
    except Exception:
      context['errorMessage'] = 'Correo inválido.'
      return self.render_to_response(context)

    try:
      self.freelancerRepository.Find(email)
      context['errorMessage'] = 'El correo ya se encuentra registrado.'
      return self.render_to_response(context)
    except FreelancerNotFoundError:
      pass

    try:
      freelancerFacade = FreelancerFacade()
      freelancerFacade.SignUp(form)
    # TODO: quitar Exception. Usar concreto
    except Exception as error:
      raise RequestAborted from error

    user = authenticate(self.request, **credentials)
    try:
      login(self.request, user)
    except ValueError:
      return redirect(reverse('site:account:signin'))

    redirectUrl = self.userRoleService.ResolveDashboardUrl(user)
    return redirect(redirectUrl)

    return super().form_valid(form)

  def form_invalid(self, form: Form):
    context = super().get_context_data(form=form)
    context['errorMessage'] = 'Debe completar todos los campo.'
    return self.render_to_response(context)


@AutoWire
class AuthViewBase(View):

  userRoleService: UserRoleService

  def processLogin(
      self,
      request: HttpRequest,
      credentials: dict) -> HttpResponseRedirect:
    user = authenticate(request, **credentials)
    try:
      login(request, user)
    except ValueError:
      return self.backToSignIn('Usuario no encontrado')

    redirectUrl = self.userRoleService.ResolveDashboardUrl(user)
    return redirect(redirectUrl)

  def validateArgument(self, queryDict: QueryDict, name: str) -> str:
    try:
      return queryDict[name]
    except KeyError:
      return self.backToSignIn(f'Missing {name}')

  # TODO: Falta usar message para notificar en HTML
  def backToSignIn(self, message: str) -> HttpResponseRedirect:
    return redirect(reverse('site:account:signin'))


class DefaultSignInView(AuthViewBase):
  def post(self, request):
    username = self.validateArgument(request.POST, 'username')
    password = self.validateArgument(request.POST, 'password')
    credentials = {'username': username, 'password': password}

    return self.processLogin(self.request, credentials)


class GoogleSignInView(AuthViewBase):
  def get(self, request):
    code = self.validateArgument(request.GET, 'code')
    credentials = {'code': code}

    return self.processLogin(self.request, credentials)


class ResetSessionView(TemplateView):
  template_name = "desktop/account/reset-session.html"
