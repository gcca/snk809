from django.contrib.auth import get_user_model
from django.db import models

from sinek.domain.model.freelancer import HalfTime, Talent, EnglishProficiency, AcceptanceAvailability

User = get_user_model()


class Staff(models.Model):
  name = models.CharField(max_length=128)


class Hunter(models.Model):
  name = models.CharField(max_length=128)


class AccountManager(models.Model):
  name = models.CharField(max_length=128)
  email = models.CharField(max_length=96, db_index=True)


class Project(models.Model):
  name = models.CharField(max_length=128)
  # TODO: Agregar account manager
  #accountmanager = models.OneToOneField(AccountManager, on_delete=models.CASCADE)


class Candidate(models.Model):
  class GenderId(models.IntegerChoices):
    Male = 0
    Female = 1

  name = models.CharField(max_length=128)
  email = models.CharField(max_length=128)
  gender = models.IntegerField(choices=GenderId.choices)


class CandidateDiscAnswers(models.Model):
  candidateId = models.CharField(max_length=128)
  number = models.IntegerField()
  plus = models.CharField(max_length=1)
  minus = models.CharField(max_length=1)


class CandidateTMMS24Answers(models.Model):
  candidateId = models.CharField(max_length=128)
  number = models.IntegerField()
  score = models.CharField(max_length=1)


class CandidateAnchorRecord(models.Model):
  candidateId = models.CharField(max_length=128)
  relevant1 = models.IntegerField()
  relevant2 = models.IntegerField()
  relevant3 = models.IntegerField()


class CandidateAnchorAnswers(models.Model):
  anchorRecord = models.ForeignKey(
    CandidateAnchorRecord,
    related_name='anchoranswers_set',
    on_delete=models.CASCADE)
  number = models.IntegerField()
  score = models.CharField(max_length=1)


class CandidateComplexRecord(models.Model):
  candidateId = models.CharField(max_length=128)
  start = models.DateTimeField()
  finish = models.DateTimeField()


class CandidateComplexAnswers(models.Model):
  complexRecord = models.ForeignKey(
    CandidateComplexRecord,
    related_name='complexanswers_set',
    on_delete=models.CASCADE)
  number = models.IntegerField()
  option_a = models.BooleanField()
  option_b = models.BooleanField()
  option_c = models.BooleanField()


class Freelancer(models.Model):
  class ConditionChoices(models.IntegerChoices):
    INITIAL = 0
    FULLTIME = 1
    HALFTIME = 2
    TALENT = 3
    TALENTANDFULLTIME = 4
    TALENTANDHALFTIME = 5

  condition = models.IntegerField(choices=ConditionChoices.choices)
  experience = models.IntegerField(
    choices=HalfTime.Experience.ToIntegerChoices().choices, null=True)
  availability = models.IntegerField(null=True)
  minimum = models.FloatField(null=True)
  maxIncome = models.FloatField(null=True)
  disponibility = models.IntegerField(
    choices=Talent.Disponibility.ToIntegerChoices().choices,
    default=Talent.Disponibility.NOSETTLED.value)
  modality = models.IntegerField(
    choices=Talent.Modality.ToIntegerChoices().choices,
    default=Talent.Modality.NOSETTLED.value)
  expectative = models.CharField(max_length=1024, null=True)
  country = models.CharField(max_length=64)
  location = models.CharField(max_length=128)
  email = models.CharField(max_length=96, db_index=True)
  name = models.CharField(max_length=128)
  phone = models.CharField(max_length=64)
  countryCode = models.IntegerField()
  isOnboarded = models.BooleanField()

  wouldChangeCountry = models.BooleanField(null=True)
  wouldChangeCity = models.BooleanField(null=True)
  interviewAvailability = models.BooleanField(null=True)
  jobSwitchTime = models.IntegerField(
    choices=AcceptanceAvailability.JobSwitchTime.ToIntegerChoices().choices,
    default=AcceptanceAvailability.JobSwitchTime.NOSETTLED)
  englishWritingSkills = models.IntegerField(
    choices=EnglishProficiency.EnglishSkill.ToIntegerChoices().choices,
    default=EnglishProficiency.EnglishSkill.NOSETTLED)
  englishSpeakingSkills = models.IntegerField(
    choices=EnglishProficiency.EnglishSkill.ToIntegerChoices().choices,
    default=EnglishProficiency.EnglishSkill.NOSETTLED)


class FreelancerTag(models.Model):
  name = models.CharField(max_length=128)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    abstract = True


class FreelancerJobTag(FreelancerTag):
  freelancer = models.ForeignKey(
    Freelancer,
    on_delete=models.CASCADE,
    related_name='jobPreferences')


class FreelancerWorklifeTag(FreelancerTag):
  freelancer = models.ForeignKey(
    Freelancer,
    on_delete=models.CASCADE,
    related_name='worklifePreferences')


class FreelancerBusinessTag(FreelancerTag):
  freelancer = models.ForeignKey(
    Freelancer,
    on_delete=models.CASCADE,
    related_name='businessTags')


class FreelancerProjectTag(FreelancerTag):
  freelancer = models.ForeignKey(
    Freelancer,
    on_delete=models.CASCADE,
    related_name='projectTags')


class FreelancerNetwork(models.Model):
  freelancer = models.ForeignKey(
    Freelancer, models.CASCADE, related_name='links')
  url = models.CharField(max_length=128)


class FreelancerSkill(models.Model):
  name = models.CharField(max_length=128)
  parent = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    related_name='children', null=True)
  

class FreelancerKnowledge(models.Model):
  freelancer = models.ForeignKey(
    Freelancer,
    on_delete=models.CASCADE,
    related_name='knowledges')
  skill = models.ForeignKey(FreelancerSkill, models.CASCADE)
  value = models.IntegerField()


class FreelancerRoleTag(FreelancerTag):
  freelancer = models.ForeignKey(
    Freelancer,
    on_delete=models.CASCADE,
    related_name='roleInterests')
  

class Upload(models.Model):
  class KindChoices(models.IntegerChoices):
    # TODO: Usar este enum desde el dominio
    OTHER = 0
    CV = 1

  googleId = models.CharField(max_length=256, null=True)
  binary = models.BinaryField(null=True)
  kind = models.IntegerField(choices=KindChoices.choices)
  created = models.DateTimeField()
  name = models.CharField(max_length=128, db_index=True)
  freelancer = models.ForeignKey(
    Freelancer, models.CASCADE, related_name='uploads', db_index=True)


class Role(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  hunter = models.OneToOneField(
    Hunter,
    on_delete=models.CASCADE,
    null=True,
    default=None)
  candidate = models.OneToOneField(
    Candidate, on_delete=models.CASCADE, null=True, default=None)
  accountManager = models.OneToOneField(
    AccountManager, on_delete=models.CASCADE, null=True, default=None)
  freelancer = models.OneToOneField(
    Freelancer, on_delete=models.CASCADE, null=True, default=None)
  staff = models.OneToOneField(
    Staff, on_delete=models.CASCADE, null=True, default=None)
