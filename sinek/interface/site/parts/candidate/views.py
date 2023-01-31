from datetime import datetime, timezone

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from neom.core.ioc import Wireable, Wired

from sinek.domain.service import CandidateTestChecklistService
from sinek.interface.site.parts.hunter.facade import \
  CandidateTestChecklistServiceFacade

from .common import CandidateViewBase
from .facade import (RecordAnchorAnswersServiceFacade,
                     RecordComplexAnswersServiceFacade,
                     RecordDISCAnswersServiceFacade,
                     RecordTMMS24AnswersServiceFacade)
from .forms import (AnchorTestForm, ComplexTestForm, DISCTestForm,
                    TMMS24TestForm)


class DashboardView(CandidateViewBase, TemplateView):
  template_name = 'desktop/candidate/dashboard.html'

  def get_context_data(self, **kwargs) -> dict:
    candidateTestCheckListServiceFacade = CandidateTestChecklistServiceFacade()
    candidateView = candidateTestCheckListServiceFacade.ListForOneCandidate(
      self.candidate.email)

    context = super().get_context_data(**kwargs)
    context['candidateView'] = candidateView

    return context


class DiscSuccessView(CandidateViewBase, TemplateView):
  template_name = 'desktop/candidate/test/success.html'


@Wireable
class ComplexTestView(CandidateViewBase, FormView):
  template_name = 'desktop/candidate/test/complex.html'
  form_class = ComplexTestForm
  success_url = reverse_lazy('site:candidate:disc-success')

  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  def get(self, request):
    complexCompleted = self.candidateTestChecklistService.IsComplexCompleted(
      self.request.user.email)
    if complexCompleted:
      return redirect(reverse('site:candidate:disc-success'))
    # TODO: modificar esta debilidad de la implementación
    request.session['initialTime'] = datetime.now(timezone.utc).timestamp()
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    complexQuestions = ComplexTestView.CreateQuestionsComplex()
    context['questions'] = complexQuestions

    return context

  def form_valid(self, form: ComplexTestForm):
    recordComplexAnswersServiceFacade = RecordComplexAnswersServiceFacade()
    email = self.request.user.email
    recordComplexAnswersServiceFacade.Record(email, form, self.request.session)

    return super().form_valid(form)

  @staticmethod
  def CreateQuestionsComplex():
    QuestionTuples = [
      ComplexTestView.CreateQuestion(1, '3000 soles | Incendios | 2 de enero de 1976'),
      ComplexTestView.CreateQuestion(2, '1000 soles | Vida | 22 de octubre de 1975'),
      ComplexTestView.CreateQuestion(3, '4000 soles | Accidentes | 14 de setiembre 1975'),
      ComplexTestView.CreateQuestion(4, '2000 soles | Vida | 13 de noviembre de 1976'),
      ComplexTestView.CreateQuestion(5, '4000 soles | Incendios | 17 de mayo de 1976'),
      ComplexTestView.CreateQuestion(6, '3000 soles | Accidentes | 12 de octubre de 1975'),
      ComplexTestView.CreateQuestion(7, '5000 soles | Vida | 16 de febrero de 1976'),
      ComplexTestView.CreateQuestion(8, '1000 soles | Incendios | 03 de agosto de 1976'),
      ComplexTestView.CreateQuestion(9, '4000 soles | Incendios | 11 de agosto de 1976'),
      ComplexTestView.CreateQuestion(10, '2000 soles | Accidentes | 21 de mayo de 1975'),
      ComplexTestView.CreateQuestion(11, '5000 soles | Vida | 09 de marzo de 1975'),
      ComplexTestView.CreateQuestion(12, '3000 soles | Incendios | 17 de julio de 1976'),
      ComplexTestView.CreateQuestion(13, '1000 soles | Accidentes | 04 de junio de 1976'),
      ComplexTestView.CreateQuestion(14, '1000 soles | Vida | 23 de noviembre de 1976'),
      ComplexTestView.CreateQuestion(15, '5000 soles | Vida | 18 de abril de 1975'),
      ComplexTestView.CreateQuestion(16, '2000 soles | Accidentes | 24 de diciembre de 1976'),
      ComplexTestView.CreateQuestion(17, '5000 soles | Accidentes | 19 de abril de 1975'),
      ComplexTestView.CreateQuestion(18, '2000 soles | Vida | 07 de diciembre de 1976'),
      ComplexTestView.CreateQuestion(19, '4000 soles | Incendios | 26 de mayo de 1975'),
      ComplexTestView.CreateQuestion(20, '3000 soles | Accidentes | 06 de enero de 1976'),
      ComplexTestView.CreateQuestion(21, '5000 soles | Vida | 29 de marzo de 1975'),
      ComplexTestView.CreateQuestion(22, '3000 soles | Vida | 28 de junio de 1975'),
      ComplexTestView.CreateQuestion(23, '4000 soles | Accidentes | 08 de febrero de 1976'),
      ComplexTestView.CreateQuestion(24, '1000 soles | Incendios | 27 de julio de 1975'),
      ComplexTestView.CreateQuestion(25, '2000 soles | Accidentes | 21 de enero de 1976'),
    ]
    return QuestionTuples

  @staticmethod
  def CreateQuestion(number, statement):
    question = {'number': number,
                'statement': statement}
    return question


