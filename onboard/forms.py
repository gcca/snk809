# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django import forms
from django.forms import MultipleChoiceField
from django.utils.translation import gettext as _

from . import fields, models, widgets

OnboardResumeForm = forms.modelform_factory(
    models.Onboard,
    fields=("resume",),
    # Translators: Este texto aparecen en el board del candidato
    labels={"resume": _("Applicant resume")},
    widgets={"resume": widgets.ResumeFileInput},
)


TmmsForm = forms.modelform_factory(
    models.TmmsInput,
    exclude=("onboard",),
    labels={
        "q1": "Presto mucha atención a los sentimientos",
        "q2": "Normalmente me preocupo por lo que siento",
        "q3": "Normalmente dedico tiempo a pensar en mis emociones",
        "q4": (
            "Pienso que merece la pena prestar atención a mis emociones y"
            " estado de ánimo"
        ),
        "q5": "Dejo que mis sentimientos afecten mis pensamientos",
        "q6": "Pienso en mi estado de ánimo constantemente",
        "q7": "A menudo pienso en mis sentimientos",
        "q8": "Presto mucha atención a cómo me siento",
        "q9": "Tengo claro mis sentimientos",
        "q10": "Frecuentemente puedo definir mis sentimientos",
        "q11": "Casi siempre sé cómo me siento",
        "q12": "Normalmente conozco mis sentimientos sobre las personas",
        "q13": (
            "A menudo me doy cuenta de mis sentimientos en diferentes"
            " situaciones"
        ),
        "q14": "Siempre puedo decir cómo me siento",
        "q15": "A veces puedo decir cuáles son mis emociones",
        "q16": "Puedo llegar a comunicar mis sentimientos",
        "q17": (
            "Aunque a veces me siento triste, suelo tener una visión optimista"
        ),
        "q18": (
            "Aunque a veces me sienta mal, procuro pensar en cosas agradables"
        ),
        "q19": "Cuando estoy triste, pienso en todos los placeres de la vida.",
        "q20": "Intento tener pensamientos positivos aunque me sienta mal",
        "q21": (
            "Si doy demasiadas vueltas a las cosas, complicándolas, trato de"
            " calmarme"
        ),
        "q22": "Me preocupo por tener un buen estado de ánimo",
        "q23": "Tengo mucha energía cuando me siento feliz",
        "q24": "Cuando estoy enfadado intento cambiar mi estado de ánimo",
    },
    formfield_callback=lambda _, **kwargs: forms.ChoiceField(
        choices=models.TmmsInput.CHOICES, widget=forms.RadioSelect, **kwargs
    ),
)


class BaseNoEquivalentModelForm(forms.Form):
    # TODO integrate to ModelForm

    model = None

    def __init__(self, *args, instance=None, initial=None, **kwargs):
        if instance is None:
            self.instance = self.model()
            # TODO if initial populate self.instance
        else:
            self.instance = instance
            if not initial:
                initial = self._GetInitial(instance)

        super().__init__(*args, initial=initial, **kwargs)

    def _post_clean(self):
        super()._post_clean()
        if not self.errors:
            self._UpdateInstance(self.cleaned_data)

    def save(self):
        """To keep ModelForm compatibility."""
        self.instance.save()
        return self.instance


