from neom.core.ioc import Wired, wire
from neom.ddd.staff import Email

from sinek.application.account import UserRoleService
from sinek.domain.model.accountmanager import (
    AccountManager,
    AccountManagerRepository,
)
from sinek.domain.model.candidate import (
    Candidate,
    CandidateId,
    CandidateRepository,
)
from sinek.domain.model.freelancer import (
    AcceptanceAvailability,
    ConditionBuilder,
    EnglishProficiency,
    Freelancer,
    FreelancerRepository,
    HalfTime,
)
from sinek.domain.model.hunter import Hunter, HunterRepository
from sinek.domain.model.staff import Staff, StaffRepository


@wire
def populate(userRoleService: Wired[UserRoleService]):
    _CreateStaff(userRoleService)
    _CreateHunter(userRoleService)
    _CreateCandidates(userRoleService)
    _CreateAccountManager(userRoleService)
    _CreateFreelancer(userRoleService)
    # _CreateRandomFreelancers(numberFreelancers=5,userRoleService=userRoleService)


@wire
def _CreateStaff(
    userRoleService: UserRoleService, staffRepository: Wired[StaffRepository]
):
    staff = Staff(name="staff")
    staffRepository.Store(staff)
    userRoleService.CreateUser(staff, "staff")


@wire
def _CreateHunter(
    userRoleService: UserRoleService, hunterRepository: Wired[HunterRepository]
):
    hunter = Hunter(name="hunter demo")
    hunterRepository.Store(hunter)
    userRoleService.CreateUser(hunter, "hunter")


@wire
def _CreateCandidates(
    userRoleService: UserRoleService,
    candidateRepository: Wired[CandidateRepository],
):
    candidate = Candidate(
        candidateId=CandidateId("male@candidate.com"),
        name="Candidato",
        gender=Candidate.Gender.MALE,
    )
    candidateRepository.Store(candidate)
    userRoleService.CreateUser(candidate, "male")

    candidate = Candidate(
        candidateId=CandidateId("female@candidate.com"),
        name="Candidata",
        gender=Candidate.Gender.FEMALE,
    )
    candidateRepository.Store(candidate)
    userRoleService.CreateUser(candidate, "female")


@wire
def _CreateAccountManager(
    userRoleService: UserRoleService,
    accountManagerRepository: Wired[AccountManagerRepository],
):
    accountManager = AccountManager(
        name="accountmanager demo", email=Email("accountmanager@neomadas.com")
    )
    accountManagerRepository.Store(accountManager)
    userRoleService.CreateUser(accountManager, "manager")


@wire
def _CreateFreelancer(
    userRoleService: UserRoleService,
    freelancerRepository: Wired[FreelancerRepository],
):
    from sinek.domain.model.freelancer import (
        Email,
        Network,
        Phone,
        Residence,
        Tag,
        Url,
    )

    networks = [
        Network(Url("http://github.com/freelancer")),
        Network(Url("http://linkedin.com/freelancer")),
    ]
    email = Email("freelancer@neomadas.com")
    businesses = [Tag("Cementeras"), Tag("Diseño")]
    projects = [Tag("CMM"), Tag("ERP")]
    condition = (
        ConditionBuilder().AsHalfTime(5, HalfTime.Experience.HIGH).Build()
    )
    residence = Residence(location="Lima", country="Peru")
    phone = Phone(Phone.CountryCode.PER, "948157511")

    roleInterests = [Tag(name="Backend"), Tag("Devops")]
    acceptanceAvailability = AcceptanceAvailability(
        wouldChangeCountry=False,
        wouldChangeCity=True,
        interviewAvailability=True,
        jobSwitchTime=AcceptanceAvailability.JobSwitchTime.GT_12M,
    )
    englishProficiency = EnglishProficiency(
        writing=EnglishProficiency.EnglishSkill.ADVANCED,
        speaking=EnglishProficiency.EnglishSkill.BEGINNER,
    )
    worklifePreferences = [
        Tag(name="Que el trabajo no interfiera para nada en mi vida actual."),
        Tag(name="Tener la oportunidad de conocer nuevas personas."),
        Tag(
            name="Recibir constate feedback para saber si voy por buen camino."
        ),
    ]
    jobPreferences = [
        Tag(name="Donde puedo ser creativo y autónomo."),
        Tag(name="Estructurados y sistemáticos."),
    ]

    freelancer = Freelancer(
        name="Free Lancer",
        email=email,
        phone=phone,
        condition=condition,
        residence=residence,
        networks=networks,
        businesses=businesses,
        projects=projects,
        roleInterests=roleInterests,
        acceptanceAvailability=acceptanceAvailability,
        englishProficiency=englishProficiency,
        worklifePreferences=worklifePreferences,
        jobPreferences=jobPreferences,
        isOnboarded=False,
    )

    freelancerRepository.Store(freelancer)
    userRoleService.CreateUser(freelancer, "freelancer123")


