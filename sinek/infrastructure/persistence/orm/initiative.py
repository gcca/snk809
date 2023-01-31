import os
import re
from collections import namedtuple
from datetime import datetime
from typing import List, NamedTuple, Tuple

import gspread
from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials

from sinek.domain.model.initiative import (Company, CompanyCode,
                                           CompanyNotFoundError, Contact,
                                           Initiative, InitiativeCode,
                                           InitiativeNotFoundError,
                                           InitiativeQueryService,
                                           InitiativeRepository)
from sinek.domain.service import InitiativeCreationService

PATH_SERVICE_ACCOUNT = os.path.join(
  settings.BASE_DIR,
  'sinek',
  'application',
  'service_account_creds.json')
SAT_SPREADSHEET_ID = settings.SAT_SPREADSHEET_ID


class GoogleSheetService:
  def __init__(self, fileId: str, wsheets: List = []):
    creds = ServiceAccountCredentials.from_json_keyfile_name(
      PATH_SERVICE_ACCOUNT,
      ['https://spreadsheets.google.com/feeds',
       'https://www.googleapis.com/auth/spreadsheets',
       'https://www.googleapis.com/auth/drive'])
    self.client = gspread.authorize(creds)
    self.gsheet = self.client.open_by_key(fileId)

    wsheetDict = dict(wsheets)
    keys = list(wsheetDict.keys())
    Sheets = namedtuple('Sheets', keys)

    wsheetTitles = list(wsheetDict.values())
    self.sheet = Sheets._make([self.gsheet.worksheet(wsheet)
                               for wsheet in wsheetTitles])

  def UpdateRow(self, sheetName: str, valueList: List, row: int):
    cells = []
    for i, val in enumerate(valueList, start=1):
      cells.append(gspread.Cell(row=row, col=i, value=val))
    getattr(self.sheet, sheetName).update_cells(
      cells, value_input_option='USER_ENTERED')


class InitiativeGoogleSheetRepositoryORM(InitiativeRepository):

  def __init__(self):
    self.googleSheetService = GoogleSheetService(
      fileId=SAT_SPREADSHEET_ID, wsheets=[
        ('initiative', 'Iniciativas')])

  def All(self) -> List[Initiative]:
    initiativesSheet = self.googleSheetService.sheet.initiative.get_all_records(
      head=2)
    return [_makeFromSheetDict(initiativeDict)
            for initiativeDict in initiativesSheet]

  def Find(self, initiativeCode: InitiativeCode) -> Initiative:
    initiativeExist = self.googleSheetService.sheet.initiative.find(
      query=str(
        initiativeCode),
      in_column=5)
    if initiativeExist:
      initiativeSheet = self.googleSheetService.sheet.initiative.row_values(
        initiativeExist.row)
      return _makeFromSheetList(initiativeSheet)
    raise InitiativeNotFoundError

  def Store(self, initiative: Initiative):
    initiativeExist = self.googleSheetService.sheet.initiative.find(
      query=str(initiative.code), in_column=5)
    if initiativeExist:
      initiativeSheet = self.googleSheetService.sheet.initiative.row_values(
        initiativeExist.row)
    else:
      initiativeSheet = [''] * InitiativeHeaders.COLUMNS

    initiativeSheet[InitiativeHeaders.RUC.index] = initiative.company.ruc
    initiativeSheet[InitiativeHeaders.COMPANY_CODE.index] = str(
      initiative.company.code)
    initiativeSheet[InitiativeHeaders.COMPANY_NAME.index] = initiative.company.name
    initiativeSheet[InitiativeHeaders.COMPANY_KIND.index] = InitiativeToSheetList.companyKind[initiative.company.kind]

    initiativeSheet[InitiativeHeaders.CONTACT_NAME.index] = initiative.contact.name

    initiativeSheet[InitiativeHeaders.CODE.index] = str(initiative.code)
    initiativeSheet[InitiativeHeaders.NAME.index] = initiative.name
    initiativeSheet[InitiativeHeaders.GOAL.index] = initiative.goal
    initiativeSheet[InitiativeHeaders.WORKKIND.index] = InitiativeToSheetList.workKind[initiative.workKind]
    initiativeSheet[InitiativeHeaders.SUBMISSION.index] = initiative.submission.strftime(
      '%d/%m/%Y')
    initiativeSheet[InitiativeHeaders.AMOUNT.index] = initiative.amountSoles
    initiativeSheet[InitiativeHeaders.STATE.index] = InitiativeToSheetList.state[initiative.state]
    initiativeSheet[InitiativeHeaders.SUCCESS_RATE.index] = initiative.percentage
    #initiativeSheet[InitiativeHeaders.DUMMY_DATE.index] = InitiativeToSheetList.dummyDate(initiative.submission)
    #initiativeSheet[InitiativeHeaders.DAYS_AFTER_DISPATCHED.index] = InitiativeToSheetList.daysAfterDispatched(initiative.submission)
    initiativeSheet[InitiativeHeaders.DUMMY_DATE.index] = None
    initiativeSheet[InitiativeHeaders.DAYS_AFTER_DISPATCHED.index] = None
    initiativeSheet[InitiativeHeaders.DRIVE.index] = InitiativeToSheetList.driveURL(
      initiative.folderId)

    if initiativeExist:
      self.googleSheetService.UpdateRow(
        'initiative',
        valueList=initiativeSheet,
        row=initiativeExist.row)
    else:
      self.googleSheetService.sheet.initiative.append_row(
        initiativeSheet, value_input_option='USER_ENTERED')