class ComplexInstructionsForm(BaseNoEquivalentModelForm):
    model = models.ComplexInstructionsInput

    class Field(MultipleChoiceField):
        CHOICES = [("a", ""), ("b", ""), ("c", "")]

        def __init__(self, amount: int, kind: str, date: str):
            super().__init__(
                choices=self.CHOICES,
                required=False,
                widget=forms.CheckboxSelectMultiple,
            )
            self.amount = amount
            self.kind = kind
            self.day, self.month, self.year = date.split(" ")

    q1 = Field(
        amount=3000,
        kind="Incendios",
        date="2 enero 1976",
    )
    q2 = Field(
        amount=1000,
        kind="Vida",
        date="22 octubre 1975",
    )
    q3 = Field(
        amount=4000,
        kind="Accidentes",
        date="14 setiembre 1975",
    )
    q4 = Field(
        amount=2000,
        kind="Vida",
        date="13 noviembre 1976",
    )
    q5 = Field(
        amount=4000,
        kind="Incendios",
        date="17 mayo 1976",
    )
    q6 = Field(
        amount=3000,
        kind="Accidentes",
        date="12 octubre 1975",
    )
    q7 = Field(
        amount=5000,
        kind="Vida",
        date="16 febrero 1976",
    )
    q8 = Field(
        amount=1000,
        kind="Incendios",
        date="3 agosto 1976",
    )
    q9 = Field(
        amount=4000,
        kind="Incendios",
        date="11 agosto 1976",
    )
    q10 = Field(
        amount=2000,
        kind="Accidentes",
        date="21 mayo 1975",
    )
    q11 = Field(
        amount=5000,
        kind="Vida",
        date="9 marzo 1975",
    )
    q12 = Field(
        amount=3000,
        kind="Incendios",
        date="17 julio 1976",
    )
    q13 = Field(
        amount=1000,
        kind="Accidentes",
        date="4 junio 1976",
    )
    q14 = Field(
        amount=1000,
        kind="Vida",
        date="23 noviembre 1976",
    )
    q15 = Field(
        amount=5000,
        kind="Vida",
        date="18 abril 1975",
    )
    q16 = Field(
        amount=2000,
        kind="Accidentes",
        date="24 diciembre 1976",
    )
    q17 = Field(
        amount=5000,
        kind="Accidentes",
        date="19 abril 1975",
    )
    q18 = Field(
        amount=2000,
        kind="Vida",
        date="7 diciembre 1976",
    )
    q19 = Field(
        amount=4000,
        kind="Incendios",
        date="26 mayo 1975",
    )
    q20 = Field(
        amount=3000,
        kind="Accidentes",
        date="6 enero 1976",
    )
    q21 = Field(
        amount=5000,
        kind="Vida",
        date="29 marzo 1975",
    )
    q22 = Field(
        amount=3000,
        kind="Vida",
        date="28 junio 1975",
    )
    q23 = Field(
        amount=4000,
        kind="Accidentes",
        date="8 febrero 1976",
    )
    q24 = Field(
        amount=1000,
        kind="Incendios",
        date="27 julio 1975",
    )
    q25 = Field(
        amount=2000,
        kind="Accidentes",
        date="21 enero 1976",
    )

    def _GetInitial(self, instance):
        return {
            "q1": self.__ModelToChoices(instance.q1),
            "q2": self.__ModelToChoices(instance.q2),
            "q3": self.__ModelToChoices(instance.q3),
            "q4": self.__ModelToChoices(instance.q4),
            "q5": self.__ModelToChoices(instance.q5),
            "q6": self.__ModelToChoices(instance.q6),
            "q7": self.__ModelToChoices(instance.q7),
            "q8": self.__ModelToChoices(instance.q8),
            "q9": self.__ModelToChoices(instance.q9),
            "q10": self.__ModelToChoices(instance.q10),
            "q11": self.__ModelToChoices(instance.q11),
            "q12": self.__ModelToChoices(instance.q12),
            "q13": self.__ModelToChoices(instance.q13),
            "q14": self.__ModelToChoices(instance.q14),
            "q15": self.__ModelToChoices(instance.q15),
            "q16": self.__ModelToChoices(instance.q16),
            "q17": self.__ModelToChoices(instance.q17),
            "q18": self.__ModelToChoices(instance.q18),
            "q19": self.__ModelToChoices(instance.q19),
            "q20": self.__ModelToChoices(instance.q20),
            "q21": self.__ModelToChoices(instance.q21),
            "q22": self.__ModelToChoices(instance.q22),
            "q23": self.__ModelToChoices(instance.q23),
            "q24": self.__ModelToChoices(instance.q24),
            "q25": self.__ModelToChoices(instance.q25),
        }

    def __ModelToChoices(self, value):
        return tuple(
            choice for choice, valid in zip(("a", "b", "c"), value) if valid
        )

    def _UpdateInstance(self, cleaned_data):
        self.instance.q1 = cleaned_data["q1"]
        self.instance.q2 = cleaned_data["q2"]
        self.instance.q3 = cleaned_data["q3"]
        self.instance.q4 = cleaned_data["q4"]
        self.instance.q5 = cleaned_data["q5"]
        self.instance.q6 = cleaned_data["q6"]
        self.instance.q7 = cleaned_data["q7"]
        self.instance.q8 = cleaned_data["q8"]
        self.instance.q9 = cleaned_data["q9"]
        self.instance.q10 = cleaned_data["q10"]
        self.instance.q11 = cleaned_data["q11"]
        self.instance.q12 = cleaned_data["q12"]
        self.instance.q13 = cleaned_data["q13"]
        self.instance.q14 = cleaned_data["q14"]
        self.instance.q15 = cleaned_data["q15"]
        self.instance.q16 = cleaned_data["q16"]
        self.instance.q17 = cleaned_data["q17"]
        self.instance.q18 = cleaned_data["q18"]
        self.instance.q19 = cleaned_data["q19"]
        self.instance.q20 = cleaned_data["q20"]
        self.instance.q21 = cleaned_data["q21"]
        self.instance.q22 = cleaned_data["q22"]
        self.instance.q23 = cleaned_data["q23"]
        self.instance.q24 = cleaned_data["q24"]
        self.instance.q25 = cleaned_data["q25"]


