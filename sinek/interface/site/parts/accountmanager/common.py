from sinek.interface.controller.account import UserIdRequiredMixin


class OnlyAccountManagerMixin(UserIdRequiredMixin):
  permission_required = 'auth.im_accountmanager'


class AccountManagerViewBase(OnlyAccountManagerMixin):
  """This must be used for each account manager view to enforce
  permissions, validations and common members."""
