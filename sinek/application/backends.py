import random
import string
from typing import Optional
from uuid import uuid1

import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractBaseUser, User
from django.http import HttpRequest
from django.urls import reverse
from neom.core.ioc import Wireable, Wired

from sinek.application.account import UserRoleService
from sinek.domain.model.freelancer import (Email, Freelancer,
                                           FreelancerNotFoundError,
                                           FreelancerRepository)

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_ACCOUNT_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


@Wireable
class GoogleBackend(BaseBackend):

  freelancerRepository: Wired[FreelancerRepository]
  userRoleService: Wired[UserRoleService]

  def authenticate(
      self,
      request: HttpRequest,
      code: str) -> Optional[AbstractBaseUser]:

    try:
      access_token = self._GetAccessToken(code)
    except ValueError:
      return None

    try:
      name, email = self._GetAccountData(access_token)
    except ValueError as error:
      # TODO: Google Error
      raise ValueError('Access Token issues') from error

    freelancerEmail = Email(email)
    try:
      # TODO: Agregar función de Exists()
      self.freelancerRepository.Find(freelancerEmail)
      # TODO: Mostrar que el email ya se encuentra registrado
      # raise ERROR
    except FreelancerNotFoundError:
      initialFreelancer = Freelancer.CreateWithoutExperience(freelancerEmail,
                                                             name)
      self.freelancerRepository.Store(initialFreelancer)
      self.userRoleService.CreateUser(initialFreelancer, _CreatePassword())

    # TODO: Tener XService.GetUserForRole(freelancer)
    try:
      return User.objects.get(email=str(freelancerEmail))
    except User.DoesNotExist as error:
      raise RuntimeError('Unreachable code') from error

  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None

  def _GetAccessToken(self, code: str) -> str:

    domain = settings.GOOGLE_OAUTH2_BASE_DOMAIN_URL
    api_uri = reverse('site:account:google-login')
    redirect_uri = f'{domain}{api_uri}'

    data = {
      'code': code,
      'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
      'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
      'redirect_uri': redirect_uri,
      'grant_type': 'authorization_code'
    }

    response = requests.post(
      GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data, timeout=30)

    if not response.ok:
      raise ValueError('Failed to obtain access token from Google.')

    accessToken = response.json().get('access_token')

    return accessToken

  def _GetAccountData(self, accessToken: str) -> str:
    response = requests.get(GOOGLE_ACCOUNT_INFO_URL,
                            params={'access_token': accessToken},
                            timeout=30)

    if not response.ok:
      raise ValueError('Failed to obtain user info from Google.')

    account_info = response.json()
    name = account_info['name']
    email = account_info['email']

    return name, email


def _CreatePassword() -> str:
  googlePassword = list(uuid1().hex + string.ascii_lowercase)
  random.shuffle(googlePassword)
  return ''.join(googlePassword)
