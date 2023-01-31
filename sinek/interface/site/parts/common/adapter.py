from typing import List, NamedTuple
from uuid import uuid1

from sinek.domain.model.freelancer import (
  CV,
  File,
  Freelancer,
  Knowledge as FreelancerKnowledge,
  Network,
  FullTime,
  HalfTime,
  Lancer,
  Talent)
from sinek.domain.model.skill import Root, Skill
from sinek.domain.service import FreelancerKnowledgeTreeService

__all__ = ['ProfileViewAdapter', 'SkillTreeViewAdapter']


class ProfileViewAdapter:
  """View adapter for a Freelancer Profile."""

  def __init__(self, freelancer: Freelancer, cvs: List[CV], files: List[File]):
    self.freelancer = freelancer
    self.cvs = cvs
    self.files = files

    self._networks = [Network(n.InferKind().name.lower(), str(n.url))
                      for n in freelancer.networks]

  @property
  def email(self) -> str:
    return str(self.freelancer.email)

  @property
  def name(self) -> str:
    return self.freelancer.name

  @property
  def phone(self) -> str:
    return self.freelancer.phone

  @property
  def phoneNumber(self) -> str:
    return self.freelancer.phone.number

  @property
  def networks(self) -> str:
    return self._networks

  @property
  def businesses(self) -> List[str]:
    return [tag.name for tag in self.freelancer.businesses]

  @property
  def projects(self) -> List[str]:
    return [tag.name for tag in self.freelancer.projects]

  @property
  def isTalent(self) -> bool:
    return isinstance(self.freelancer.condition, Talent)

  @property
  def isLancer(self) -> bool:
    return isinstance(self.freelancer.condition, Lancer)

  @property
  def minimum(self) -> str:
    if self.isTalent:
      return str(self.freelancer.condition.incomeRange[0])
    return None

  @property
  def maximum(self) -> str:
    if self.isTalent:
      return str(self.freelancer.condition.incomeRange[1])
    return None

  @property
  def modality(self) -> str:
    if self.isTalent:
      if self.freelancer.condition.modality == Talent.Modality.REMOTE:
        return '1'
      elif self.freelancer.condition.modality == Talent.Modality.HYBRID:
        return '2'
      elif self.freelancer.condition.modality == Talent.Modality.OFFICE:
        return '3'

  @property
  def disponibility(self) -> str:
    if self.isTalent:
      if self.freelancer.condition.disponibility == Talent.Disponibility.ONEWEEK:
        return '1'
      elif self.freelancer.condition.disponibility == Talent.Disponibility.TWOWEEKS:
        return '2'
      elif self.freelancer.condition.disponibility == Talent.Disponibility.THREEWEEKS:
        return '3'
      elif self.freelancer.condition.disponibility == Talent.Disponibility.ONEMONTH:
        return '4'
    return '0'

  @property
  def expectative(self) -> str:
    if self.isTalent:
      return self.freelancer.condition.expectative
    return ''

  @property
  def condition(self) -> str:
    if isinstance(self.freelancer.condition, FullTime):
      return 'Fulltime'
    elif isinstance(self.freelancer.condition, HalfTime):
      return 'Halftime'

  @property
  def experience(self) -> str:
    if not isinstance(self.freelancer.condition, HalfTime):
      return None
    if self.freelancer.condition.experience == HalfTime.Experience.LOW:
      return '1'
    elif self.freelancer.condition.experience == HalfTime.Experience.MEDIUM:
      return '2'
    elif self.freelancer.condition.experience == HalfTime.Experience.HIGH:
      return '3'

  @property
  def availability(self) -> str:
    if not isinstance(self.freelancer.condition, HalfTime):
      return 10
    if self.freelancer.condition.availability:
      return self.freelancer.condition.availability
    else:
      return 10

  @property
  def hasCVs(self) -> bool:
    return self.cvs != []

  @property
  def hasFiles(self) -> bool:
    return self.files != []

  @property
  def attachCVs(self) -> List[str]:
    return self.cvs

  @property
  def uniqueCV(self) -> CV:
    try:
      return self.cvs[0]
    except:
      return None

  @property
  def attachFiles(self) -> List[str]:
    return self.files

  # BORRAR***********************************************************
  @property
  def cvGooglePath(self):
    if self.cv.googleId.id:
      return f'https://drive.google.com/file/d/{str(self.cv.googleId)}/view?usp=drivesdk'

  @property
  def cvGoogleId(self):
    if self.cv.googleId.id:
      return str(self.cv.googleId)
  # ***********************************************************BORRAR

  @property
  def whatsappText(self) -> str:
    return f'{self.freelancer.phone.countryCode}{self.freelancer.phone.number}'

  @property
  def wouldChangeCountry(self) -> bool:
    return self.freelancer.acceptanceAvailability.wouldChangeCountry

  @property
  def wouldChangeCity(self) -> bool:
    return self.freelancer.acceptanceAvailability.wouldChangeCity

  @property
  def interviewAvailability(self) -> bool:
    return self.freelancer.acceptanceAvailability.interviewAvailability

  @property
  def jobSwitchTime(self) -> str:
    return self.freelancer.acceptanceAvailability.jobSwitchTime.name

  @property
  def writing(self) -> str:
    return self.freelancer.englishProficiency.writing.name

  @property
  def speaking(self) -> str:
    return self.freelancer.englishProficiency.speaking.name

  @property
  def roles(self) -> list:
    return [rol.name for rol in self.freelancer.roleInterests]

  @property
  def worklifePreferences(self) -> list:
    return [worklife.name for worklife in self.freelancer.worklifePreferences]

  @property
  def jobPreferences(self) -> list:
    return [job.name for job in self.freelancer.jobPreferences]


