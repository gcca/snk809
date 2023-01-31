from abc import abstractmethod
from typing import List

from neom.ddd.shared import Entity, Repository


class Project(Entity):
  name: str


class ProjectRepository(Repository):

  @abstractmethod
  def All(self) -> List[Project]:
    """ TODO: Raises: Repository.NotFoundError."""

  @abstractmethod
  def Store(self, project: Project):
    """ TODO: Raises: Repository.PersistenceError."""
