from sinek.interface.controller.account import UserIdRequiredMixin


class OnlyStaffMixin(UserIdRequiredMixin):
  permission_required = 'auth.im_staff'


class StaffViewBase(OnlyStaffMixin):
  """This must be used for each staff view to enforce permissions, validations
  and common members."""
