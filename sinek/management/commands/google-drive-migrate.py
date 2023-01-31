from django.core.management.base import BaseCommand
from neom.core.ioc import AutoWire

from sinek.domain.model.freelancer import Freelancer, FreelancerRepository, CVRepository, FileRepository, GoogleId
from sinek.application.service import GoogleDriveService


@AutoWire
class Command(BaseCommand):

  freelancerRepository: FreelancerRepository
  cvRepository: CVRepository
  fileRepository: FileRepository
  googleDriveService: GoogleDriveService

  help = 'Migrar archivos a Google Drive.'

  def handle(self, *unused_args, **options):

    freelancers = self.freelancerRepository.All()

    for freelancer in freelancers:
      self._CVMigration(freelancer)
      self._FilesMigration(freelancer)

      print(f'{str(freelancer.email)}: Migración terminada')

    print('Migración finalizada')

  def _CVMigration(self, freelancer: Freelancer):
    try:
      cv = self.cvRepository.Find(freelancer)

      if not cv.googleId.id:
        upload = self.googleDriveService.UploadFreelancerCV(cv)
        cv.googleId = GoogleId(id=upload.googleId)
        self.cvRepository.Store(cv)
    except BaseException:
      print(f'El freelancer {str(freelancer.email)} no tiene cv')

  def _FilesMigration(self, freelancer: Freelancer):
    files = self.fileRepository.FindBy(freelancer)
    temp = []
    for file in files:
      if not file.googleId.id:
        temp.append(file)
    files = temp
    if files:
      uploads = self.googleDriveService.UploadFreelancerPortfolio(files)
      for i in range(len(files)):
        files[i].googleId = GoogleId(id=uploads[i].googleId)
        self.fileRepository.Store(files[i])