@Wireable
class DiscTestView(CandidateViewBase, FormView):
  template_name = 'desktop/candidate/test/disc.html'
  form_class = DISCTestForm
  success_url = reverse_lazy('site:candidate:disc-success')

  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  def get(self, request):
    discCompleted = self.candidateTestChecklistService.IsDiscCompleted(
      self.request.user.email)
    if discCompleted:
      return redirect(reverse('site:candidate:disc-success'))
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    discQuestions = DiscTestView.CreateQuestionsDisc()
    context['discQuestions'] = discQuestions

    return context

  def form_valid(self, form):
    recordDISCAnswersServiceFacade = RecordDISCAnswersServiceFacade()

    email = self.request.user.email
    recordDISCAnswersServiceFacade.Record(email, form)

    return super().form_valid(form)

  @staticmethod
  def CreateQuestionsDisc():
    QuestionTuples = [
      DiscTestView.CreateQuestion(1, ('Expresivo', 'Sumiso', 'Enérgico', 'Controlado')),
      DiscTestView.CreateQuestion(2, ('Fuerte de carácter', 'Cuidadoso', 'Emocional', 'Satisfecho')),
      DiscTestView.CreateQuestion(3, ('Correcto', 'Tranquilo', 'Pionero', 'Influyente')),
      DiscTestView.CreateQuestion(4, ('Preciso', 'Dominante', 'Dispuesto', 'Atractivo')),
      DiscTestView.CreateQuestion(5, ('Ecuánime', 'Estimulante', 'Meticuloso', 'Decidido')),
      DiscTestView.CreateQuestion(6, ('Tímido', 'Exigente', 'Paciente', 'Cautivador')),
      DiscTestView.CreateQuestion(7, ('Concienzudo', 'Buena compañia', 'Bondadoso', 'Depende de si')),
      DiscTestView.CreateQuestion(8, ('Agradable', 'Con dominio propio', 'Juguetón', 'Persistente')),
      DiscTestView.CreateQuestion(9, ('Animoso', 'Conversador', 'Bonachon', 'Conservador')),
      DiscTestView.CreateQuestion(10, ('Contento', 'Impaciente', 'Convicente', 'Resignado')),
      DiscTestView.CreateQuestion(11, ('Respetuoso', 'Socialmente desenvuelto', 'Agresivo', 'Apacible')),
      DiscTestView.CreateQuestion(12, ('Aplomo', 'Convencional', 'Toma riesgos', 'Servicial')),
      DiscTestView.CreateQuestion(13, ('Seguro de sí mismo', 'Cooperativo', 'Disputador', 'Relajado, sin tensiones')),
      DiscTestView.CreateQuestion(14, ('Inquieto', 'Disciplinado', 'Inspirador', 'Considerado')),
      DiscTestView.CreateQuestion(15, ('Diplomático', 'Valiente', 'Compasivo', 'Optimista')),
      DiscTestView.CreateQuestion(16, ('Encantador', 'Positivo', 'Indulgente', 'Riguroso')),
      DiscTestView.CreateQuestion(17, ('Aventurero', 'Entusiasta', 'Sigue las reglas', 'Leal')),
      DiscTestView.CreateQuestion(18, ('Humilde', 'Oyente atento', 'Entretenido', 'Con fuerza de voluntad')),
      DiscTestView.CreateQuestion(19, ('Divertido', 'Obediente', 'Discreto', 'Competitivo')),
      DiscTestView.CreateQuestion(20, ('Cauteloso', 'Amistoso', 'Vigoroso', 'Persuasivo')),
      DiscTestView.CreateQuestion(21, ('Reservado', 'Franco', 'Estricto', 'Elocuente')),
      DiscTestView.CreateQuestion(22, ('Cortés', 'Animado', 'Decisivo', 'Preciso')),
      DiscTestView.CreateQuestion(23, ('Asertivo', 'Sociable', 'Estable', 'Metódico')),
      DiscTestView.CreateQuestion(24, ('Extrovertido', 'Intrepido', 'Moderado', 'Perfeccionista')),
    ]
    return QuestionTuples

  @staticmethod
  def CreateQuestion(number, answers):
    question = {'number': number,
                'enumeratedAnswers': enumerate(answers, 1)}
    return question


