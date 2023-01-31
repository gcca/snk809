from abc import abstractmethod

from neom.ddd.shared import Repository

from .role import Role

# Staff entity


class Staff(Role):
  name: str

  @staticmethod
  def IsStaff():
    return True


# Staff Repository

class StaffRepository(Repository):

  @abstractmethod
  def Store(self, staff: Staff):
    """ TODO: Raises: Repository.PersistenceError."""