class DiscForm(BaseNoEquivalentModelForm):

    model = models.DiscInput

    q1 = fields.DiscField(("Expresivo", "Sumiso", "Enérgico", "Controlado"))
    q2 = fields.DiscField(
        ("Fuerte de carácter", "Cuidadoso", "Emocional", "Satisfecho")
    )
    q3 = fields.DiscField(("Correcto", "Tranquilo", "Pionero", "Influyente"))
    q4 = fields.DiscField(("Preciso", "Dominante", "Dispuesto", "Atractivo"))
    q5 = fields.DiscField(("Ecuánime", "Estimulante", "Meticuloso", "Decidido"))
    q6 = fields.DiscField(("Tímido", "Exigente", "Paciente", "Cautivador"))
    q7 = fields.DiscField(
        ("Concienzudo", "Buena compañia", "Bondadoso", "Depende de si")
    )
    q8 = fields.DiscField(
        ("Agradable", "Con dominio propio", "Juguetón", "Persistente")
    )
    q9 = fields.DiscField(("Animoso", "Conversador", "Bonachon", "Conservador"))
    q10 = fields.DiscField(
        ("Contento", "Impaciente", "Convicente", "Resignado")
    )
    q11 = fields.DiscField(
        ("Respetuoso", "Socialmente desenvuelto", "Agresivo", "Apacible")
    )
    q12 = fields.DiscField(
        ("Aplomo", "Convencional", "Toma riesgos", "Servicial")
    )
    q13 = fields.DiscField(
        (
            "Seguro de sí mismo",
            "Cooperativo",
            "Disputador",
            "Relajado, sin tensiones",
        )
    )
    q14 = fields.DiscField(
        ("Inquieto", "Disciplinado", "Inspirador", "Considerado")
    )
    q15 = fields.DiscField(
        ("Diplomático", "Valiente", "Compasivo", "Optimista")
    )
    q16 = fields.DiscField(("Encantador", "Positivo", "Indulgente", "Riguroso"))
    q17 = fields.DiscField(
        ("Aventurero", "Entusiasta", "Sigue las reglas", "Leal")
    )
    q18 = fields.DiscField(
        ("Humilde", "Oyente atento", "Entretenido", "Con fuerza de voluntad")
    )
    q19 = fields.DiscField(
        ("Divertido", "Obediente", "Discreto", "Competitivo")
    )
    q20 = fields.DiscField(("Cauteloso", "Amistoso", "Vigoroso", "Persuasivo"))
    q21 = fields.DiscField(("Reservado", "Franco", "Estricto", "Elocuente"))
    q22 = fields.DiscField(("Cortés", "Animado", "Decisivo", "Preciso"))
    q23 = fields.DiscField(("Asertivo", "Sociable", "Estable", "Metódico"))
    q24 = fields.DiscField(
        ("Extrovertido", "Intrepido", "Moderado", "Perfeccionista")
    )

    def _GetInitial(self, instance):
        ValueTuple = widgets.DiscInput.ValueTuple
        return {
            "q1": ValueTuple(instance.q1_minus, instance.q1_plus),
            "q2": ValueTuple(instance.q2_minus, instance.q2_plus),
            "q3": ValueTuple(instance.q3_minus, instance.q3_plus),
            "q4": ValueTuple(instance.q4_minus, instance.q4_plus),
            "q5": ValueTuple(instance.q5_minus, instance.q5_plus),
            "q6": ValueTuple(instance.q6_minus, instance.q6_plus),
            "q7": ValueTuple(instance.q7_minus, instance.q7_plus),
            "q8": ValueTuple(instance.q8_minus, instance.q8_plus),
            "q9": ValueTuple(instance.q9_minus, instance.q9_plus),
            "q10": ValueTuple(instance.q10_minus, instance.q10_plus),
            "q11": ValueTuple(instance.q11_minus, instance.q11_plus),
            "q12": ValueTuple(instance.q12_minus, instance.q12_plus),
            "q13": ValueTuple(instance.q13_minus, instance.q13_plus),
            "q14": ValueTuple(instance.q14_minus, instance.q14_plus),
            "q15": ValueTuple(instance.q15_minus, instance.q15_plus),
            "q16": ValueTuple(instance.q16_minus, instance.q16_plus),
            "q17": ValueTuple(instance.q17_minus, instance.q17_plus),
            "q18": ValueTuple(instance.q18_minus, instance.q18_plus),
            "q19": ValueTuple(instance.q19_minus, instance.q19_plus),
            "q20": ValueTuple(instance.q20_minus, instance.q20_plus),
            "q21": ValueTuple(instance.q21_minus, instance.q21_plus),
            "q22": ValueTuple(instance.q22_minus, instance.q22_plus),
            "q23": ValueTuple(instance.q23_minus, instance.q23_plus),
            "q24": ValueTuple(instance.q24_minus, instance.q24_plus),
        }

    def _UpdateInstance(self, cleaned_data):
        self.instance.q1_minus = cleaned_data["q1"].minus
        self.instance.q1_plus = cleaned_data["q1"].plus
        self.instance.q2_minus = cleaned_data["q2"].minus
        self.instance.q2_plus = cleaned_data["q2"].plus
        self.instance.q3_minus = cleaned_data["q3"].minus
        self.instance.q3_plus = cleaned_data["q3"].plus
        self.instance.q4_minus = cleaned_data["q4"].minus
        self.instance.q4_plus = cleaned_data["q4"].plus
        self.instance.q5_minus = cleaned_data["q5"].minus
        self.instance.q5_plus = cleaned_data["q5"].plus
        self.instance.q6_minus = cleaned_data["q6"].minus
        self.instance.q6_plus = cleaned_data["q6"].plus
        self.instance.q7_minus = cleaned_data["q7"].minus
        self.instance.q7_plus = cleaned_data["q7"].plus
        self.instance.q8_minus = cleaned_data["q8"].minus
        self.instance.q8_plus = cleaned_data["q8"].plus
        self.instance.q9_minus = cleaned_data["q9"].minus
        self.instance.q9_plus = cleaned_data["q9"].plus
        self.instance.q10_minus = cleaned_data["q10"].minus
        self.instance.q10_plus = cleaned_data["q10"].plus
        self.instance.q11_minus = cleaned_data["q11"].minus
        self.instance.q11_plus = cleaned_data["q11"].plus
        self.instance.q12_minus = cleaned_data["q12"].minus
        self.instance.q12_plus = cleaned_data["q12"].plus
        self.instance.q13_minus = cleaned_data["q13"].minus
        self.instance.q13_plus = cleaned_data["q13"].plus
        self.instance.q14_minus = cleaned_data["q14"].minus
        self.instance.q14_plus = cleaned_data["q14"].plus
        self.instance.q15_minus = cleaned_data["q15"].minus
        self.instance.q15_plus = cleaned_data["q15"].plus
        self.instance.q16_minus = cleaned_data["q16"].minus
        self.instance.q16_plus = cleaned_data["q16"].plus
        self.instance.q17_minus = cleaned_data["q17"].minus
        self.instance.q17_plus = cleaned_data["q17"].plus
        self.instance.q18_minus = cleaned_data["q18"].minus
        self.instance.q18_plus = cleaned_data["q18"].plus
        self.instance.q19_minus = cleaned_data["q19"].minus
        self.instance.q19_plus = cleaned_data["q19"].plus
        self.instance.q20_minus = cleaned_data["q20"].minus
        self.instance.q20_plus = cleaned_data["q20"].plus
        self.instance.q21_minus = cleaned_data["q21"].minus
        self.instance.q21_plus = cleaned_data["q21"].plus
        self.instance.q22_minus = cleaned_data["q22"].minus
        self.instance.q22_plus = cleaned_data["q22"].plus
        self.instance.q23_minus = cleaned_data["q23"].minus
        self.instance.q23_plus = cleaned_data["q23"].plus
        self.instance.q24_minus = cleaned_data["q24"].minus
        self.instance.q24_plus = cleaned_data["q24"].plus


