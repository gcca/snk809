from sinek.interface.controller.account import UserIdRequiredMixin


class OnlyHunterMixin(UserIdRequiredMixin):
  permission_required = 'auth.im_hunter'


class HunterViewBase(OnlyHunterMixin):
  """This must be used for each hunter view to enforce permissions, validations
  and common members."""