class InitiativeHeaders:

  COLUMNS = 18

  class Header(NamedTuple):
    index: int
    label: str

  RUC = Header(0, 'RUC')
  COMPANY_CODE = Header(1, 'Código Cliente')
  COMPANY_NAME = Header(2, 'Nombre Cuenta')
  COMPANY_KIND = Header(3, 'Tipo')
  CODE = Header(4, 'Código iniciativa')
  CONTACT_NAME = Header(5, 'Solicitante')
  NAME = Header(6, 'Nombre clave')
  GOAL = Header(7, 'Objetivo de la iniciativa')
  DRIVE = Header(8, 'Carpeta preventa')
  WORKKIND = Header(9, 'Forma de trabajo')
  SUBMISSION = Header(10, 'Fecha Real o Proyectada del envio de propuesta')
  DAYS_AFTER_DISPATCHED = Header(12, 'Días de enviada la propuesta')
  AMOUNT = Header(13, 'Monto Real o Proyectado soles')
  STATE = Header(15, 'Estado de la iniciativa')
  DUMMY_DATE = Header(16, 'Dummy')
  SUCCESS_RATE = Header(17, 'Probabilidad')


class InitiativeToDomain:
  companyKind = {
    'New Business': Company.Kind.NEW_BUSINESS,
    'Cuenta': Company.Kind.ACCOUNT
  }

  workKind = {
    'Manpower': Initiative.WorkKind.MAN_POWER,
    'Proyecto digital': Initiative.WorkKind.DIGITAL_PRODUCT,
    'Bolsa de horas': Initiative.WorkKind.BAG_HOURS,
    'Reclutamiento': Initiative.WorkKind.RECRUITMENT,
    'Selección': Initiative.WorkKind.SELECTION,
    'R&S': Initiative.WorkKind.RS,
  }

  state = {
    '0. En preparación': Initiative.State.FORTH_COMING,
    '1. Enviada': Initiative.State.DISPATCHED,
    '2. Ganada': Initiative.State.EARNED,
    '3. Perdida': Initiative.State.LOST
  }

  @staticmethod
  def amountToDomain(amount: str) -> str:
    return re.sub(r'[^\d,]', '', amount).replace(',', '.')