@Wireable
class AnchorTestView(CandidateViewBase, FormView):
  template_name = 'desktop/candidate/test/anchor.html'
  form_class = AnchorTestForm
  success_url = reverse_lazy('site:candidate:disc-success')

  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  def get(self, request):
    anchorCompleted = self.candidateTestChecklistService.IsAnchorCompleted(
      self.request.user.email)
    if anchorCompleted:
      return redirect(reverse('site:candidate:disc-success'))
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    anchorQuestions = AnchorTestView.CreateQuestionsAnchor()
    context['questions'] = anchorQuestions
    context['favourites'] = [1, 2, 3]

    return context

  def form_valid(self, form):
    recordAnchorAnswersServiceFacade = RecordAnchorAnswersServiceFacade()

    email = self.request.user.email
    recordAnchorAnswersServiceFacade.Record(email, form)
    return super().form_valid(form)

  @staticmethod
  def CreateQuestionsAnchor():
    QuestionTuples = [
      AnchorTestView.CreateQuestion(1, 'Me gustaría ser tan bueno en lo que hago que la gente me pida continuamente consejos y sugerencias'),
      AnchorTestView.CreateQuestion(2, 'Me encuentro más satisfecho con mi trabajo cuando puedo integrar y gestionar los esfuerzos delos demás'),
      AnchorTestView.CreateQuestion(3, 'Me gustaría tener una carrera que me permita autonomía y decidir los plazos'),
      AnchorTestView.CreateQuestion(4, 'La seguridad y la estabilidad son más importantes para mí que la libertad y autonomía'),
      AnchorTestView.CreateQuestion(5, 'Siempre estoy buscando ideas que me permitan tener mi propio negocio'),
      AnchorTestView.CreateQuestion(6, 'Considero que alcanzo el éxito en mi carrera sólo si tengo la sensación de haber contribuido al bienestar común'),
      AnchorTestView.CreateQuestion(7, 'Me gustaría una carrera en la que pueda resolver problemas o salir ganando en situaciones muy desafiantes'),
      AnchorTestView.CreateQuestion(8, 'Preferiría dejar mi empresa antes que ocupar un puesto que comprometiera mi atención a mi familia y vida personal'),
      AnchorTestView.CreateQuestion(9, 'Para mí el éxito consiste en desarrollar mis capacidades técnicas o funcionales hasta convertirme en un experto'),
      AnchorTestView.CreateQuestion(10, 'Me gustaría estar a cargo de una organización compleja y tomar decisiones que afecten a muchas personas'),
      AnchorTestView.CreateQuestion(11, 'Estoy más satisfecho cuando tengo plena libertad para definir mis propias actividades, plazos y procedimientos'),
      AnchorTestView.CreateQuestion(12, 'Preferiría dejar mi empresa antes que aceptar un proyecto que afectara mi seguridad dentro de la organización'),
      AnchorTestView.CreateQuestion(13, 'Crear mi propio negocio es más importante que alcanzar un puesto directivo de alto nivel en otra organización'),
      AnchorTestView.CreateQuestion(14, 'Me encuentro más satisfecho con mi carrera cuando puedo poner mi talento al servicio de los demás'),
      AnchorTestView.CreateQuestion(15, 'Alcanzo el éxito en mi carrera sólo si me enfrento y supero grandes desafíos y retos'),
      AnchorTestView.CreateQuestion(16, 'Me gustaría una carrera que me permita integrar mis necesidades personales, familiares y profesionales'),
      AnchorTestView.CreateQuestion(17, 'Me atrae más llegar a ser un directivo senior dentro de mi área funcional antes que llegar a ser Director General'),
      AnchorTestView.CreateQuestion(18, 'Alcanzo el éxito en mi carrera sólo si llego a ser director general de alguna empresa'),
      AnchorTestView.CreateQuestion(19, 'Alcanzo el éxito en mi carrera sólo si logro autonomía y libertad plena'),
      AnchorTestView.CreateQuestion(20, 'Busco trabajo dentro de organizaciones que me proporcionen seguridad y estabilidad'),
      AnchorTestView.CreateQuestion(21, 'Me encuentro más satisfecho con mi carrera cuando he creado algo que es el resultado de mis propias ideas y esfuerzos'),
      AnchorTestView.CreateQuestion(22, 'Es más importante para mí utilizar mis capacidades para crear un mundo donde se viva y trabaje mejor que tener un puesto directivo de alto nivel'),
      AnchorTestView.CreateQuestion(23, 'Me he encontrado más satisfecho en mi carrera cuando he resuelto problemas aparentemente sin solución o he vencido cuando parecía imposible hacerlo'),
      AnchorTestView.CreateQuestion(24, 'Me encuentro satisfecho con mi vida sólo cuando consigo alcanzar un equilibrio entre las exigencias de mi vida personal, familiar y profesional'),
      AnchorTestView.CreateQuestion(25, 'Preferiría dejar mi empresa antes que aceptar un proyecto que me obligara a dejar mi área de especialización'),
      AnchorTestView.CreateQuestion(26, 'Me atrae más llegar a ser director general que un directivo senior dentro de mi área de especialización'),
      AnchorTestView.CreateQuestion(27, 'La oportunidad de realizar un trabajo según mis propios criterios, sin normas y limitaciones es más importante para mí que la seguridad'),
      AnchorTestView.CreateQuestion(28, 'Me encuentro más satisfecho con mi trabajo cuando considero que he alcanzado seguridad financiera y profesional'),
      AnchorTestView.CreateQuestion(29, 'Considero que alcanzo el éxito en mi carrera sólo si consigo crear o construir algo que es completamente mi propio producto o idea'),
      AnchorTestView.CreateQuestion(30, 'Me gustaría tener una carrera que suponga una gran contribución a la humanidad y a la sociedad'),
      AnchorTestView.CreateQuestion(31, 'Busco oportunidades de trabajo que pongan a prueba mi capacidad para resolver problemas o para competir'),
      AnchorTestView.CreateQuestion(32, 'Encontrar el equilibrio entre las exigencias de mi vida personal y profesional es más importante que conseguir un puesto directivo de alto nivel'),
      AnchorTestView.CreateQuestion(33, 'Me encuentro más satisfecho con mi trabajo cuando tengo oportunidad de usar mis capacidades y talentos'),
      AnchorTestView.CreateQuestion(34, 'Preferiría dejar mi empresa antes que aceptar un puesto que me aleje del camino hacia la dirección general'),
      AnchorTestView.CreateQuestion(35, 'Preferiría dejar mi empresa antes que aceptar un puesto que limite mi autonomía y libertad'),
      AnchorTestView.CreateQuestion(36, 'Me gustaría tener una carrera que me permita sentir un cierto nivel de seguridad y estabilidad'),
      AnchorTestView.CreateQuestion(37, 'Me gustaría crear y construir mi propio negocio'),
      AnchorTestView.CreateQuestion(38, 'Preferiría dejar mi empresa antes que aceptar un proyecto que imitara mi capacidad de ayudar a los demás'),
      AnchorTestView.CreateQuestion(39, 'Trabajar con problemas que aparentemente no tienen solución es más importante que alcanzar un puesto directivo de alto nivel'),
      AnchorTestView.CreateQuestion(40, 'He buscado siempre oportunidades profesionales que no interfieran demasiado con mis preocupaciones personales y familiares'),
    ]
    return QuestionTuples

  @staticmethod
  def CreateQuestion(number, statement):
    question = {'number': number,
                'statement': statement}
    return question


