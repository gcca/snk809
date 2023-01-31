# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from typing import Dict

from django.template.response import TemplateResponse
from django.test import Client, TestCase

from .data.disc import CreateQuiz as CreateDiscQuiz
from .forms import DiscFormSet
from .models import DiscSelectAnswer, Evaluation, Option, Quiz


class EvaluationDiscFormTestCase(TestCase):
    def setUp(self):
        from sinek.infrastructure.persistence.orm.models import Freelancer

        freelancer = Freelancer.objects.create(
            name="Dummy",
            condition=Freelancer.ConditionChoices.TALENT,
            countryCode=123,
            isOnboarded=True,
        )

        CreateDiscQuiz()

        freelancerId = freelancer.id
        quizId = Quiz.ID.DISC

        self.evaluationUrl = f"/quizzes/{quizId}/evaluate/{freelancerId}/"
        self.freelancer = freelancer

        self.client = Client()

    def test_get_disc_quiz(self):
        response = self.client.get(self.evaluationUrl)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["freelancer"].name, "Dummy")
        self.assertIsInstance(response.context["form"], DiscFormSet)

    def test_send_empty_data(self):
        response = self.client.post(self.evaluationUrl)

        self._AssertFormWithError(response)

    def test_send_only_blank_body_data(self):
        data = {
            "disc-TOTAL_FORMS": "0",
            "disc-INITIAL_FORMS": "0",
        }

        response = self.client.post(self.evaluationUrl, data=data)

        self.assertEqual(response.status_code, 302)

    def test_send_only_incomplete_body_data(self):
        data = {
            "disc-TOTAL_FORMS": "1",
            "disc-INITIAL_FORMS": "0",
        }

        response = self.client.post(self.evaluationUrl, data=data)

        self._AssertFormWithError(response)

    def test_send_only_incomplete_subform_data(self):
        data = {
            "disc-TOTAL_FORMS": "1",
            "disc-INITIAL_FORMS": "0",
            "disc-0-Expresivo": "+",
        }

        response = self.client.post(self.evaluationUrl, data=data)

        self._AssertFormWithError(response)

    def test_send_default_data(self):
        data = self._CreateDiscData()

        response = self.client.post(self.evaluationUrl, data=data)

        self._AssertFormWithError(response)

    def test_without_plus(self):
        data = self._CreateDiscData()
        data["disc-0-Expresivo"] = "-"
        # No +

        response = self.client.post(self.evaluationUrl, data=data)

        self._AssertFormWithError(response)

    def test_without_minus(self):
        data = self._CreateDiscData()
        data["disc-0-Expresivo"] = "+"
        # No -

        response = self.client.post(self.evaluationUrl, data=data)

        self._AssertFormWithError(response)

    def test_extra_plusminus(self):
        data = self._CreateDiscData()
        data["disc-0-Expresivo"] = "+"
        data["disc-0-Sumiso"] = "-"
        data["disc-0-Enérgico"] = "+"

        response = self.client.post(self.evaluationUrl, data=data)

        self._AssertFormWithError(response)

    # FALTA MÁS VALIDACIONES CON LAS POSIBLES COMBINACIONES +,-,o
    # Y VALIDAR EL MENSAJE DE RETORNO

    def test_send_right_data(self):
        data = self._CreateDiscData()

        data.update(
            {
                "disc-0-Expresivo": "-",
                "disc-0-Sumiso": "+",
                "disc-1-Fuerte de carácter": "-",
                "disc-1-Cuidadoso": "+",
                "disc-2-Correcto": "-",
                "disc-2-Tranquilo": "+",
                "disc-3-Preciso": "-",
                "disc-3-Dominante": "+",
                "disc-4-Ecuánime": "-",
                "disc-4-Estimulante": "+",
                "disc-5-Tímido": "-",
                "disc-5-Exigente": "+",
                "disc-6-Concienzudo": "-",
                "disc-6-Buena compañia": "+",
                "disc-7-Agradable": "-",
                "disc-7-Con dominio propio": "+",
                "disc-8-Animoso": "-",
                "disc-8-Conversador": "+",
                "disc-9-Contento": "-",
                "disc-9-Impaciente": "+",
                "disc-10-Respetuoso": "-",
                "disc-10-Socialmente desenvuelto": "+",
                "disc-11-Aplomo": "-",
                "disc-11-Convencional": "+",
                "disc-12-Seguro de sí mismo": "-",
                "disc-12-Cooperativo": "+",
                "disc-13-Inquieto": "-",
                "disc-13-Disciplinado": "+",
                "disc-14-Diplomático": "-",
                "disc-14-Valiente": "+",
                "disc-15-Encantador": "-",
                "disc-15-Positivo": "+",
                "disc-16-Aventurero": "-",
                "disc-16-Entusiasta": "+",
                "disc-17-Humilde": "-",
                "disc-17-Oyente atento": "+",
                "disc-18-Divertido": "-",
                "disc-18-Obediente": "+",
                "disc-19-Cauteloso": "-",
                "disc-19-Amistoso": "+",
                "disc-20-Reservado": "-",
                "disc-20-Franco": "+",
                "disc-21-Cortés": "-",
                "disc-21-Animado": "+",
                "disc-22-Asertivo": "-",
                "disc-22-Sociable": "+",
                "disc-23-Extrovertido": "-",
                "disc-23-Intrepido": "+",
            }
        )

        response = self.client.post(self.evaluationUrl, data=data)

        self.assertEqual(response.status_code, 302)

        evaluations = Evaluation.objects.all()

        self.assertEqual(len(evaluations), 1)

        evaluation = evaluations[0]

        self.assertEqual(evaluation.freelancer.id, self.freelancer.id)
        self.assertEqual(evaluation.quiz.id, Quiz.ID.DISC)

        for answer in DiscSelectAnswer.objects.filter(evaluation=evaluation):
            options = Option.objects.filter(question=answer.question)

            self.assertGreater(len(options), 0)

            # Se supone que aquí se mantiene el orden de la db
            # Si falla, implementar los OrderedOption, OrderedQuestion, etc.
            expectedLeastOption = options[0]
            expectedMostOption = options[1]

            self.assertEqual(answer.leastOption, expectedLeastOption)
            self.assertEqual(answer.mostOption, expectedMostOption)

    # internal methods

    def _AssertFormWithError(self, response: TemplateResponse):
        self.assertEqual(response.status_code, 200)
        self.assertIn("form_with_error", response.context)
        self.assertTrue(response.context["form_with_error"])

    def _CreateDiscData(self) -> Dict[str, str]:
        """Returns a dict for DISC formset data with default value 'o'
        for each option in questions. For example:

        {
          'disc-0-Expresivo': 'o'
          'disc-0-Sumiso': 'o'
          'disc-0-Enérgico': 'o'
          'disc-0-Controlado': 'o'
          'disc-1-Fuerte de carácter': 'o'
          'disc-1-Cuidadoso': 'o'
          'disc-1-Emocional': 'o'
          'disc-1-Satisfecho': 'o'
          'disc-2-Correcto': 'o'
          'disc-2-Tranquilo': 'o'
          'disc-2-Pionero': 'o'
          'disc-2-Influyente': 'o'
          'disc-3-Preciso': 'o'
          'disc-3-Dominante': 'o'
          'disc-3-Dispuesto': 'o'
          'disc-3-Atractivo': 'o'
          'disc-4-Ecuánime': 'o'
          'disc-4-Estimulante': 'o'
          'disc-4-Meticuloso': 'o'
          'disc-4-Decidido': 'o'
          'disc-5-Tímido': 'o'
          'disc-5-Exigente': 'o'
          'disc-5-Paciente': 'o'
          'disc-5-Cautivador': 'o'
          'disc-6-Concienzudo': 'o'
          'disc-6-Buena compañia': 'o'
          'disc-6-Bondadoso': 'o'
          'disc-6-Depende de si': 'o'
          'disc-7-Agradable': 'o'
          'disc-7-Con dominio propio': 'o'
          'disc-7-Juguetón': 'o'
          'disc-7-Persistente': 'o'
          'disc-8-Animoso': 'o'
          'disc-8-Conversador': 'o'
          'disc-8-Bonachon': 'o'
          'disc-8-Conservador': 'o'
          'disc-9-Contento': 'o'
          'disc-9-Impaciente': 'o'
          'disc-9-Convicente': 'o'
          'disc-9-Resignado': 'o'
          'disc-10-Respetuoso': 'o'
          'disc-10-Socialmente desenvuelto': 'o'
          'disc-10-Agresivo': 'o'
          'disc-10-Apacible': 'o'
          'disc-11-Aplomo': 'o'
          'disc-11-Convencional': 'o'
          'disc-11-Toma riesgos': 'o'
          'disc-11-Servicial': 'o'
          'disc-12-Seguro de sí mismo': 'o'
          'disc-12-Cooperativo': 'o'
          'disc-12-Disputador': 'o'
          'disc-12-Relajado, sin tensiones': 'o'
          'disc-13-Inquieto': 'o'
          'disc-13-Disciplinado': 'o'
          'disc-13-Inspirador': 'o'
          'disc-13-Considerado': 'o'
          'disc-14-Diplomático': 'o'
          'disc-14-Valiente': 'o'
          'disc-14-Compasivo': 'o'
          'disc-14-Optimista': 'o'
          'disc-15-Encantador': 'o'
          'disc-15-Positivo': 'o'
          'disc-15-Indulgente': 'o'
          'disc-15-Riguroso': 'o'
          'disc-16-Aventurero': 'o'
          'disc-16-Entusiasta': 'o'
          'disc-16-Sigue las reglas': 'o'
          'disc-16-Leal': 'o'
          'disc-17-Humilde': 'o'
          'disc-17-Oyente atento': 'o'
          'disc-17-Entretenido': 'o'
          'disc-17-Con fuerza de voluntad': 'o'
          'disc-18-Divertido': 'o'
          'disc-18-Obediente': 'o'
          'disc-18-Discreto': 'o'
          'disc-18-Competitivo': 'o'
          'disc-19-Cauteloso': 'o'
          'disc-19-Amistoso': 'o'
          'disc-19-Vigoroso': 'o'
          'disc-19-Persuasivo': 'o'
          'disc-20-Reservado': 'o'
          'disc-20-Franco': 'o'
          'disc-20-Estricto': 'o'
          'disc-20-Elocuente': 'o'
          'disc-21-Cortés': 'o'
          'disc-21-Animado': 'o'
          'disc-21-Decisivo': 'o'
          'disc-21-Preciso': 'o'
          'disc-22-Asertivo': 'o'
          'disc-22-Sociable': 'o'
          'disc-22-Estable': 'o'
          'disc-22-Metódico': 'o'
          'disc-23-Extrovertido': 'o'
          'disc-23-Intrepido': 'o'
          'disc-23-Moderado': 'o'
          'disc-23-Perfeccionista': 'o',
          'disc-TOTAL_FORMS': '24',
          'disc-INITIAL_FORMS': '0'
        }
        """
        from .data.disc import OPTIONS_GROUPS

        return {
            "disc-TOTAL_FORMS": "24",
            "disc-INITIAL_FORMS": "0",
            **{
                f"disc-{index}-{name}": "o"
                for index, names in enumerate(OPTIONS_GROUPS)
                for name in names
            },
        }


class BadRequestEvaluationTestCase(TestCase):
    def setUp(self):
        import logging

        logging.root.setLevel(logging.CRITICAL)

        CreateDiscQuiz()
        self.client = Client()

    def test_bad_freelancer_id(self):
        response = self.client.get(
            f"/quizzes/{Quiz.ID.DISC}/evaluate/BAD_123_ID/"
        )

        self.assertEqual(response.status_code, 404)

    def test_freelancer_does_not_exist(self):
        response = self.client.get(f"/quizzes/{Quiz.ID.DISC}/evaluate/123/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("view_error", response.context)
        self.assertTrue(response.context["view_error"])


class RespondentTestCase(TestCase):
    def test_available_quizzes(self):
        from .models import Respondent

        pairs = Respondent.AvailableQuizzes()
        for quizIdValue, text in pairs:
            quizId = Quiz.ID(quizIdValue)  # valid id int
            self.assertNotIn(quizId.name.lower(), text.lower())
