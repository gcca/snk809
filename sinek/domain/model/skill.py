from abc import abstractmethod
from typing import List, Set

from neom.ddd.shared import Entity, Identity, Repository

from sinek.domain.model.freelancer import Tag


class Skill(Entity):
  key: Identity[str]
  name: str

  def GetId(self) -> int:
    return self.key

  # TODO: Agregar esta funcionalidad desde el NEOM
  def __eq__(self, other: Entity) -> bool:
    return all(getattr(self, name) == getattr(other, name)
               for name in self.__slots__)

  def __hash__(self):
    return hash(self.key)


class Group(Skill):
  children: List[Skill]


class Knowledge(Skill):
  pass


class Root(Group):
  pass


class SkillRepository(Repository):

  @abstractmethod
  def Store(self, skill: Skill):
    ...


class SkillQueryService:

  @abstractmethod
  def ListAllKnowledges(self) -> List[str]:
    ...

  @abstractmethod
  def LoadKnowledgeTree(self) -> Root:
    ...

  @abstractmethod
  def LoadRolesKnowledgeTree(self, roles: Set[Tag]) -> Root:
    ...
