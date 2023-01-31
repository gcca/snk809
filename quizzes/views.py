# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

import logging
from typing import Any, Dict, Type

from django.forms import Form
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from sinek.infrastructure.persistence.orm.models import Freelancer

from .forms import DiscFormSet
from .models import DiscSelectAnswer, Evaluation, Option, Quiz, Respondent


class EvaluateView(FormView):

    template_name = "quizzes/evaluation.html"

    def get_form_class(self) -> Type[Form]:
        # En esta parte tendríamos que seleccionar el quiz que responde
        # el freelancer. De momento sólo disc hardcoded.
        quizzesMap = {
            Quiz.ID.DISC: DiscFormSet,
        }

        # los url arguments como quiz_id se validan desde urls.py
        # con el url pattern
        quizId = Quiz.ID(int(self.kwargs["quiz_id"]))

        return quizzesMap[quizId]

    def get_success_url(self) -> str:
        # Similar a lo anterior. Acá habrá que decidir a donde regresar
        # dependiendo del tipo de quiz. O tal vez siempre se hará un redirect
        # hacia el dashboard del freelancer
        return "/quizzes/disc-demo/"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Deberíamos manejar esto en form_invalid.
        # TODO Falta decidir cómo manejaremos el form con valores erróneos
        # Según eso, seguiremos manejando esto acá o lo pasaremos a form_invalid
        if not context["form"].is_valid():
            # Esto no es necesario porque form.is_valid() sirve en el template
            context["form_with_error"] = True

        freelancerId = self.kwargs["freelancer_id"]

        self._GetFreelancer(freelancerId, context)
        # Acá no es necesario tener el Quiz(id=DISC)
        # porque eso ya lo está haciendo el formset

        return context

    def form_valid(self, form: DiscFormSet) -> HttpResponse:
        # Acá irá el guardado de las respuestas disc
        quiz = Quiz.objects.get(id=int(self.kwargs["quiz_id"]))
        freelancer = Freelancer.objects.get(id=self.kwargs["freelancer_id"])
        evaluation, _ = Evaluation.objects.update_or_create(
            quiz=quiz, freelancer=freelancer
        )

        # TODO Esto deberíamos moverlo hacia el form
        # NOTE Revisar la documentación del ModelForm
        for subform in form:
            data = subform.cleaned_data

            # TODO Esto no debería ser necesario. Hay que cambiar la lógica para
            # no necesitar validar un form sin data.
            if not data:
                subform.add_error(None, "Incomplete form data")
                return self.form_invalid(form)

            mostOptionText = list(data.keys())[list(data.values()).index("+")]
            leastOptionText = list(data.keys())[list(data.values()).index("-")]

            mostOption = Option.objects.get(
                text=mostOptionText, question_id=subform.question_id
            )
            leastOption = Option.objects.get(
                text=leastOptionText, question_id=subform.question_id
            )

            DiscSelectAnswer.objects.update_or_create(
                question=mostOption.question,
                evaluation=evaluation,
                mostOption=mostOption,
                leastOption=leastOption,
            )

            ################################################################
            # Guardar como se muestra en el diseño:                        #
            # Evaluation relaciona al freelancer con el quiz y los answers #
            ################################################################

        return super().form_valid(form)

    @staticmethod
    def _GetFreelancer(freelancerId: int, context: Dict[str, Any]):
        from sinek.infrastructure.persistence.orm.models import Freelancer

        try:
            freelancer = Freelancer.objects.get(id=freelancerId)
        except Freelancer.DoesNotExist as error:
            logging.error(
                "Error getting freelancer with id=%s (error=%s)",
                freelancerId,
                error,
            )
            context["view_error"] = True
            return

        context["freelancer"] = freelancer

        return freelancer


class EvaluationListView(ListView):
    model = Evaluation


# Esto de momento sólo mostrará DISC
class EvaluationDetailView(DetailView):
    model = Evaluation
    pk_url_kwarg = "evaluation_id"


class QuizzesForView(DetailView):
    model = Respondent
    template_name = "quizzes/quizzes_for.html"
    pk_url_kwarg = "freelancer_id"
