from typing import List

from neom.core.ioc import Wired, wire

from sinek.domain.model.freelancer import FreelancerCommandService

# TODO: remover esto, usar el repositorio.store
from sinek.infrastructure.persistence.orm.models import FreelancerSkill


def populate():
    # allSkills()
    # TODO: Borrar al finalizar las pruebas
    fewSkills()
    addKnowledges()


@wire
def addKnowledges(freelancerCommandService: Wired[FreelancerCommandService]):
    from sinek.domain.model.freelancer import Knowledge
    from sinek.infrastructure.persistence.orm.models import Freelancer

    freelancer = Freelancer.objects.get(email="freelancer@neomadas.com")
    freelancerCommandService.StoreKnowledge(freelancer, Knowledge("Naming", 1))
    freelancerCommandService.StoreKnowledge(
        freelancer, Knowledge("Diseño de tarjetas de presentación", 2)
    )
    freelancerCommandService.StoreKnowledge(
        freelancer, Knowledge("Diseño en 3D", 4)
    )
    freelancerCommandService.StoreKnowledge(
        freelancer, Knowledge("Modelado en 3D", 3)
    )
    freelancerCommandService.StoreKnowledge(
        freelancer, Knowledge("Videojuegos publicitarios 3D", 4)
    )
    freelancerCommandService.StoreKnowledge(
        freelancer, Knowledge("Escritura del curriculum vitae", 2)
    )
    freelancerCommandService.StoreKnowledge(
        freelancer, Knowledge("Contenido de sitio web", 3)
    )
    freelancerCommandService.StoreKnowledge(
        freelancer, Knowledge("Artículos y publicaciones de blog", 1)
    )


def addRandomKnowledges(email: str):
    import random

    from sinek.infrastructure.persistence.orm.models import Freelancer
    from sinek.infrastructure.persistence.orm.models import (
        FreelancerKnowledge as ORMKnowledge,
    )

    random.seed(a=None, version=2)
    freelancer = Freelancer.objects.get(email=email)
    skillsOption = [
        "Naming",
        "Diseño de logo",
        "Diseño de identidad visual y brandbook",
        "Diseño de tarjetas de presentación",
        "Estudio y conceptualización de marca",
        "Estrategia de Marca",
        "Diseño en 3D",
        "Modelado en 3D",
        "Renderizado en 3D",
        "Animación en 3D",
        "Fotografía y recorridos 3D",
        "Arquitectura comercial",
        "Showrooms",
        "Doblaje español-inglés",
        "Doblaje inglés-español",
        "Efectos de sonido",
        "Producción de audiolibros",
        "Experiencias publicitarias en Realidad Aumentada",
        "Experiencias publicitarias en Realidad Virtual",
        "Videojuegos publicitarios web 2D",
        "Videojuegos publicitarios para activaciones",
        "Videojuegos publicitarios 3D",
        "Artículos y publicaciones de blog",
        "Escritura del curriculum vitae",
        "Corrección de textos y edición",
        "Descripciones de productos",
        "Contenido de sitio web",
        "Escritura de guiones",
        "Escritura de artículos",
        "Escritura creativa",
    ]
    numberKnowledges = random.randint(2, 20)
    for _ in range(numberKnowledges):
        nameSkill = random.choice(skillsOption)
        ORMKnowledge.objects.create(
            freelancer=freelancer, name=nameSkill, value=random.randint(1, 4)
        )
        skillsOption.remove(nameSkill)


