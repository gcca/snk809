import io
import os
from typing import List

from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from sinek.application.service import GoogleDriveService
from sinek.domain.model.freelancer import CV, File, GoogleId
from sinek.domain.model.initiative import InitiativeCode

PATH_SERVICE_ACCOUNT = os.path.join(
  settings.BASE_DIR,
  'sinek',
  'application',
  'service_account_creds.json')


class GoogleDriveServiceImpl(GoogleDriveService):

  GoogleDriveUpload = GoogleDriveService.GoogleDriveUpload

  def __init__(self):
    self.credentials = self._login()

  def UploadFreelancerCV(
      self,
      cvFile: CV,
      rootId: str = settings.LUCI_MAIN_FOLDER_ID) -> GoogleDriveUpload:
    folder = self._SearchFile(
      f"title = '{str(cvFile.freelancer.email)}' and parents in '{rootId}'")

    if not folder:
      folder_id = self._CreateFolder(str(cvFile.freelancer.email), rootId)
    else:
      folder_id = folder[0]['id']
    uploaded = self._UploadFile(cvFile, folder_id)

    return self.GoogleDriveUpload(googleId=uploaded['id'], name=cvFile.name)

  def UploadFreelancerPortfolio(
      self, files: List[File],
      rootId: str = settings.LUCI_MAIN_FOLDER_ID) -> List[GoogleDriveUpload]:
    folder = self._SearchFile(
      f"title = '{str(files[0].freelancer.email)}' and parents in '{rootId}'")

    if not folder:
      folder_id = self._CreateFolder(str(files[0].freelancer.email), rootId)
    else:
      folder_id = folder[0]['id']

    # TODO: Reemplazar por Bulk create de google drive API
    googleFiles = []
    for file in files:
      uploaded = self._UploadFile(file, folder_id)
      googleFile = self.GoogleDriveUpload(
        googleId=uploaded['id'], name=file.name)
      googleFiles.append(googleFile)

    return googleFiles

  def RemoveFreelancerUpload(self, googleId: GoogleId):
    self._RemoveFile(str(googleId))

  def CreateInitiativeFolder(
      self,
      initiativeCode: InitiativeCode,
      name: str,
      rootId: str) -> str:

    # TODO: Verificar si existe una carpeta llamada así y luego crear
    initiativeFolderId = self._CreateFolder(
      name=f'[{str(initiativeCode)}] {name}', id=rootId)

    self._CreateFolder(
      name=f'[{str(initiativeCode)}] Propuesta Neómada',
      id=initiativeFolderId)
    self._CreateFolder(
      name=f'[{str(initiativeCode)}] Documentos requerimiento',
      id=initiativeFolderId)
    self._CreateFolder(
      name=f'[{str(initiativeCode)}] Cotizaciones recibidas',
      id=initiativeFolderId)

    return initiativeFolderId

  def _login(self):
    # TODO: Crear excepciones
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
      PATH_SERVICE_ACCOUNT, ['https://www.googleapis.com/auth/drive'])
    return GoogleDrive(gauth)

  def _CreateFolder(
      self,
      name: str,
      id: str = settings.LUCI_MAIN_FOLDER_ID) -> str:
    folder = self.credentials.CreateFile(
      {'title': name, 'mimeType': 'application/vnd.google-apps.folder',
       'parents': [{'kind': 'drive#fileLink', 'id': id}]})
    folder.Upload()
    return folder['id']

  def _SearchFile(self, query: str) -> list:
    results = []

    file_match = self.credentials.ListFile({'q': query}).GetList()

    for file in file_match:
      results.append(file)

    return results

  def _UploadFile(self, file, idFolder):
    driveFile = self.credentials.CreateFile(
      {'parents': [{'kind': 'drive#fileLink', 'id': idFolder}]})
    driveFile['title'] = file.name
    driveFile.content = io.BytesIO(file.blob)
    driveFile.Upload()

    return driveFile

  def _DownloadFile(self, googleId: GoogleId) -> io.BytesIO:
    driveFile = self.credentials.CreateFile({'id': str(googleId)})
    driveFile.FetchContent()
    return driveFile.content

  def _RemoveFile(self, idFile):
    file = self.credentials.CreateFile({'id': idFile})
    file.Trash()  # hacia la papelera de reciclaje del gDrive file
    # file.Delete() lo elimina permanentemente
