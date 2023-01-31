from datetime import datetime, timezone

from django.core.management.base import BaseCommand
from django.conf import settings
from neom.core.ioc import AutoWire

from sinek.domain.model.freelancer import Freelancer, FreelancerRepository, CVRepository, FileRepository
from sinek.application.service import GoogleDriveService


@AutoWire
class Command(BaseCommand):

  freelancerRepository: FreelancerRepository
  cvRepository: CVRepository
  fileRepository: FileRepository
  googleDriveService: GoogleDriveService

  help = 'Backup de archivos a Google Drive.'

  def handle(self, *unused_args, **options):

    freelancers = self.freelancerRepository.All()

    now = datetime.now(timezone.utc).strftime('%d/%m/%Y')

    backupFolderId = self.googleDriveService._CreateFolder(
      name=now, id=settings.LUCI_BACKUP_MAIN_FOLDER_ID)

    for freelancer in freelancers:
      self._CVMigration(freelancer, backupFolderId)
      self._FilesMigration(freelancer, backupFolderId)

    print('Backup finalizado')

  def _CVMigration(self, freelancer: Freelancer, folderId: str):
    cvs = self.cvRepository.FindBy(freelancer)
    temp = []
    for cv in cvs:
      temp.append(cv)
    cvs = temp
    if cvs:
      self.googleDriveService.UploadFreelancerPortfolio(cvs, folderId)

  def _FilesMigration(self, freelancer: Freelancer, folderId: str):
    files = self.fileRepository.FindBy(freelancer)
    temp = []
    for file in files:
      temp.append(file)
    files = temp
    if files:
      self.googleDriveService.UploadFreelancerPortfolio(files, folderId)