def fewSkills():
    n1 = _createGroup("Creatividad y diseño", None)
    n22 = _createGroup("Logo e identidad", n1)
    _createChildren(
        n22,
        [
            "Naming",
            "Diseño de logo",
            "Diseño de identidad visual y brandbook",
            "Diseño de tarjetas de presentación",
            "Estudio y conceptualización de marca",
            "Estrategia de Marca",
        ],
    )
    n22 = _createGroup("3D", n1)
    _createChildren(
        n22,
        [
            "Diseño en 3D",
            "Modelado en 3D",
            "Renderizado en 3D",
            "Animación en 3D",
            "Fotografía y recorridos 3D",
            "Arquitectura comercial",
            "Showrooms",
        ],
    )
    n22 = _createGroup("Audio", n1)
    _createChildren(
        n22,
        [
            "Doblaje español-inglés",
            "Doblaje inglés-español",
            "Efectos de sonido",
            "Producción de audiolibros",
        ],
    )
    n22 = _createGroup("Videojuegos y Realidad aumentada y virtual", n1)
    _createChildren(
        n22,
        [
            "Experiencias publicitarias en Realidad Aumentada",
            "Experiencias publicitarias en Realidad Virtual",
            "Videojuegos publicitarios web 2D",
            "Videojuegos publicitarios para activaciones",
            "Videojuegos publicitarios 3D",
        ],
    )

    n1 = _createGroup("Redacción", None)
    _createChildren(
        n1,
        [
            "Artículos y publicaciones de blog",
            "Escritura del curriculum vitae",
            "Corrección de textos y edición",
            "Descripciones de productos",
            "Contenido de sitio web",
            "Escritura de guiones",
            "Escritura de artículos",
            "Escritura creativa",
        ],
    )


# TODO: end TODO


def _createGroup(skill: str, parent):
    id = FreelancerSkill.objects.create(name=skill)
    if parent:
        parent.children.add(id)
    return id


def _createSkill(skill: str, parent):
    id = FreelancerSkill.objects.create(name=skill)
    parent.children.add(id)


def _createChildren(parent, children: List[str]):
    for child in children:
        _createSkill(child, parent)