class InitiativeToSheetList:
  companyKind = {
    Company.Kind.NEW_BUSINESS: 'New Business',
    Company.Kind.ACCOUNT: 'Cuenta',
  }

  workKind = {
    Initiative.WorkKind.MAN_POWER: 'Manpower',
    Initiative.WorkKind.DIGITAL_PRODUCT: 'Proyecto digital',
    Initiative.WorkKind.BAG_HOURS: 'Bolsa de horas',
    Initiative.WorkKind.RECRUITMENT: 'Reclutamiento',
    Initiative.WorkKind.SELECTION: 'Selección',
    Initiative.WorkKind.RS: 'R&S',
  }

  state = {
    Initiative.State.FORTH_COMING: '0. En preparación',
    Initiative.State.DISPATCHED: '1. Enviada',
    Initiative.State.EARNED: '2. Ganada',
    Initiative.State.LOST: '3. Perdida'
  }

  @staticmethod
  def driveURL(folderId: str) -> str:
    return f'https://drive.google.com/drive/folders/{folderId}'

  @staticmethod
  def daysAfterDispatched(submission: datetime) -> str:
    return f'=SIFECHA("{submission.strftime("%d/%m/%Y")}";HOY();"D")'

  @staticmethod
  def dummyDate(submission: datetime) -> str:
    return f'=SI("{submission.strftime("%d/%m/%Y")}"="";"";CONCATENAR(DERECHA(CONCATENAR("0";MES("{submission.strftime("%d/%m/%Y")}"));2);"-";TEXTO("{submission.strftime("%d/%m/%Y")}";"mmmm");"-";DERECHA(AÑO("{submission.strftime("%d/%m/%Y")}");2)))'


class CompanyToDomain:
  companyKind = {
    '0. Repesca': Company.Kind.NEW_BUSINESS,
    '0. Cuenta objetivo': Company.Kind.NEW_BUSINESS,
    '1. Emergente': Company.Kind.ACCOUNT,
    '2. Crecimiento': Company.Kind.ACCOUNT,
    '3. Madurez': Company.Kind.ACCOUNT,
    '4. Declive': Company.Kind.ACCOUNT,
    '5. Perdida': Company.Kind.ACCOUNT
  }

# TODO: Usar un Assembler


def _makeFromSheetList(initiativeList: List) -> Initiative:

  ruc = initiativeList[InitiativeHeaders.RUC.index]
  companyCode = CompanyCode(
    initiativeList[InitiativeHeaders.COMPANY_CODE.index])
  name = initiativeList[InitiativeHeaders.COMPANY_NAME.index]
  kind = initiativeList[InitiativeHeaders.COMPANY_KIND.index]

  company = Company(code=companyCode, ruc=ruc, name=name,
                    kind=InitiativeToDomain.companyKind[kind])

  initiativeCode = InitiativeCode(initiativeList[InitiativeHeaders.CODE.index])
  contact = Contact(name=initiativeList[InitiativeHeaders.CONTACT_NAME.index])
  nameKey = initiativeList[InitiativeHeaders.NAME.index]
  goal = initiativeList[InitiativeHeaders.GOAL.index]
  amountText = initiativeList[InitiativeHeaders.AMOUNT.index]
  amount = amount = InitiativeToDomain.amountToDomain(amountText)
  submissionDate = initiativeList[InitiativeHeaders.SUBMISSION.index]
  submission = datetime.strptime(submissionDate, '%d/%m/%Y').date()
  workKind = initiativeList[InitiativeHeaders.WORKKIND.index]
  state = initiativeList[InitiativeHeaders.STATE.index]
  successRate = initiativeList[InitiativeHeaders.SUCCESS_RATE.index][:-1]
  folderId = initiativeList[InitiativeHeaders.DRIVE.index]
  folderId = folderId.split('folders/')[1] if folderId else None

  return Initiative(
    code=initiativeCode,
    company=company,
    contact=contact,
    name=nameKey,
    amount=amount,
    goal=goal,
    submission=submission,
    workKind=InitiativeToDomain.workKind[workKind],
    state=InitiativeToDomain.state[state],
    successRate=successRate,
    folderId=folderId)


