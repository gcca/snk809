from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)


class UserIdRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
  """
  Use this class to avoid write `LoginRequiredMixin, PermissionRequiredMixin`
  parents when you create a view.
  """
  # TODO: improve all uses to allow only specify the user