@Wireable
class Tmms24TestView(CandidateViewBase, FormView):
  template_name = 'desktop/candidate/test/tmms24.html'
  form_class = TMMS24TestForm
  success_url = reverse_lazy('site:candidate:disc-success')

  candidateTestChecklistService: Wired[CandidateTestChecklistService]

  def get(self, request):
    tmms24Completed = self.candidateTestChecklistService.IsTmms24Completed(
      self.request.user.email)
    if tmms24Completed:
      return redirect(reverse('site:candidate:disc-success'))
    return super().get(request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    tmms24Questions = Tmms24TestView.CreateQuestionsTmms24()
    context['questions'] = tmms24Questions

    return context

  def form_valid(self, form):
    recordTMMS24AnswersServiceFacade = RecordTMMS24AnswersServiceFacade()
    email = self.request.user.email
    recordTMMS24AnswersServiceFacade.Record(email, form)
    return super().form_valid(form)

  @staticmethod
  def CreateQuestionsTmms24():
    QuestionTuples = [
      Tmms24TestView.CreateQuestion(1, 'Presto mucha atención a los sentimientos'),
      Tmms24TestView.CreateQuestion(2, 'Normalmente me preocupo por lo que siento'),
      Tmms24TestView.CreateQuestion(3, 'Normalmente dedico tiempo a pensar en mis emociones'),
      Tmms24TestView.CreateQuestion(4, 'Pienso que merece la pena prestar atención a mis emociones y estado de ánimo'),
      Tmms24TestView.CreateQuestion(5, 'Dejo que mis sentimientos afecten mis pensamientos'),
      Tmms24TestView.CreateQuestion(6, 'Pienso en mi estado de ánimo constantemente'),
      Tmms24TestView.CreateQuestion(7, 'A menudo pienso en mis sentimientos'),
      Tmms24TestView.CreateQuestion(8, 'Presto mucha atención a cómo me siento'),
      Tmms24TestView.CreateQuestion(9, 'Tengo claro mis sentimientos'),
      Tmms24TestView.CreateQuestion(10, 'Frecuentemente puedo definir mis sentimientos'),
      Tmms24TestView.CreateQuestion(11, 'Casi siempre sé cómo me siento'),
      Tmms24TestView.CreateQuestion(12, 'Normalmente conozco mis sentimientos sobre las personas'),
      Tmms24TestView.CreateQuestion(13, 'A menudo me doy cuenta de mis sentimientos en diferentes situaciones'),
      Tmms24TestView.CreateQuestion(14, 'Siempre puedo decir cómo me sien'),
      Tmms24TestView.CreateQuestion(15, 'A veces puedo decir cuáles son mis emociones'),
      Tmms24TestView.CreateQuestion(16, 'Puedo llegar a comunicar mis sentimientos'),
      Tmms24TestView.CreateQuestion(17, 'Aunque a veces me siento triste, suelo tener una visión optimista'),
      Tmms24TestView.CreateQuestion(18, 'Aunque a veces me sienta mal, procuro pensar en cosas agradables'),
      Tmms24TestView.CreateQuestion(19, 'Cuando estoy triste, pienso en todos los placeres de la vida.'),
      Tmms24TestView.CreateQuestion(20, 'Intento tener pensamientos positivos aunque me sienta mal'),
      Tmms24TestView.CreateQuestion(21, 'Si doy demasiadas vueltas a las cosas, complicándolas, trato de calmarme'),
      Tmms24TestView.CreateQuestion(22, 'Me preocupo por tener un buen estado de ánimo'),
      Tmms24TestView.CreateQuestion(23, 'Tengo mucha energía cuando me siento feliz'),
      Tmms24TestView.CreateQuestion(24, 'Cuando estoy enfadado intento cambiar mi estado de ánimo'),
    ]
    return QuestionTuples

  @staticmethod
  def CreateQuestion(number, statement):
    question = {'number': number,
                'statement': statement}
    return question
