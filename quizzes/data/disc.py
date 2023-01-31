# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from ..models import DiscSelectQuestion, Option, Quiz

OPTIONS_GROUPS = (
    ("Expresivo", "Sumiso", "Enérgico", "Controlado"),
    ("Fuerte de carácter", "Cuidadoso", "Emocional", "Satisfecho"),
    ("Correcto", "Tranquilo", "Pionero", "Influyente"),
    ("Preciso", "Dominante", "Dispuesto", "Atractivo"),
    ("Ecuánime", "Estimulante", "Meticuloso", "Decidido"),
    ("Tímido", "Exigente", "Paciente", "Cautivador"),
    ("Concienzudo", "Buena compañia", "Bondadoso", "Depende de si"),
    ("Agradable", "Con dominio propio", "Juguetón", "Persistente"),
    ("Animoso", "Conversador", "Bonachon", "Conservador"),
    ("Contento", "Impaciente", "Convicente", "Resignado"),
    ("Respetuoso", "Socialmente desenvuelto", "Agresivo", "Apacible"),
    ("Aplomo", "Convencional", "Toma riesgos", "Servicial"),
    (
        "Seguro de sí mismo",
        "Cooperativo",
        "Disputador",
        "Relajado, sin tensiones",
    ),
    ("Inquieto", "Disciplinado", "Inspirador", "Considerado"),
    ("Diplomático", "Valiente", "Compasivo", "Optimista"),
    ("Encantador", "Positivo", "Indulgente", "Riguroso"),
    ("Aventurero", "Entusiasta", "Sigue las reglas", "Leal"),
    ("Humilde", "Oyente atento", "Entretenido", "Con fuerza de voluntad"),
    ("Divertido", "Obediente", "Discreto", "Competitivo"),
    ("Cauteloso", "Amistoso", "Vigoroso", "Persuasivo"),
    ("Reservado", "Franco", "Estricto", "Elocuente"),
    ("Cortés", "Animado", "Decisivo", "Preciso"),
    ("Asertivo", "Sociable", "Estable", "Metódico"),
    ("Extrovertido", "Intrepido", "Moderado", "Perfeccionista"),
)


def CreateQuiz() -> Quiz:
    quiz = Quiz.objects.create(
        id=Quiz.ID.DISC, title="DISC", description="Test de personalidad."
    )

    # Acá no soporta bulk_create por la herencia multitable.
    # TODO usar bulk_create creando los padres secuencialmente. Q>SQ>DSQ
    questions = [
        DiscSelectQuestion.objects.create(
            quiz=quiz, text=f"Pregunta {index + 1}"
        )
        for index in range(len(OPTIONS_GROUPS))
    ]

    Option.objects.bulk_create(
        [
            Option(text=text, question=question)
            for group, question in zip(OPTIONS_GROUPS, questions)
            for text in group
        ]
    )

    return quiz
