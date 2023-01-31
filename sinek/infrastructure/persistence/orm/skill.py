# TODO: Remover al finalizar las pruebas
from typing import List, Set
from uuid import uuid1

from sinek.domain.model.freelancer import Tag
from sinek.domain.model.skill import (Group, Knowledge, Root,
                                      SkillQueryService, SkillRepository)
from sinek.infrastructure.persistence.orm.models import \
  FreelancerSkill as ORMFreelancerSkill


# TODO: actualizar modelo de datos
class SkillRepositoryORM(SkillRepository):
  ...


class SkillQueryServiceORM(SkillQueryService):

  def ListAllKnowledges(self) -> List[str]:
    ormKnowledges = ORMFreelancerSkill.objects.filter(children=None)
    return [ormKnowledge.name for ormKnowledge in ormKnowledges]

  def LoadKnowledgeTree(self) -> Root:
    root = Root(uuid1().hex, 'root', [])
    skillsORM = ORMFreelancerSkill.objects.filter(parent=None)
    for skillORM in skillsORM:
      root.children.append(_makeNode(skillORM))
    return root

  def LoadRolesKnowledgeTree(self, roles: Set[Tag]) -> Root:
    from sinek.infrastructure.persistence.orm.roletag_data import RootSkillDict
    root = Root(uuid1().hex, 'root', [])
    skillParents = {RootSkillDict[rol.name] for rol in roles}
    skillsORM = ORMFreelancerSkill.objects.filter(name__in=list(skillParents))
    for skillORM in skillsORM:
      root.children.append(_makeNode(skillORM))
    return root

def _makeNode(skillORM: ORMFreelancerSkill):
  if skillORM.children.all():
    children = [_makeNode(child) for child in skillORM.children.all()]
    return Group(skillORM.id, skillORM.name, children)
  return Knowledge(skillORM.id, skillORM.name)
