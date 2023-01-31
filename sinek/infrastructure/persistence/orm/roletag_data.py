AREA_ROLE_MAP = {
    "Software Development": [
        "Frontend",
        "Backend",
        "Full Stack",
        "Mobile",
        "QA Testing",
        "Software Architect",
        "Enterprise Solution Developer",
        "Business Analyst",
        "QA Security",
    ],
    "Operation Management": [
        "Solution Architect",
        "Arquitecto Cloud",
        "Devops",
    ],
    "Data Management & Exploitation": [
        "Data Engineer",
        "Data Modeler",
        "Data Science",
        "Machine Learning",
    ],
    "Product & Service Design": [
        "Design Research",
        "UX/UI Designers",
        "Service Designer",
    ],
    "Product Management & Business Agility": [
        "Product Manager",
        "Product Owner",
        "Scrum Master",
    ],
    "Marketing": [
        "Diseñador gráfico",
        "Campaign Manager",
        "Redactor creativo",
        "Ejecutivo de cuentas",
    ],
}

ROLE_ROOTSKILL_MAP = {
    "Marketing": "Marketing y publicidad",
    "Product & Service Design": "Diseño de experiencia",
    "Product Management & Business Agility": "Diseño de experiencia",
    "Software Development": "Desarrollo de software",
    "Operation Management": "Desarrollo de software",
    "Data Management & Exploitation": "Business Intelligence",
}

ROLE_AREA_MAP = { v: k for k in AREA_ROLE_MAP for v in AREA_ROLE_MAP[k] }

class RootSkillDict:
    role_area = ROLE_AREA_MAP
    area_skill = ROLE_ROOTSKILL_MAP
 
    def __class_getitem__(self, role):
        try:
            return self.area_skill[self.role_area[role]]
        except Exception:
            raise RuntimeError('Inconsistent information in roletag_data file.')
