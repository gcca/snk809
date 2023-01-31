from abc import abstractmethod

from typing import List
from neom.ddd.shared import Service, Stuff

from sinek.domain.model.freelancer import CV, File, GoogleId
from sinek.domain.model.initiative import InitiativeCode


class GoogleDriveService(Service):

  class GoogleDriveUpload(Stuff):
    googleId: str
    name: str

    @property
    def path(self):
      return (f'https://drive.google.com/file/d/{self.googleId}/view?'
              'usp=drivesdk')

  @abstractmethod
  def UploadFreelancerCV(self, cvFile: CV) -> GoogleDriveUpload:
    return NotImplemented

  @abstractmethod
  def UploadFreelancerPortfolio(
      self, files: List[File]) -> List[GoogleDriveUpload]:
    return NotImplemented

  @abstractmethod
  def RemoveFreelancerUpload(self, googleId: GoogleId):
    return NotImplemented

  @abstractmethod
  def CreateInitiativeFolder(
      self,
      initiativeCode: InitiativeCode,
      name: str,
      rootId: str):
    return NotImplemented
