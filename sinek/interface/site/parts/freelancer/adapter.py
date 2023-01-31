from typing import List

from sinek.domain.model.freelancer import CV, File, Freelancer, Knowledge
from sinek.interface.site.parts.common.adapter import ProfileViewAdapter as ProfileViewAdapterCommon

__all__ = ['ProfileViewAdapter']


class ProfileViewAdapter(ProfileViewAdapterCommon):

  def __init__(self, freelancer, cvs, files, knowledges):
    super().__init__(freelancer=freelancer, cvs=cvs, files=files)
    self.knowledges = knowledges

  @property
  def residence(self) -> str:
    return self.freelancer.residence

  @property
  def hasPremarkedKnowledge(self) -> bool:
    for knowledge in self.knowledges:
      if knowledge.score == Knowledge.Score.PREMARKED:
        return True
    return False
