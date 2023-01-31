from typing import Optional

from django.core.management.base import (BaseCommand, CommandError,
                                         CommandParser)
from neom.core.ioc import AutoWire

from sinek.application.account import UserRoleService
from sinek.domain.model.staff import Staff, StaffRepository


@AutoWire
class Command(BaseCommand):

  staffRepository: StaffRepository
  userRoleService: UserRoleService

  help = 'Crear LUCI staff.'

  def add_arguments(self, parser: CommandParser):
    parser.add_argument('--name', '-n', required=True, help='Nombre del Staff')
    parser.add_argument(
      '--password',
      '-p',
      required=True,
      help='Contraseña del Staff')

  def handle(self, *unused_args, **options):
    name = options['name']
    password = options['password']

    staff = Staff(name=name)
    self.staffRepository.Store(staff)
    self.userRoleService.CreateUser(staff, password)