def CareerAnchors_CreateQuestionField(**kwargs):
    return forms.ChoiceField(
        choices=models.CareerAnchorsInput.QUESTION_CHOICES,
        widget=forms.RadioSelect,
        **kwargs
    )


def CareerAnchors_CreateFavoriteField(**kwargs):
    return forms.ChoiceField(
        choices=models.CareerAnchorsInput.FAVORITE_CHOICES,
        widget=forms.Select,
        **kwargs
    )


CAREER_ANCHORS_QUESTION_FIELDS = {
    "q1": CareerAnchors_CreateQuestionField,
    "q2": CareerAnchors_CreateQuestionField,
    "q3": CareerAnchors_CreateQuestionField,
    "q4": CareerAnchors_CreateQuestionField,
    "q5": CareerAnchors_CreateQuestionField,
    "q6": CareerAnchors_CreateQuestionField,
    "q7": CareerAnchors_CreateQuestionField,
    "q8": CareerAnchors_CreateQuestionField,
    "q9": CareerAnchors_CreateQuestionField,
    "q10": CareerAnchors_CreateQuestionField,
    "q11": CareerAnchors_CreateQuestionField,
    "q12": CareerAnchors_CreateQuestionField,
    "q13": CareerAnchors_CreateQuestionField,
    "q14": CareerAnchors_CreateQuestionField,
    "q15": CareerAnchors_CreateQuestionField,
    "q16": CareerAnchors_CreateQuestionField,
    "q17": CareerAnchors_CreateQuestionField,
    "q18": CareerAnchors_CreateQuestionField,
    "q19": CareerAnchors_CreateQuestionField,
    "q20": CareerAnchors_CreateQuestionField,
    "q21": CareerAnchors_CreateQuestionField,
    "q22": CareerAnchors_CreateQuestionField,
    "q23": CareerAnchors_CreateQuestionField,
    "q24": CareerAnchors_CreateQuestionField,
    "q25": CareerAnchors_CreateQuestionField,
    "q26": CareerAnchors_CreateQuestionField,
    "q27": CareerAnchors_CreateQuestionField,
    "q28": CareerAnchors_CreateQuestionField,
    "q29": CareerAnchors_CreateQuestionField,
    "q30": CareerAnchors_CreateQuestionField,
    "q31": CareerAnchors_CreateQuestionField,
    "q32": CareerAnchors_CreateQuestionField,
    "q33": CareerAnchors_CreateQuestionField,
    "q34": CareerAnchors_CreateQuestionField,
    "q35": CareerAnchors_CreateQuestionField,
    "q36": CareerAnchors_CreateQuestionField,
    "q37": CareerAnchors_CreateQuestionField,
    "q38": CareerAnchors_CreateQuestionField,
    "q39": CareerAnchors_CreateQuestionField,
    "q40": CareerAnchors_CreateQuestionField,
}