@wire
def _CreateRandomFreelancers(
    numberFreelancers: int,
    userRoleService: UserRoleService,
    freelancerRepository: Wired[FreelancerRepository],
):
    import random

    from sinek.domain.model.freelancer import (
        Network,
        Phone,
        Residence,
        Tag,
        Url,
    )

    random.seed(a=None, version=2)

    businessesOptions = [
        "Requisitos",
        "Análisis",
        "Diseño",
        "Programación",
        "Pruebas",
        "Implementación",
        "Mantenimiento",
    ]
    projectsOptions = ["ERP", "CMM", "SAP", "ACDC", "ITIL", "PMBOK", "CISCO"]
    cityOptions = [
        "Lima",
        "Caracas",
        "Trujillo",
        "Santiago",
        "Montevideo",
        "La Paz",
        "Arequipa",
        "Ica",
        "Brasilia",
    ]
    countryOptions = [
        "Peru",
        "Brasil",
        "Chile",
        "Ecuador",
        "Uruguay",
        "Paraguay",
        "Venezuela",
        "Bolivia",
        "Argentina",
        "Colombia",
    ]
    nameOptions = [
        "Hugo",
        "Paco",
        "Luis",
        "Donald",
        "Deisy",
        "Clara",
        "Mickey",
        "Pluto",
        "Pedro",
        "Goofy",
    ]
    lastOptions = [
        "Blue",
        "Red",
        "Yellow",
        "Black",
        "Brown",
        "Green",
        "Pink",
        "White",
        "Orange",
        "Cyan",
    ]
    for number in range(numberFreelancers):
        networks = []
        if random.randint(0, 1):
            networks.append(Network(Url("http://github.com")))
        if random.randint(0, 1):
            networks.append(Network(Url("http://linkedin.com")))
        if random.randint(0, 1):
            networks.append(Network(Url("http://behance.com")))

        businesses = []
        for _ in range(random.randint(0, 5)):
            businesses.append(Tag(random.choice(businessesOptions)))

        projects = []
        for _ in range(random.randint(0, 5)):
            projects.append(Tag(random.choice(projectsOptions)))

        if random.randint(0, 1):
            condition = (
                ConditionBuilder()
                .AsHalfTime(5, HalfTime.Experience.HIGH)
                .Build()
            )
        else:
            condition = ConditionBuilder().AsFullTime().Build()

        residence = Residence(
            location=random.choice(cityOptions),
            country=random.choice(countryOptions),
        )

        freelancer = Freelancer(
            name=f"{random.choice(nameOptions)} {random.choice(lastOptions)}",
            email=f"freelancer{number}@neomadas.com",
            phone=Phone(Phone.CountryCode.PER, f"{number}12345{number}"),
            condition=condition,
            residence=residence,
            networks=networks,
            businesses=businesses,
            projects=projects,
        )
        freelancerRepository.Store(freelancer)
        userRoleService.CreateUser(freelancer, "123")

        from devtools.populators.skills import addRandomKnowledges

        addRandomKnowledges(f"freelancer{number}@neomadas.com")