def _makeFromSheetDict(initiativeSheet: dict) -> Initiative:

  ruc = initiativeSheet[InitiativeHeaders.RUC.label]
  companyCode = CompanyCode(
    initiativeSheet[InitiativeHeaders.COMPANY_CODE.label])
  name = initiativeSheet[InitiativeHeaders.COMPANY_NAME.label]
  kind = initiativeSheet[InitiativeHeaders.COMPANY_KIND.label]

  company = Company(code=companyCode, ruc=ruc, name=name,
                    kind=InitiativeToDomain.companyKind[kind])

  initiativeCode = InitiativeCode(
    initiativeSheet[InitiativeHeaders.CODE.label])
  contact = Contact(name=initiativeSheet[InitiativeHeaders.CONTACT_NAME.label])
  nameKey = initiativeSheet[InitiativeHeaders.NAME.label]
  goal = initiativeSheet[InitiativeHeaders.GOAL.label]
  amountText = initiativeSheet[InitiativeHeaders.AMOUNT.label]
  amount = InitiativeToDomain.amountToDomain(amountText)
  submissionDate = initiativeSheet[InitiativeHeaders.SUBMISSION.label]
  submission = datetime.strptime(submissionDate, '%d/%m/%Y').date()
  workKind = initiativeSheet[InitiativeHeaders.WORKKIND.label]
  state = initiativeSheet[InitiativeHeaders.STATE.label]
  successRate = initiativeSheet[InitiativeHeaders.SUCCESS_RATE.label][:-1]
  folderId = initiativeSheet[InitiativeHeaders.DRIVE.label]
  try:
    folderId = folderId.split('folders/')[1] if folderId else None
  except BaseException:
    folderId = ''

  return Initiative(
    code=initiativeCode,
    company=company,
    contact=contact,
    name=nameKey,
    amount=amount,
    goal=goal,
    submission=submission,
    workKind=InitiativeToDomain.workKind[workKind],
    state=InitiativeToDomain.state[state],
    successRate=successRate,
    folderId=folderId)


class InitiativeGoogleSheetQueryService(InitiativeQueryService):

  def __init__(self):
    self.googleSheetService = GoogleSheetService(
      fileId=SAT_SPREADSHEET_ID,
      wsheets=[('contact', 'Contactos'),
               ('company', 'Empresas'),
               ('initiative', 'Iniciativas')])

  def ListForthComingAndDispatchedInitiatives(self) -> List[Initiative]:
    initiativesSheet = self.googleSheetService.sheet.initiative.get_all_records(
      head=2)
    return [_makeFromSheetDict(initiativeDict) for initiativeDict in initiativesSheet
            if initiativeDict[InitiativeHeaders.STATE.label] == InitiativeToSheetList.state[Initiative.State.FORTH_COMING]
            or initiativeDict[InitiativeHeaders.STATE.label] == InitiativeToSheetList.state[Initiative.State.DISPATCHED]]

  def FindCompany(
      self,
      companyCode: CompanyCode) -> InitiativeCreationService.CompanyFolderInformation:
    companyExist = self.googleSheetService.sheet.company.find(
      query=str(
        companyCode),
      in_column=3)
    if companyExist:
      companySheet = self.googleSheetService.sheet.company.row_values(
        companyExist.row)
      company = _makeCompanyFromList(companySheet)
      contactFolderId = companySheet[CompanyHeaders.CONTACT_FOLDER.index].split(
        'folders/')[1]
      initiativeFolderId = companySheet[CompanyHeaders.INITIATIVE_FOLDER.index].split(
        'folders/')[1]
      digitalProjectsFolderId = companySheet[CompanyHeaders.DIGITAL_PROJECTS_FOLDER.index].split(
        'folders/')[1]
      bagHoursFolderId = companySheet[CompanyHeaders.BAG_HOURS_FOLDER.index].split(
        'folders/')[1]

      return InitiativeCreationService.CompanyFolderInformation(
        company=company, contactFolderId=contactFolderId,
        initiativeFolderId=initiativeFolderId,
        digitalProjectsFolderId=digitalProjectsFolderId,
        bagHoursFolderId=bagHoursFolderId)

    raise CompanyNotFoundError

  def FindNextInitiativeCode(self, companyCode: CompanyCode) -> InitiativeCode:
    from datetime import date
    currentYear = str(date.today().year)
    lastTwoDigitsYear = currentYear[-2:]
    criteria = re.compile(
      '({})-INI-({}).*'.format(str(companyCode), lastTwoDigitsYear))
    matches = self.googleSheetService.sheet.initiative.findall(
      criteria, in_column=5)

    if matches:
      initiativeCompanySeries = [int(match.value[-3:]) for match in matches]
      serieAvailable = max(initiativeCompanySeries) + 1

    else:
      serieAvailable = 1

    return InitiativeCode.RemakeMake(
      companyCode=companyCode,
      year=lastTwoDigitsYear,
      serie=serieAvailable)

  def ListAllContacts(self) -> List[Tuple[CompanyCode, Contact]]:
    contactsSheet = self.googleSheetService.sheet.contact.get_all_records(
      head=1)
    return [_makeContactFromDict(contactSheet)
            for contactSheet in contactsSheet]

  def ListAllAccounts(self) -> List[Company]:
    accountsSheet = self.googleSheetService.sheet.company.get_all_records(
      head=1)
    return [_makeCompanyFromDict(accountSheet)
            for accountSheet in accountsSheet]


