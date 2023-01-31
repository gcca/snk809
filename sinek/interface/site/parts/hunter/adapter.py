from typing import List, Set, Tuple

from sinek.domain.service import (AnchorEvaluationService,
                                  CandidateTestChecklistService,
                                  ComplexEvaluationService,
                                  DISCEvaluationService,
                                  TMMS24EvaluationService)


class DISCResultViewAdapter:
  """ View adapter for DISC result """

  Personality = DISCEvaluationService.Personality

  def __init__(self, result: DISCEvaluationService.Result):
    self.result = result

  PERSONALITIES = {
    Personality.ACOMODADIZO: 'ACOMODADIZO',
    Personality.AFILIADOR: 'AFILIADOR',
    Personality.ANALISTA: 'ANALISTA',
    Personality.ASESOR: 'ASESOR',
    Personality.COOPERATIVO: 'COOPERATIVO',
    Personality.CREADOR: 'CREADOR',
    Personality.DIRECTOR: 'DIRECTOR',
    Personality.EMPRENDEDOR: 'EMPRENDEDOR',
    Personality.ESPECIALISTA: 'ESPECIALISTA',
    Personality.ESTRATEGA: 'ESTRATEGA',
    Personality.INDIVIDUALISTA: 'INDIVIDUALISTA',
    Personality.INVESTIGADOR: 'INVESTIGADOR',
    Personality.MOTIVADOR: 'MOTIVADOR',
    Personality.NEGOCIADOR: 'NEGOCIADOR',
    Personality.ORGANIZADOR: 'ORGANIZADOR',
    Personality.PERFECCIONISTA: 'PERFECCIONISTA',
    Personality.PERSEVERANTE: 'PERSEVERANTE',
    Personality.PERSUASIVO: 'PERSUASIVO',
    Personality.PIONERO: 'PIONERO',
    Personality.TORBELLINO: 'TORBELLINO',
    Personality.PATRONESUNIFORMES: 'PATRONES UNIFORMES',
  }

  @property
  def personalityText(self) -> str:
    return self.PERSONALITIES[self.result.personality]

  @property
  def pointsUserD(self) -> str:
    return self.result.pointsUser.d

  @property
  def pointsUserI(self) -> str:
    return self.result.pointsUser.i

  @property
  def pointsUserS(self) -> str:
    return self.result.pointsUser.s

  @property
  def pointsUserC(self) -> str:
    return self.result.pointsUser.c

  @property
  def pointsPersonalityD(self) -> str:
    return self.result.pointsPersonality.d

  @property
  def pointsPersonalityI(self) -> str:
    return self.result.pointsPersonality.i

  @property
  def pointsPersonalityS(self) -> str:
    return self.result.pointsPersonality.s

  @property
  def pointsPersonalityC(self) -> str:
    return self.result.pointsPersonality.c

  @property
  def pointsUserText(self) -> Tuple[int, int, int, int]:
    return self.result.pointsUser

  @property
  def pointsPersonalityText(self) -> Tuple[int, int, int, int]:
    return self.result.pointsPersonality


class TMMS24ResultViewAdapter:
  """ View adapter for a TMMS24 result """

  Personality = TMMS24EvaluationService.Personality

  def __init__(self, result: TMMS24EvaluationService.Result):
    self.result = result

  PERSONALITIES = {
    Personality.INADECUADO: 'INADECUADO',
    Personality.ADECUADO: 'ADECUADO',
    Personality.EXCELENTE: 'EXCELENTE'
  }

  @property
  def atencionResultText(self) -> str:
    return self.PERSONALITIES[self.result.atencion]

  @property
  def claridadResultText(self) -> str:
    return self.PERSONALITIES[self.result.claridad]

  @property
  def reparacionResultText(self) -> str:
    return self.PERSONALITIES[self.result.reparacion]


class AnchorResultViewAdapter:
  """ View adapter for a Career Anchor result """

  Personality = AnchorEvaluationService.Personality

  PERSONALITIES = {
    Personality.TF: 'Técnica Funcional',
    Personality.DG: 'Dirección General',
    Personality.AI: 'Autonomía',
    Personality.SE: 'Seguridad y estabilidad',
    Personality.CE: 'Creatividad empresarial',
    Personality.SC: 'Servicio-dedicación a una causa',
    Personality.ED: 'Exclusivamente desafío',
    Personality.EV: 'Estilo de vida',
  }

  def __init__(self, result: AnchorEvaluationService.Result):
    self.result = result

  @property
  def firstResultText(self) -> str:
    return self.PERSONALITIES[self.result.first]

  @property
  def secondResultText(self) -> str:
    return self.PERSONALITIES[self.result.second]

  @property
  def thirdResultText(self) -> str:
    return self.PERSONALITIES[self.result.third]

  @property
  def totalsResultText(self) -> str:
    return self.result.totals


class ComplexResultViewAdapter:
  """ View adapter for a Complex Instructions result"""

  def __init__(self, result: ComplexEvaluationService.Result):
    self.result = result

  Level = ComplexEvaluationService.Level

  LEVEL = {
    Level.ADECUADO: 'Adecuado',
    Level.REGULAR: 'Regular',
    Level.INFERIOR: 'Inferior',
  }

  @property
  def levelResultText(self) -> str:
    return self.LEVEL[self.result.level]

  @property
  def pointsResultText(self) -> str:
    return self.result.points

  @property
  def percentageResultText(self) -> str:
    return self.result.percentage


class ChecklistViewAdapter:
  """ View adapter for a Candidate Test Checklist """

  def __init__(self, check: CandidateTestChecklistService.Check):
    self.check = check

  @property
  def candidateName(self) -> str:
    return self.check.candidate.name

  @property
  def candidateEmail(self) -> str:
    return self.check.candidate.email

  @property
  def discCompleted(self) -> bool:
    return self.check.disc_completed

  @property
  def tmms24Completed(self) -> bool:
    return self.check.tmms24_completed

  @property
  def anchorCompleted(self) -> bool:
    return self.check.anchor_completed

  @property
  def complexCompleted(self) -> bool:
    return self.check.complex_completed

  # TODO: solución temporal
  @property
  def completedCounter(self) -> str:
    totalTests = 6  # por mientras🤠

    counter = 0

    if self.check.disc_completed:
      counter += 1
    if self.check.tmms24_completed:
      counter += 1
    if self.check.anchor_completed:
      counter += 1
    if self.check.complex_completed:
      counter += 1

    return f'{counter}/{totalTests}'