def allSkills():
    n1 = _createGroup("Creatividad y diseño", None)
    n22 = _createGroup("Logo e identidad", n1)
    _createChildren(
        n22,
        [
            "Naming",
            "Diseño de logo",
            "Diseño de identidad visual y brandbook",
            "Diseño de tarjetas de presentación",
            "Estudio y conceptualización de marca",
            "Estrategia de Marca",
        ],
    )
    n22 = _createGroup("Arte e ilustración", n1)
    _createChildren(
        n22,
        [
            "Ilustración corporativa",
            "Ilustración para libros",
            "Storyboards",
            "Caricaturas",
            "Infografías",
            "Graffitis",
            "Diseño de personajes",
        ],
    )
    n22 = _createGroup("Dirección creativa", n1)
    _createChildren(
        n22,
        [
            "Auditoría Digital",
            "Dirección creativa para campañas 360",
            "Dirección creativa de eventos",
            "Dirección creativa audiovisual",
            "Dirección creativa musical",
        ],
    )
    n22 = _createGroup("Diseño gráfico corporativo", n1)
    _createChildren(
        n22,
        [
            "Diseño de empaques - Packaging",
            "Diseño de etiquetas",
            "Diseño editorial",
            "Diseño de presentaciones",
            "Diseño de menú (restaurants)",
        ],
    )
    n22 = _createGroup("Diseño publicitario", n1)
    _createChildren(
        n22,
        [
            "Diseño de merchandising",
            "Diseño de brochures",
            "Diseño de flyers informativos",
            "Diseño de Banners",
            "Diseño de catálogos",
            "Diseño y edición de imágenes",
            "Diseño para social media",
        ],
    )
    n22 = _createGroup("Fotografía", n1)
    _createChildren(
        n22,
        [
            "Fotografía para redes sociales",
            "Fotografía de productos",
            "Fotografía de prendas y zapatería",
            "Fotografía de modelos",
            "Fotografía gastronómica",
            "Fotografía de bebés",
            "Retratos familiares",
            "Fotografía de matrimonios",
            "Fotografía de eventos",
            "Fotografía corporativa",
            "Fotografías 360º",
            "Fotografía industrial",
            "Fotografía publicitaria",
            "Retoque de fotografía digital",
        ],
    )
    n22 = _createGroup("Video", n1)
    _createChildren(
        n22,
        [
            "Videos corporativos para empresas",
            "Producción y post-producción de videos",
            "Servicio de grabación de video 360º",
            "Videos publicitarios",
            "Videos animados",
            "Elaboración de tutoriales",
            "Cortometrajes",
            "Producción de audio",
            "Edición de vídeo",
            "Grabación de video",
            "Dirección de vídeo",
        ],
    )
    n22 = _createGroup("3D", n1)
    _createChildren(
        n22,
        [
            "Diseño en 3D",
            "Modelado en 3D",
            "Renderizado en 3D",
            "Animación en 3D",
            "Fotografía y recorridos 3D",
            "Arquitectura comercial",
            "Showrooms",
        ],
    )
    n22 = _createGroup("Audio", n1)
    _createChildren(
        n22,
        [
            "Doblaje español-inglés",
            "Doblaje inglés-español",
            "Voz en off",
            "Voz para publicidad",
            "Songwriting",
            "Composición musical",
            "Producción musical",
            "DJ",
            "Vocalista",
            "Creación de jingles publicitario",
            "Creación de intros musicales",
            "Elaboración de podcasts",
            "Efectos de sonido",
            "Producción de audiolibros",
        ],
    )
    n22 = _createGroup("Videojuegos y Realidad aumentada y virtual", n1)
    _createChildren(
        n22,
        [
            "Experiencias publicitarias en Realidad Aumentada",
            "Experiencias publicitarias en Realidad Virtual",
            "Videojuegos publicitarios web 2D",
            "Videojuegos publicitarios para activaciones",
            "Videojuegos publicitarios 3D",
        ],
    )

    n1 = _createGroup("Redacción", None)
    _createChildren(
        n1,
        [
            "Artículos y publicaciones de blog",
            "Escritura del curriculum vitae",
            "Corrección de textos y edición",
            "Escritura técnica",
            "Cartas de presentación",
            "Perfiles de LinkedIn",
            "UX Writing",
            "Copywriting",
            "Ghostwriting",
            "Investigación y resúmenes",
            "Descripciones de productos",
            "Contenido de sitio web",
            "Escritura de guiones",
            "Redacción de discursos",
            "Redacción de podcasts",
            "Creación de diálogos",
            "Corrección de estilo",
            "Escritura de artículos",
            "Escritura creativa",
        ],
    )

    n1 = _createGroup("Traducción", None)
    _createChildren(
        n1,
        [
            "Traducción inglés-español",
            "Traducción español-inglés",
            "Traducción español-quechua",
        ],
    )

    n1 = _createGroup("Marketing Digital", None)
    n22 = _createGroup("Consultoría", n1)
    _createChildren(
        n22,
        [
            "Estrategia de marca",
            "Estrategia de engagement",
            "Diseño de planes de acción en redes",
            "Manejo de crisis reputacional",
            "Estrategia de inbound Marketing",
            "Estrategia see think do care",
            "Estrategia AIDA",
            "Estrategia de contenidos",
            "Consultoría SEO",
            "Auditoría SEO",
        ],
    )
    n22 = _createGroup("Generación de Tráfico", n1)
    _createChildren(
        n22,
        [
            "Generación de contenido",
            "Redacción de artículos SEO",
            "Producción de contenido audiovisual",
            "E-mailing",
            "Email Remarketing",
            "Retargeting a website",
            "Retargeting a productos visitados e-commerce",
            "Activaciones digitales",
            "Facebook Ads",
            "Google Ads",
            "Linkedin Ads",
            "Tinder Ads",
            "TikTok Ads",
            "Twitch Ads",
            "Youtube Ads",
            "Publicidad programática",
        ],
    )
    n22 = _createGroup("Medición y optimización", n1)
    _createChildren(
        n22,
        [
            "Media Tracking",
            "A/B Testing",
            "ROI",
            "Facebook insight",
            "Google Analytics",
            "Google Data Studio",
            "Hootsuite",
            "RD  Station",
            "Hubspot",
        ],
    )
    n22 = _createGroup("Posicionamiento SEO", n1)
    _createChildren(
        n22,
        [
            "SEO Técnico, etiquetas, sitemaps, robots.txt",
            "Index optimization",
            "SEO Local",
            "SEO Ecommerce",
            "SEO para Startups",
            "SEO Internacional ",
            "SEO para marca personal",
        ],
    )
    n22 = _createGroup("Social Media", n1)
    _createChildren(n22, ["Community Management", "Social listening avanzado"])
    _createChildren(
        n1, ["Growth Hacking", "Chatbots", "PR y Marketing de influencers"]
    )

    n1 = _createGroup("Diseño de experiencia digital", None)
    n22 = _createGroup("Consultoría", n1)
    _createChildren(
        n22,
        [
            "Estrategia de producto",
            "Estrategia de adopción de usuarios",
            "Estrategia de contenido",
            "Entrenamiento de personal",
        ],
    )
    n22 = _createGroup("Levantamiento de procesos", n1)
    _createChildren(n22, ["Modelado de procesos", "Optimización de procesos"])
    n22 = _createGroup("Diseño de servicio y producto", n1)
    _createChildren(
        n22,
        [
            "Lean StartUp",
            "Investigación estadística",
            "Investigación de escritorio",
            "Investigación netnográfica",
            "Identificación de insights",
            "Definición de problema(s)",
            "Elaboración de árbol de problemas",
            "Elaboración de Benchmark",
            "Construcción de Buyer Persona",
            "Construcción de Customer Journey Maps",
            "Elaboración de Service Blueprint",
            "Ideación y diseño de experiencia TOBE",
            "Validación de ideas con usuarios",
            "Realización de Focus Groups",
            "Generación de modelos de negocio",
            "Sprint Design",
            "Agile Inception DECK",
            "Diseño de métricas e indicadores",
            "Método HEART",
        ],
    )
    n22 = _createGroup("Implementación UX", n1)
    _createChildren(
        n22,
        [
            "Diseño y prototipado UX de aplicaciones móviles",
            "Diseño y prototipado UX de aplicaciones web",
            "Diseño y prototipado UX de websites corporativos",
            "Diseño y prototipado UX de e-commerce",
            "Pruebas de usabilidad con usuarios",
            "Testing A/B",
            "Auditoría UX",
        ],
    )
    n22 = _createGroup("Diseño de interfaces", n1)
    _createChildren(
        n22,
        [
            "Diseño UI de landing pages",
            "Diseño UI de aplicaciones móviles",
            "Diseño UI de aplicaciones web",
            "Diseño UI de websites corporativos",
            "Diseño UI de ecommerce",
            "Elaboración de guía de estilos digital",
            "Creación de íconos",
            "Elaboración de tutoriales",
            "Elaboración de documentos funcionales",
            "Elaboración de product backlog",
        ],
    )

    n1 = _createGroup("Desarrollo web", None)
    n22 = _createGroup("Websites Corporativos CMS", n1)
    _createChildren(
        n22, ["Wordpress", "Drupal", "Joomla", "Acquia", "Magnolia"]
    )
    n22 = _createGroup("LMS - Learning Management System", n1)
    _createChildren(
        n22,
        [
            "Moodle",
            "Blackboard",
            "Chamilo",
            "Docebo",
            "Mindflash",
            "Plugins de Wordpress",
            "Open edX ",
            "Canvas",
            "Talent LMS",
        ],
    )
    n22 = _createGroup("CRM", n1)
    _createChildren(
        n22,
        [
            "Salesforce",
            "Hubspot",
            "Britix24",
            "Odoo CRM",
            "Sugar CRM",
            "Suite CRM",
            "Vtiger CRM",
            "Dolibarr",
        ],
    )
    n22 = _createGroup("Intranets y sistemas colaborativos", n1)
    n333 = _createGroup("Sharepoint", n22)
    _createChildren(
        n333,
        [
            "SharePoint 2010",
            "SharePoint 2013",
            "SharePoint 2016",
            "SharePoint 2019",
            "SharePoint Online",
        ],
    )
    _createChildren(
        n22,
        [
            "Bitrix24 ",
            "dotCMS",
            "TWiki ",
            "Liferay ",
            "EXO",
            "Precurio ",
            "Quintagroup",
            "Engynn",
            "Intranet basada en Drupal",
            "Intranet basada en Wordpress",
        ],
    )
    n22 = _createGroup("Website Builders", n1)
    _createChildren(
        n22,
        [
            "Wix",
            "Godaddy website builder",
            "Wordpress website builder",
            "Squarespace",
            "Blogger",
        ],
    )
    n22 = _createGroup("Ecommerce CMS", n1)
    _createChildren(
        n22,
        [
            "Woocommerce",
            "Prestashop",
            "Magento",
            "Shopify",
            "IBM WebSphere Commerce",
            "Oracle ATG",
            "SAP Hybris",
            "VTEX",
            "Análisis de performance y seguridad",
        ],
    )

    n1 = _createGroup("Desarrollo de sistemas a medida", None)
    n22 = _createGroup("Aplicativos Móviles", n1)
    n333 = _createGroup("Desarrollo Nativo en Android", n22)
    _createChildren(n333, ["Java", "Kotlin"])
    n333 = _createGroup("Desarrollo Nativo en iOS", n22)
    _createChildren(n333, ["Objective-C", "Swift"])
    _createChildren(n22, ["Phonegap", "Xamarin", "React Native", "Flutter"])
    n22 = _createGroup("Frontend web", n1)
    _createChildren(
        n22,
        [
            "Angular JS",
            "Angular CLI",
            "Knockout",
            "ReactJS",
            "Vue JS",
            "Vue CLI",
        ],
    )
    n22 = _createGroup("Backend y fullstack", n1)
    n333 = _createGroup(".NET", n22)
    _createSkill("Consultoría en arquitectura de aplicaciones en .NET", n333)
    n4444 = _createGroup("Lenguaje de programación", n333)
    _createChildren(n4444, ["C#", "C++", "Visual Basic"])
    n4444 = _createGroup("Versión del Framework", n333)
    _createChildren(
        n4444,
        [
            ".NET 2.0",
            ".NET 3",
            ".NET 4",
            ".NET 4.5 ",
            ".NET 4.6",
            ".NET 4.7",
            ".NET 4.8",
            ".NET Core",
        ],
    )
    n333 = _createGroup("Java", n22)
    _createChildren(
        n333,
        [
            "Consultoría en arquitectura de aplicaciones en JAVA",
            "Java Spring Web",
            "Java Spring Boot",
            "Java JPA",
            "Java JDO",
            "Java JUnit",
        ],
    )
    n333 = _createGroup("PHP", n22)
    _createChildren(
        n333,
        [
            "Consultoría en arquitectura de aplicaciones en PHP",
            "Laravel",
            "Symfony",
            "CodeIgniter",
            "Zend Framewor",
            "Yii (Framework)",
            "CakePHP",
            "Slim",
            "Phalcon",
            "FuelPHP",
            "Fat-Free Framework",
        ],
    )
    n333 = _createGroup("Python", n22)
    _createChildren(
        n333,
        [
            "Python Django",
            "Python CherryPy",
            "Python Tornado",
            "Python SqlAlchemy",
            "Python Jinja2",
        ],
    )

    _createSkill("Ruby on rails", n22)
    n333 = _createGroup("NodeJS", n22)
    _createChildren(
        n333, ["NodeJS Express", "NodeJS Mongoose", "NodeJS Vanilla"]
    )

    n22 = _createGroup("Gestor de bases de datos SQL", n1)
    _createChildren(n22, ["MySQL", "Maria DB"])
    n333 = _createGroup("PostgreSQL", n22)
    _createChildren(
        n333,
        [
            "PostgreSQL Versión 9",
            "PostgreSQL Versión 10",
            "PostgreSQL Versión 11",
        ],
    )
    n333 = _createGroup("MSSQL Server", n22)
    _createChildren(
        n333,
        [
            "SQL Server 2008",
            "SQL Server 2008 R2",
            "SQL Server 2012",
            "SQL Server 2014",
            "SQL Server 2016",
            "SQL Server 2017",
            "SQL Server 2019",
        ],
    )
    n333 = _createGroup("Oracle", n22)
    _createChildren(
        n333,
        [
            "Oracle Database 11g",
            "Oracle Database 12c",
            "Oracle Database 18c",
            "Oracle Database 19c",
            "Oracle Database 21c",
        ],
    )
    n22 = _createGroup("Gestor de bases de datos NoSQL", n1)
    _createChildren(
        n22, ["MongoDB", "Cassandra", "Redis", "CouchDB", "Node4J", "Hazelcast"]
    )
    n22 = _createGroup("Gestor de despliegues", n1)
    _createChildren(n22, ["Kubernetes", "Docker", "Jenkins"])

    n1 = _createGroup("Programación avanzada", None)
    _createChildren(
        n1,
        [
            "Linux developmentAssembler development",
            "Algoritmia avanzada para soluciones industriales",
            "Algoritmia avanzada para soluciones comerciales",
            "Matemáticas aplicada a la industria",
            "Inteligencia artificial",
            "Machine learning",
            "Deep learning",
        ],
    )

    n1 = _createGroup("Integraciones con ERP", None)
    # _createSkill('Integración con Microsoft Dynamics', n1)
    n22 = _createGroup("Integración con Oracle", n1)
    _createChildren(
        n22,
        [
            "JD Edwards Enterprise One",
            "Oracle People Soft",
            "Oracle E-Business One",
        ],
    )
    # _createSkill('Integración con Infor', n1)
    n22 = _createGroup("Integración con SAP", n1)
    _createChildren(n22, ["SAP ABAP", "SAP Fiori", "SAPUI5"])
    n333 = _createGroup("Módulos de SAP R3", n22)
    _createChildren(
        n333,
        [
            "FI: (Finanzas) Contabilidad Financiera",
            "CO: (Controlling) Control y Costos",
            "LO: (Logistics) Logística general",
            "SD: (Sales and Distribution) Ventas y Distribución",
            "MM: (Materials Management) Gestión de Materiales",
            "LE: (Logistics Execution) Ejecución de logística",
            "PP: (Production Planning) Planificación de la producción",
            "PS: (Project system) Sistema de Proyectos",
            "QM (Quality Management) Gestión de calidad",
            "HR (Human Resources) Recursos Humanos",
            "BC Basis Components",
        ],
    )
    n333 = _createGroup("Módulos de SAP S/4 HANA Enterprise Management", n22)
    _createChildren(
        n333,
        [
            "Asset Management (Gestión de activos)",
            "Finance (Finanzas)",
            "Human Resources (Recursos humanos)",
            "Manufacturing (Fabricación)",
            "Maintenance, Repair, and Overhaul"
            " (Mantenimiento, reparación y revisión)",
            "R&D / Engineering (I+D / Ingeniería)",
            "Sales (Ventas)",
            "Service (Servicios)",
            "Supply Chain (Cadena de suministro)",
            "Analytics Technology (Tecnología analítica)",
            "Enterprise Technology (Tecnología empresarial)",
            "Projects (Proyectos)",
        ],
    )
    n333 = _createGroup("Módulos de SAP S/4 HANA LoB Products", n22)
    _createChildren(
        n333,
        [
            "Asset Management (Gestión de activos)",
            "Database and Data Management (Base de datos y gestión de datos)",
            "Finance (Finanzas)",
            "Manufacturing (Fabricación)",
            "R&D / Engineering (I+D / Ingeniería)",
            "Sales (Ventas)",
            "Supply Chain (Cadena de suministro)",
            "Enterprise Technology (Tecnología empresarial)",
        ],
    )
    n333 = _createGroup(
        "SAP S/4 HANA LoB Products para industrias específicas", n22
    )
    _createChildren(
        n333,
        [
            "Agriculture (Agricultura)",
            "Banking (La banca)",
            "Insurance (Aseguradoras)",
            "Oil & Gas (Petróleso y gas natural)",
            "Professional Services (Servicios profesionales)",
            "Public Sector (Sector público)",
            "Retail and Fashion (Retail y moda)",
            "Utilities (Servicios)",
            "SAP Waste & Recycling (Desperdicio y reciclaje)",
        ],
    )
    n333 = _createGroup("SAP Business One", n22)
    n4444 = _createGroup("Módulos", n333)
    _createChildren(
        n4444,
        [
            "Finanzas",
            "Oportunidades",
            "Ventas",
            "Interlocutores comerciales",
            "Gestión de bancos",
            "Inventario",
            "Recursos",
            "Producción",
            "Compras",
            "Planificación de necesidades",
            "Servicio",
            "Recursos humanos",
            "Informes",
            "Gestión",
        ],
    )
    n4444 = _createGroup("Versiones", n333)
    _createChildren(
        n4444,
        [
            "SAP Business One 7",
            "SAP Business One 8",
            "SAP Business One 9",
            "SAP Business One 10",
        ],
    )

    n1 = _createGroup("Quality Assurance & Testing especializado", None)
    _createChildren(
        n1,
        [
            "Agile testing comprobado",
            "Pruebas funcionales",
            "Pruebas de rendimiento",
            "Pruebas de estrés",
            "Pruebas de accesibilidad",
            "Pruebas de usabilidad",
            "Pruebas de seguridad",
            "Accounting and Financial Testing",
            "Ubertesting",
        ],
    )
    n22 = _createGroup("Automatización de pruebas", n1)
    _createChildren(n22, ["UiPath", "Selenium", "Appium", "Protractor"])

    n1 = _createGroup("Data & Analytics", None)
    n22 = _createGroup("Estadística, minería y ciencia de datos", n1)
    _createChildren(
        n22,
        [
            "SPSS",
            "Stata",
            "Lenguaje R",
            "Programación Python",
            "Programación Java",
            "Programación SQL",
            "Matlab",
            "SAS",
            "RapidMinder",
            "BigML",
            "SAS",
            "TIBCO",
            "Alteryx",
            "Knime",
            "Mathworks",
            "Hadoop",
            "Spark",
            "Hive",
            "HBase",
        ],
    )
    n22 = _createGroup("ETL", n1)
    _createChildren(
        n22,
        [
            "IBM Websphere DataStage",
            "Microsoft Integration Services",
            "SAP Data Integrator",
            "Cognos Decisionstream",
            "Sunopsis",
            "Apache NiFi",
            "Streamsets",
            "Apache Airflow",
            "AWS Data Pipeline",
            "AWS Glue",
            "Talend",
            "Informatica Power Center",
            "AB Initio",
            "Pentaho",
            "Azure Data Factory",
            "SAS Dataflux",
        ],
    )
    n22 = _createGroup("Análisis y visualización de Datos", n1)
    _createChildren(
        n22,
        [
            "SAP Business Objects",
            "Microsoft Reporting Services",
            "Microsoft Analysis Services",
            "Power BI",
            "Tableau",
            "Qlik",
            "Microstrategy",
            "Thoughtspot",
        ],
    )

    n1 = _createGroup("Cloud", None)
    _createChildren(
        n1, ["Google Cloud", "AWS", "Microsoft Azure", "Huawei Cloud"]
    )