CAREER_ANCHORS_FAVORITES_FIELDS = {
    "favorite1": CareerAnchors_CreateFavoriteField,
    "favorite2": CareerAnchors_CreateFavoriteField,
    "favorite3": CareerAnchors_CreateFavoriteField,
}

CareerAnchorsQuestionsForm = forms.modelform_factory(
    models.CareerAnchorsInput,
    exclude=("onboard", "favorite1", "favorite2", "favorite3"),
    labels={
        "q1": (
            "Me gustaría ser tan bueno en lo que hago que la gente me pida"
            " continuamente consejos y sugerencias"
        ),
        "q2": (
            "Me encuentro más satisfecho con mi trabajo cuando puedo integrar y"
            " gestionar los esfuerzos de los demás"
        ),
        "q3": (
            "Me gustaría tener una carrera que me permita autonomía y decidir"
            " los plazos"
        ),
        "q4": (
            "La seguridad y la estabilidad son más importantes para mí que la"
            " libertad y autonomía"
        ),
        "q5": (
            "Siempre estoy buscando ideas que me permitan tener mi propio"
            " negocio"
        ),
        "q6": (
            "Considero que alcanzo el éxito en mi carrera sólo si tengo la"
            " sensación de haber contribuido al bienestar común"
        ),
        "q7": (
            "Me gustaría una carrera en la que pueda resolver problemas o salir"
            " ganando en situaciones muy desafiantes"
        ),
        "q8": (
            "Preferiría dejar mi empresa antes que ocupar un puesto que"
            " comprometiera mi atención a mi familia y vida personal"
        ),
        "q9": (
            "Para mí el éxito consiste en desarrollar mis capacidades técnicas"
            " o funcionales hasta convertirme en un experto"
        ),
        "q10": (
            "Me gustaría estar a cargo de una organización compleja y tomar"
            " decisiones que afecten a muchas personas"
        ),
        "q11": (
            "Estoy más satisfecho cuando tengo plena libertad para definir mis"
            " propias actividades, plazos y procedimientos"
        ),
        "q12": (
            "Preferiría dejar mi empresa antes que aceptar un proyecto que"
            " afectara mi seguridad dentro de la organización"
        ),
        "q13": (
            "Crear mi propio negocio es más importante que alcanzar un puesto"
            " directivo de alto nivel en otra organización"
        ),
        "q14": (
            "Me encuentro más satisfecho con mi carrera cuando puedo poner mi"
            " talento al servicio de los demás"
        ),
        "q15": (
            "Alcanzo el éxito en mi carrera sólo si me enfrento y supero"
            " grandes desafíos y retos"
        ),
        "q16": (
            "Me gustaría una carrera que me permita integrar mis necesidades"
            " personales, familiares y profesionales"
        ),
        "q17": (
            "Me atrae más llegar a ser un directivo senior dentro de mi área"
            " funcional antes que llegar a ser Director General"
        ),
        "q18": (
            "Alcanzo el éxito en mi carrera sólo si llego a ser director"
            " general de alguna empresa"
        ),
        "q19": (
            "Alcanzo el éxito en mi carrera sólo si logro autonomía y libertad"
            " plena"
        ),
        "q20": (
            "Busco trabajo dentro de organizaciones que me proporcionen"
            " seguridad y estabilidad"
        ),
        "q21": (
            "Me encuentro más satisfecho con mi carrera cuando he creado algo"
            " que es el resultado de mis propias ideas y esfuerzos"
        ),
        "q22": (
            "Es más importante para mí utilizar mis capacidades para crear un"
            " mundo donde se viva y trabaje mejor que tener un puesto directivo"
            " de alto nivel"
        ),
        "q23": (
            "Me he encontrado más satisfecho en mi carrera cuando he resuelto"
            " problemas aparentemente sin solución o he vencido cuando parecía"
            " imposible hacerlo"
        ),
        "q24": (
            "Me encuentro satisfecho con mi vida sólo cuando consigo alcanzar"
            " un equilibrio entre las exigencias de mi vida personal, familiar"
            " y profesional"
        ),
        "q25": (
            "Preferiría dejar mi empresa antes que aceptar un proyecto que me"
            " obligara a dejar mi área de especialización"
        ),
        "q26": (
            "Me atrae más llegar a ser director general que un directivo senior"
            " dentro de mi área de especialización"
        ),
        "q27": (
            "La oportunidad de realizar un trabajo según mis propios criterios,"
            " sin normas y limitaciones es más importante para mí que la"
            " seguridad"
        ),
        "q28": (
            "Me encuentro más satisfecho con mi trabajo cuando considero que he"
            " alcanzado seguridad financiera y profesional"
        ),
        "q29": (
            "Considero que alcanzo el éxito en mi carrera sólo si consigo crear"
            " o construir algo que es completamente mi propio producto o idea"
        ),
        "q30": (
            "Me gustaría tener una carrera que suponga una gran contribución a"
            " la humanidad y a la sociedad"
        ),
        "q31": (
            "Busco oportunidades de trabajo que pongan a prueba mi capacidad"
            " para resolver problemas o para competir"
        ),
        "q32": (
            "Encontrar el equilibrio entre las exigencias de mi vida personal y"
            " profesional es más importante que conseguir un puesto directivo"
            " de alto nivel"
        ),
        "q33": (
            "Me encuentro más satisfecho con mi trabajo cuando tengo"
            " oportunidad de usar mis capacidades y talentos"
        ),
        "q34": (
            "Preferiría dejar mi empresa antes que aceptar un puesto que me"
            " aleje del camino hacia la dirección general"
        ),
        "q35": (
            "Preferiría dejar mi empresa antes que aceptar un puesto que limite"
            " mi autonomía y libertad"
        ),
        "q36": (
            "Me gustaría tener una carrera que me permita sentir un cierto"
            " nivel de seguridad y estabilidad"
        ),
        "q37": "Me gustaría crear y construir mi propio negocio",
        "q38": (
            "Preferiría dejar mi empresa antes que aceptar un proyecto que"
            " imitara mi capacidad de ayudar a los demás"
        ),
        "q39": (
            "Trabajar con problemas que aparentemente no tienen solución es más"
            " importante que alcanzar un puesto directivo de alto nivel"
        ),
        "q40": (
            "He buscado siempre oportunidades profesionales que no interfieran"
            " demasiado con mis preocupaciones personales y familiares"
        ),
    },
    formfield_callback=lambda field, **kwargs: CAREER_ANCHORS_QUESTION_FIELDS[
        field.name
    ](**kwargs),
)


