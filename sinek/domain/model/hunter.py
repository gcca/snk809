from abc import abstractmethod

from neom.ddd.shared import Repository

from .role import Role

# Hunter entity


class Hunter(Role):  # TODO: Hunter(Employee)
  name: str

  @staticmethod
  def IsHunter():
    return True


# Hunter Repository

class HunterRepository(Repository):

  @abstractmethod
  def Find(self, name: str) -> Hunter:
    """ TODO: Raises: Repository.NotFoundError."""

  @abstractmethod
  def Store(self, hunter: Hunter):
    """ TODO: Raises: Repository.PersistenceError."""