class ContactHeaders:

  COLUMNS = 10

  class Header(NamedTuple):
    index: int
    label: str

  COMPANY_RUC = Header(0, 'RUC Empresa')
  COMPANY_CODE = Header(1, 'Cod Empresa')
  NAME = Header(2, 'Nombre del contacto')
  KIND = Header(3, 'Estado del contacto')
  EMAIL = Header(4, 'Correo')
  WHATSAPP = Header(5, 'Whatsapp')
  JOB = Header(6, 'Cargo')
  BUYER = Header(7, 'Buyer persona')
  REGISTRATION_DATE = Header(8, 'Fecha ingreso')
  LINKEDIN = Header(9, 'Linkedin')


class CompanyHeaders:

  COLUMNS = 12

  class Header(NamedTuple):
    index: int
    label: str

  RUC = Header(0, 'RUC')
  NAME = Header(1, 'Nombre Comercial')
  CODE = Header(2, 'Codigo Empresa')
  DRIVE = Header(3, 'Carpeta de cliente')
  SIZE = Header(4, 'Tamaño de empresa')
  INDUSTRY = Header(5, 'Industria_LUCI')
  COUNTRY = Header(6, 'País')
  KIND = Header(11, 'Estado de la cuenta')
  CONTACT_FOLDER = Header(12, 'Carpeta de file de contactos')
  INITIATIVE_FOLDER = Header(13, 'Carpeta de Iniciativas')
  DIGITAL_PROJECTS_FOLDER = Header(14, 'Carpeta de proyectos digitales')
  BAG_HOURS_FOLDER = Header(15, 'Carpeta de bolsas de horas')
  STAFF_FOLDER = Header(16, 'Carpeta de Staff Augmentation')


def _makeContactFromDict(contactSheet: dict) -> Tuple[CompanyCode, Contact]:
  return CompanyCode(
    code=contactSheet[ContactHeaders.COMPANY_CODE.label]), Contact(
    name=contactSheet[ContactHeaders.NAME.label])


def _makeCompanyFromDict(accountSheet: dict) -> Company:

  ruc = accountSheet[CompanyHeaders.RUC.label]
  companyCode = CompanyCode(accountSheet[CompanyHeaders.CODE.label])
  name = accountSheet[CompanyHeaders.NAME.label]
  kind = accountSheet[CompanyHeaders.KIND.label]

  companyKind = CompanyToDomain.companyKind[kind]

  return Company(code=companyCode, ruc=ruc, name=name, kind=companyKind)


def _makeCompanyFromList(accountSheet: List) -> Company:

  ruc = accountSheet[CompanyHeaders.RUC.index]
  companyCode = CompanyCode(accountSheet[CompanyHeaders.CODE.index])
  name = accountSheet[CompanyHeaders.NAME.index]
  kind = accountSheet[CompanyHeaders.KIND.index]

  companyKind = CompanyToDomain.companyKind[kind]

  return Company(code=companyCode, ruc=ruc, name=name, kind=companyKind)