class CareerAnchorsValidation(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        favorite1 = cleaned_data["favorite1"]
        favorite2 = cleaned_data["favorite2"]
        favorite3 = cleaned_data["favorite3"]

        if favorite1 == favorite2:
            raise forms.ValidationError(
                "La elección 1 debe ser distinta a la 2",
            )
        if favorite2 == favorite3:
            raise forms.ValidationError(
                "La elección 2 debe ser distinta a la 3",
            )
        if favorite3 == favorite1:
            raise forms.ValidationError(
                "La elección 3 debe ser distinta a la 1",
            )


CareerAnchorsFavoritesForm = forms.modelform_factory(
    models.CareerAnchorsInput,
    form=CareerAnchorsValidation,
    fields=("favorite1", "favorite2", "favorite3"),
    labels={
        "favorite1": "Elección 1",
        "favorite2": "Elección 2",
        "favorite3": "Elección 3",
    },
    formfield_callback=lambda field, **kwargs: CAREER_ANCHORS_FAVORITES_FIELDS[
        field.name
    ](**kwargs),
)


class CareerAnchorsFormFacade:
    def __init__(self, *args, instance=None, **kwargs):
        self.__questions_form = CareerAnchorsQuestionsForm(
            instance=instance, **kwargs
        )
        self.__favorites_form = CareerAnchorsFavoritesForm(
            instance=instance, **kwargs
        )

        self.__instance = (
            models.CareerAnchorsInput() if instance is None else instance
        )

    def save(self):
        data = self.__questions_form.cleaned_data

        self.__instance.q1 = data["q1"]
        self.__instance.q2 = data["q2"]
        self.__instance.q3 = data["q3"]
        self.__instance.q4 = data["q4"]
        self.__instance.q5 = data["q5"]
        self.__instance.q6 = data["q6"]
        self.__instance.q7 = data["q7"]
        self.__instance.q8 = data["q8"]
        self.__instance.q9 = data["q9"]
        self.__instance.q10 = data["q10"]
        self.__instance.q11 = data["q11"]
        self.__instance.q12 = data["q12"]
        self.__instance.q13 = data["q13"]
        self.__instance.q14 = data["q14"]
        self.__instance.q15 = data["q15"]
        self.__instance.q16 = data["q16"]
        self.__instance.q17 = data["q17"]
        self.__instance.q18 = data["q18"]
        self.__instance.q19 = data["q19"]
        self.__instance.q20 = data["q20"]
        self.__instance.q21 = data["q21"]
        self.__instance.q22 = data["q22"]
        self.__instance.q23 = data["q23"]
        self.__instance.q24 = data["q24"]
        self.__instance.q25 = data["q25"]
        self.__instance.q26 = data["q26"]
        self.__instance.q27 = data["q27"]
        self.__instance.q28 = data["q28"]
        self.__instance.q29 = data["q29"]
        self.__instance.q30 = data["q30"]
        self.__instance.q31 = data["q31"]
        self.__instance.q32 = data["q32"]
        self.__instance.q33 = data["q33"]
        self.__instance.q34 = data["q34"]
        self.__instance.q35 = data["q35"]
        self.__instance.q36 = data["q36"]
        self.__instance.q37 = data["q37"]
        self.__instance.q38 = data["q38"]
        self.__instance.q39 = data["q39"]
        self.__instance.q40 = data["q40"]

        data = self.__favorites_form.cleaned_data

        self.__instance.favorite1 = data["favorite1"]
        self.__instance.favorite2 = data["favorite2"]
        self.__instance.favorite3 = data["favorite3"]

        self.__instance.save()

    def is_valid(self):
        return (
            self.__questions_form.is_valid()
            and self.__favorites_form.is_valid()
        )

    @property
    def instance(self):
        return self.__instance

    @property
    def questions(self):
        return self.__questions_form

    @property
    def favorites(self):
        return self.__favorites_form
