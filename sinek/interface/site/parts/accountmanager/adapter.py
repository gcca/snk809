from typing import List, Set
from uuid import uuid1

from sinek.domain.model.freelancer import CV, File, FullTime
from sinek.domain.model.project import Project
from sinek.domain.model.skill import Root, Group, Skill, Knowledge
from sinek.domain.service import FreelancerExperienceService
from sinek.interface.site.parts.common.adapter import ProfileViewAdapter
from sinek.domain.model.initiative import Initiative

__all__ = ['ProjectViewAdapter', 'FreelancerRankViewAdapter']


class ProjectViewAdapter:
  """ View adapter for a Project """

  def __init__(self, project: Project):
    self.project = project

  @property
  def projectName(self) -> str:
    return self.project.name


class FreelancerRankViewAdapter(ProfileViewAdapter):

  NOCOMPATIBILITY_LABEL = [0]

  def __init__(
      self,
      rank: FreelancerExperienceService.Rank,
      cv: CV,
      files: List[File]):
    super().__init__(rank.freelancer, cv, files)
    self.rank = rank

  @property
  def isFulltime(self) -> bool:
    return isinstance(self.freelancer.condition, FullTime)

  @property
  def hasExperience(self) -> bool:
    for network in self.networks:
      if network.name == "linkedin":
        return True
    if self.hasCVs:
      return True
    return False

  @property
  def businessCompatibility(self) -> List[str]:
    return self.NOCOMPATIBILITY_LABEL if len(
      self.rank.businessMatch) == 0 else self.rank.businessMatch

  @property
  def projectsCompatibility(self) -> List[str]:
    return self.NOCOMPATIBILITY_LABEL if len(
      self.rank.projectMatch) == 0 else self.rank.projectMatch

  @property
  def knowledgeCompatibility(self) -> List[str]:
    return self.NOCOMPATIBILITY_LABEL if len(
      self.rank.knowledgeMatch) == 0 else self.rank.knowledgeMatch


class CountedTreeViewAdapter:

  def __init__(self, root: Root):
    self.root = self.decorateSkillTreeAdapter(root)

  def decorateSkillTreeAdapter(self, root: Root) -> Root:
    tree = Root(key=uuid1(), name='knowledgeTree', children=[])
    code = 'A'
    for child in root.children:
      newChild = self._makeNodeAdapter(child, code)
      tree.children.append(newChild)
      code = chr(ord(code) + 1)
    return tree

  def _makeNodeAdapter(self, node: Skill, code: str) -> Skill:
    if isinstance(node, Knowledge):
      return CountedKnowledgeViewAdapter(knowledge=node, orderCode=code)

    newGroup = Group(key=node.key, name=node.name, children=[])
    addCode = 'A'
    for child in node.children:
      newChild = self._makeNodeAdapter(child, code + addCode)
      newGroup.children.append(newChild)
      addCode = chr(ord(addCode) + 1)
    return CountedGroupViewAdapter(group=newGroup, orderCode=code)


class CountedGroupViewAdapter():
  group: Group
  scored: bool
  orderCode: str
  freelancerLevels: List[Set[int]]
  freelancerResult: Set[int]

  def __init__(self, group, orderCode):
    self.group = group
    self.scored = False
    self.orderCode = orderCode
    self.freelancerLevels = [set(), set(), set(), set()]
    self.freelancerResult = set()

  @property
  def hasScoredChild(self):
    return self.scored

  @property
  def name(self):
    return self.group.name

  @property
  def children(self):
    return self.group.children

  @property
  def GetId(self):
    return id(self)

  @property
  def code(self):
    return self.orderCode

  @property
  def counts(self):
    return [len(freelancerSet) for freelancerSet in self.freelancerLevels]

  @property
  def count(self):
    return len(self.freelancerResult)

  @property
  def freelancersCount(self):
    return self.freelancerLevels

  @property
  def freelancers(self):
    return self.freelancerResult


class CountedKnowledgeViewAdapter():
  knowledge: Knowledge
  orderCode: str
  freelancerLevels: List[Set[int]]
  freelancerResult: Set[int]

  def __init__(self, knowledge, orderCode):
    self.knowledge = knowledge
    self.orderCode = orderCode
    self.freelancerLevels = [set(), set(), set(), set()]
    self.freelancerResult = set()

  @property
  def isKnowledge(self):
    return True

  @property
  def name(self):
    return self.knowledge.name

  @property
  def code(self):
    return self.orderCode

  @property
  def scored(self):
    if self.count > 0:
      return True
    return False

  @property
  def counts(self):
    return [len(freelancerSet) for freelancerSet in self.freelancerLevels]

  @property
  def count(self):
    return len(self.freelancerResult)

  @property
  def freelancersCount(self):
    return self.freelancerLevels

  @property
  def freelancers(self):
    return self.freelancerResult


class InitiativeViewAdapter:
  initiative: Initiative

  def __init__(self, initiative: Initiative):
    self.initiative = initiative

  @property
  def isKnowledge(self):
    return True

  @property
  def code(self):
    return str(self.initiative.code)

  @property
  def company(self):
    return self.initiative.company.name

  @property
  def companyCode(self):
    return str(self.initiative.company.code)

  @property
  def contact(self):
    return self.initiative.contact.name

  @property
  def amount(self):
    return self.initiative.amount

  @property
  def name(self):
    return self.initiative.name

  @property
  def successRate(self):
    return self.initiative.successRate

  @property
  def goal(self):
    return self.initiative.goal

  @property
  def folderId(self):
    return self.initiative.folderId

  @property
  def workKind(self):
    mapKind = {
      Initiative.WorkKind.MAN_POWER: 'Man Power',
      Initiative.WorkKind.DIGITAL_PRODUCT: 'Proyecto Digital',
      Initiative.WorkKind.BAG_HOURS: 'Bolsa de Horas',
      Initiative.WorkKind.RECRUITMENT: 'Reclutamiento',
      Initiative.WorkKind.SELECTION: 'Selección',
      Initiative.WorkKind.RS: 'R & S',
    }
    return mapKind.get(self.initiative.workKind, '')

  @property
  def workKindCode(self):
    mapKind = {
      Initiative.WorkKind.MAN_POWER: 'MP',
      Initiative.WorkKind.DIGITAL_PRODUCT: 'DP',
      Initiative.WorkKind.BAG_HOURS: 'BH',
      Initiative.WorkKind.RECRUITMENT: 'RC',
      Initiative.WorkKind.SELECTION: 'SL',
      Initiative.WorkKind.RS: 'RS',
    }
    return mapKind.get(self.initiative.workKind, '')

  @property
  def state(self):
    mapKind = {
      Initiative.State.FORTH_COMING: '0. En preparación',
      Initiative.State.DISPATCHED: '1. Enviada',
      Initiative.State.EARNED: '2. Ganada',
      Initiative.State.LOST: '3. Perdida'
    }
    return mapKind.get(self.initiative.state, '')

  @property
  def stateCode(self):
    mapKind = {
      Initiative.State.FORTH_COMING: 'FC',
      Initiative.State.DISPATCHED: 'D',
      Initiative.State.EARNED: 'E',
      Initiative.State.LOST: 'L'
    }
    return mapKind.get(self.initiative.state, '')

  @property
  def driveURL(self):
    return f'https://drive.google.com/drive/folders/{self.initiative.folderId}'

  @property
  def submissionDate(self):
    return self.initiative.submission.strftime('%d/%m/%Y')

  @property
  def submissionDateRead(self):
    return self.initiative.submission.strftime('%Y-%m-%d')