class Network(NamedTuple):
  name: str
  url: str


ScoredKnowledge = FreelancerKnowledgeTreeService.ScoredKnowledge
PremarkedKnowledge = FreelancerKnowledgeTreeService.PremarkedKnowledge
UnScoredKnowledge = FreelancerKnowledgeTreeService.UnScoredKnowledge
ScoredGroup = FreelancerKnowledgeTreeService.ScoredGroup
PremarkedGroup = FreelancerKnowledgeTreeService.PremarkedGroup


class SkillTreeViewAdapter:

  def __init__(self, root: Root):
    self.root = self.decorateSkillTreeAdapter(root)

  def decorateSkillTreeAdapter(self, root: Root) -> Root:
    tree = Root(key=uuid1().hex, name='knowledgeTree', children=[])
    code = 'A'
    for child in root.children:
      newChild = self._makeNodeAdapter(child, code)
      tree.children.append(newChild)
      code = chr(ord(code) + 1)
    return tree

  def _makeNodeAdapter(self, node: Skill, code: str) -> Skill:
    if isinstance(node, UnScoredKnowledge):
      return UnScoredKnowledgeViewAdapter(knowledge=node, orderCode=code)
    if isinstance(node, ScoredKnowledge):
      return ScoredKnowledgeViewAdapter(knowledge=node, orderCode=code)
    elif isinstance(node, PremarkedKnowledge):
      return PremarkedKnowledgeViewAdapter(knowledge=node, orderCode=code)
    else:
      scoredChild = False
      premarkedChild = False
      if isinstance(node, ScoredGroup):
        scoredChild = True
      if isinstance(node, PremarkedGroup):
        premarkedChild = True
      newGroup = ScoredGroup(key=node.key, name=node.name, children=[])
      addCode = 'A'
      for child in node.children:
        newChild = self._makeNodeAdapter(child, code + addCode)
        newGroup.children.append(newChild)
        addCode = chr(ord(addCode) + 1)
      return GroupViewAdapter(
        group=newGroup,
        scored=scoredChild,
        orderCode=code,
        premarked=premarkedChild)


class GroupViewAdapter():
  group: FreelancerKnowledgeTreeService.ScoredGroup
  scored: bool
  orderCode: str
  premarked: bool

  def __init__(self, group, scored, orderCode, premarked):
    self.group = group
    self.scored = scored
    self.orderCode = orderCode
    self.premarked = premarked

  @property
  def isKnowledge(self):
    return False

  @property
  def hasPremarkedChild(self):
    return self.premarked

  @property
  def hasScoredChild(self):
    return self.scored

  @property
  def hasScoredOrPremarkedChild(self):
    return self.premarked + self.scored

  @property
  def name(self):
    return self.group.name

  @property
  def children(self):
    return self.group.children

  @property
  def GetId(self):
    return self.group.key

  @property
  def code(self):
    return self.orderCode


class KnowledgeViewAdapter():
  knowledge: FreelancerKnowledgeTreeService.ScoredKnowledge
  orderCode: str

  def __init__(self, knowledge, orderCode):
    self.knowledge = knowledge
    self.orderCode = orderCode

  @property
  def isKnowledge(self):
    return True

  @property
  def isScored(self):
    return False

  @property
  def isPremarked(self):
    return False

  @property
  def isScoredOrPremarked(self):
    return False

  @property
  def isUnScoredOrPremarked(self):
    return False

  @property
  def name(self):
    return self.knowledge.name

  @property
  def score(self): ...

  @property
  def key(self):
    return self.knowledge.key

  @property
  def code(self):
    return self.orderCode

  @property
  def isBeginner(self):
    return False

  @property
  def isJunior(self):
    return False

  @property
  def isMiddle(self):
    return False

  @property
  def isSenior(self):
    return False


class UnScoredKnowledgeViewAdapter(KnowledgeViewAdapter):

  @property
  def score(self):
    return 0

  @property
  def isUnScoredOrPremarked(self):
    return True


class ScoredKnowledgeViewAdapter(KnowledgeViewAdapter):

  @property
  def isScored(self):
    return True

  @property
  def isScoredOrPremarked(self):
    return True

  @property
  def score(self):
    return self.knowledge.score.value

  @property
  def isBeginner(self):
    return self.knowledge.score == FreelancerKnowledge.Score.BEGINNER

  @property
  def isJunior(self):
    return self.knowledge.score == FreelancerKnowledge.Score.JUNIOR

  @property
  def isMiddle(self):
    return self.knowledge.score == FreelancerKnowledge.Score.MIDDLE

  @property
  def isSenior(self):
    return self.knowledge.score == FreelancerKnowledge.Score.SENIOR


class PremarkedKnowledgeViewAdapter(KnowledgeViewAdapter):

  @property
  def isPremarked(self):
    return True

  @property
  def isScoredOrPremarked(self):
    return True

  @property
  def isUnScoredOrPremarked(self):
    return True

  @property
  def score(self):
    return FreelancerKnowledge.Score.PREMARKED.value
