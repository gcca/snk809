# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

# Django 4.1.3 on 2022-12-12 18:13

import django.db.models.deletion
from django.db import migrations, models

import onboard.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Applicant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1024)),
                ("email", models.EmailField(max_length=128, unique=True)),
                (
                    "gender",
                    models.IntegerField(choices=[(1, "Male"), (2, "Female")]),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GoogleForm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                ("description", models.TextField(max_length=2048)),
                (
                    "shared_url",
                    models.URLField(
                        max_length=1024,
                        validators=[onboard.models.validate_googleform_url],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Onboard",
            fields=[
                (
                    "applicant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="onboard.applicant",
                    ),
                ),
                ("slug", models.SlugField(max_length=128, unique=True)),
                (
                    "resume",
                    models.FileField(
                        null=True, upload_to=onboard.models.ResumeDirectoryPath
                    ),
                ),
                ("show_disc", models.BooleanField(default=True)),
                ("show_tmms", models.BooleanField(default=True)),
                ("show_agility_learning", models.BooleanField(default=True)),
                ("show_career_anchors", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="AgilityLearningInput",
            fields=[
                (
                    "onboard",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="onboard.onboard",
                    ),
                ),
                ("q1_a", models.BooleanField(default=False)),
                ("q1_b", models.BooleanField(default=False)),
                ("q1_c", models.BooleanField(default=False)),
                ("q2_a", models.BooleanField(default=False)),
                ("q2_b", models.BooleanField(default=False)),
                ("q2_c", models.BooleanField(default=False)),
                ("q3_a", models.BooleanField(default=False)),
                ("q3_b", models.BooleanField(default=False)),
                ("q3_c", models.BooleanField(default=False)),
                ("q4_a", models.BooleanField(default=False)),
                ("q4_b", models.BooleanField(default=False)),
                ("q4_c", models.BooleanField(default=False)),
                ("q5_a", models.BooleanField(default=False)),
                ("q5_b", models.BooleanField(default=False)),
                ("q5_c", models.BooleanField(default=False)),
                ("q6_a", models.BooleanField(default=False)),
                ("q6_b", models.BooleanField(default=False)),
                ("q6_c", models.BooleanField(default=False)),
                ("q7_a", models.BooleanField(default=False)),
                ("q7_b", models.BooleanField(default=False)),
                ("q7_c", models.BooleanField(default=False)),
                ("q8_a", models.BooleanField(default=False)),
                ("q8_b", models.BooleanField(default=False)),
                ("q8_c", models.BooleanField(default=False)),
                ("q9_a", models.BooleanField(default=False)),
                ("q9_b", models.BooleanField(default=False)),
                ("q9_c", models.BooleanField(default=False)),
                ("q10_a", models.BooleanField(default=False)),
                ("q10_b", models.BooleanField(default=False)),
                ("q10_c", models.BooleanField(default=False)),
                ("q11_a", models.BooleanField(default=False)),
                ("q11_b", models.BooleanField(default=False)),
                ("q11_c", models.BooleanField(default=False)),
                ("q12_a", models.BooleanField(default=False)),
                ("q12_b", models.BooleanField(default=False)),
                ("q12_c", models.BooleanField(default=False)),
                ("q13_a", models.BooleanField(default=False)),
                ("q13_b", models.BooleanField(default=False)),
                ("q13_c", models.BooleanField(default=False)),
                ("q14_a", models.BooleanField(default=False)),
                ("q14_b", models.BooleanField(default=False)),
                ("q14_c", models.BooleanField(default=False)),
                ("q15_a", models.BooleanField(default=False)),
                ("q15_b", models.BooleanField(default=False)),
                ("q15_c", models.BooleanField(default=False)),
                ("q16_a", models.BooleanField(default=False)),
                ("q16_b", models.BooleanField(default=False)),
                ("q16_c", models.BooleanField(default=False)),
                ("q17_a", models.BooleanField(default=False)),
                ("q17_b", models.BooleanField(default=False)),
                ("q17_c", models.BooleanField(default=False)),
                ("q18_a", models.BooleanField(default=False)),
                ("q18_b", models.BooleanField(default=False)),
                ("q18_c", models.BooleanField(default=False)),
                ("q19_a", models.BooleanField(default=False)),
                ("q19_b", models.BooleanField(default=False)),
                ("q19_c", models.BooleanField(default=False)),
                ("q20_a", models.BooleanField(default=False)),
                ("q20_b", models.BooleanField(default=False)),
                ("q20_c", models.BooleanField(default=False)),
                ("q21_a", models.BooleanField(default=False)),
                ("q21_b", models.BooleanField(default=False)),
                ("q21_c", models.BooleanField(default=False)),
                ("q22_a", models.BooleanField(default=False)),
                ("q22_b", models.BooleanField(default=False)),
                ("q22_c", models.BooleanField(default=False)),
                ("q23_a", models.BooleanField(default=False)),
                ("q23_b", models.BooleanField(default=False)),
                ("q23_c", models.BooleanField(default=False)),
                ("q24_a", models.BooleanField(default=False)),
                ("q24_b", models.BooleanField(default=False)),
                ("q24_c", models.BooleanField(default=False)),
                ("q25_a", models.BooleanField(default=False)),
                ("q25_b", models.BooleanField(default=False)),
                ("q25_c", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="CareerAnchorsInput",
            fields=[
                (
                    "onboard",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="onboard.onboard",
                    ),
                ),
                (
                    "q1",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q2",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q3",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q4",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q5",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q6",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q7",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q8",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q9",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q10",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q11",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q12",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q13",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q14",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q15",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q16",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q17",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q18",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q19",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q20",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q21",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q22",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q23",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q24",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q25",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q26",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q27",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q28",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q29",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q30",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q31",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q32",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q33",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q34",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q35",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q36",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q37",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q38",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q39",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q40",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "favorite1",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                            (11, 11),
                            (12, 12),
                            (13, 13),
                            (14, 14),
                            (15, 15),
                            (16, 16),
                            (17, 17),
                            (18, 18),
                            (19, 19),
                            (20, 20),
                            (21, 21),
                            (22, 22),
                            (23, 23),
                            (24, 24),
                            (25, 25),
                            (26, 26),
                            (27, 27),
                            (28, 28),
                            (29, 29),
                            (30, 30),
                            (31, 31),
                            (32, 32),
                            (33, 33),
                            (34, 34),
                            (35, 35),
                            (36, 36),
                            (37, 37),
                            (38, 38),
                            (39, 39),
                            (40, 40),
                        ],
                        default=None,
                    ),
                ),
                (
                    "favorite2",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                            (11, 11),
                            (12, 12),
                            (13, 13),
                            (14, 14),
                            (15, 15),
                            (16, 16),
                            (17, 17),
                            (18, 18),
                            (19, 19),
                            (20, 20),
                            (21, 21),
                            (22, 22),
                            (23, 23),
                            (24, 24),
                            (25, 25),
                            (26, 26),
                            (27, 27),
                            (28, 28),
                            (29, 29),
                            (30, 30),
                            (31, 31),
                            (32, 32),
                            (33, 33),
                            (34, 34),
                            (35, 35),
                            (36, 36),
                            (37, 37),
                            (38, 38),
                            (39, 39),
                            (40, 40),
                        ],
                        default=None,
                    ),
                ),
                (
                    "favorite3",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                            (11, 11),
                            (12, 12),
                            (13, 13),
                            (14, 14),
                            (15, 15),
                            (16, 16),
                            (17, 17),
                            (18, 18),
                            (19, 19),
                            (20, 20),
                            (21, 21),
                            (22, 22),
                            (23, 23),
                            (24, 24),
                            (25, 25),
                            (26, 26),
                            (27, 27),
                            (28, 28),
                            (29, 29),
                            (30, 30),
                            (31, 31),
                            (32, 32),
                            (33, 33),
                            (34, 34),
                            (35, 35),
                            (36, 36),
                            (37, 37),
                            (38, 38),
                            (39, 39),
                            (40, 40),
                        ],
                        default=None,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DiscInput",
            fields=[
                (
                    "onboard",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="onboard.onboard",
                    ),
                ),
                (
                    "q1_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Expresivo"),
                            (2, "Sumiso"),
                            (3, "Enérgico"),
                            (4, "Controlado"),
                        ]
                    ),
                ),
                (
                    "q1_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Expresivo"),
                            (2, "Sumiso"),
                            (3, "Enérgico"),
                            (4, "Controlado"),
                        ]
                    ),
                ),
                (
                    "q2_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Fuerte De Carácter"),
                            (2, "Cuidadoso"),
                            (3, "Emocional"),
                            (4, "Satisfecho"),
                        ]
                    ),
                ),
                (
                    "q2_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Fuerte De Carácter"),
                            (2, "Cuidadoso"),
                            (3, "Emocional"),
                            (4, "Satisfecho"),
                        ]
                    ),
                ),
                (
                    "q3_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Correcto"),
                            (2, "Pionero"),
                            (3, "Tranquilo"),
                            (4, "Influyente"),
                        ]
                    ),
                ),
                (
                    "q3_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Correcto"),
                            (2, "Pionero"),
                            (3, "Tranquilo"),
                            (4, "Influyente"),
                        ]
                    ),
                ),
                (
                    "q4_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Preciso"),
                            (2, "Dominante"),
                            (3, "Dispuesto"),
                            (4, "Atractivo"),
                        ]
                    ),
                ),
                (
                    "q4_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Preciso"),
                            (2, "Dominante"),
                            (3, "Dispuesto"),
                            (4, "Atractivo"),
                        ]
                    ),
                ),
                (
                    "q5_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Ecuánime"),
                            (2, "Estimulante"),
                            (3, "Meticuloso"),
                            (4, "Decidido"),
                        ]
                    ),
                ),
                (
                    "q5_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Ecuánime"),
                            (2, "Estimulante"),
                            (3, "Meticuloso"),
                            (4, "Decidido"),
                        ]
                    ),
                ),
                (
                    "q6_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Tímido"),
                            (2, "Exigente"),
                            (3, "Paciente"),
                            (4, "Cautivador"),
                        ]
                    ),
                ),
                (
                    "q6_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Tímido"),
                            (2, "Exigente"),
                            (3, "Paciente"),
                            (4, "Cautivador"),
                        ]
                    ),
                ),
                (
                    "q7_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Concienzudo"),
                            (2, "Buena Compañia"),
                            (3, "Bondadoso"),
                            (4, "Depende De Si"),
                        ]
                    ),
                ),
                (
                    "q7_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Concienzudo"),
                            (2, "Buena Compañia"),
                            (3, "Bondadoso"),
                            (4, "Depende De Si"),
                        ]
                    ),
                ),
                (
                    "q8_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Agradable"),
                            (2, "Con Dominio Propio"),
                            (3, "Juguetón"),
                            (4, "Persistente"),
                        ]
                    ),
                ),
                (
                    "q8_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Agradable"),
                            (2, "Con Dominio Propio"),
                            (3, "Juguetón"),
                            (4, "Persistente"),
                        ]
                    ),
                ),
                (
                    "q9_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Animoso"),
                            (2, "Conversador"),
                            (3, "Bonachon"),
                            (4, "Conservador"),
                        ]
                    ),
                ),
                (
                    "q9_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Animoso"),
                            (2, "Conversador"),
                            (3, "Bonachon"),
                            (4, "Conservador"),
                        ]
                    ),
                ),
                (
                    "q10_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Contento"),
                            (2, "Impaciente"),
                            (3, "Convicente"),
                            (4, "Resignado"),
                        ]
                    ),
                ),
                (
                    "q10_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Contento"),
                            (2, "Impaciente"),
                            (3, "Convicente"),
                            (4, "Resignado"),
                        ]
                    ),
                ),
                (
                    "q11_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Respetuoso"),
                            (2, "Socialmente Desenvuelto"),
                            (3, "Agresivo"),
                            (4, "Apacible"),
                        ]
                    ),
                ),
                (
                    "q11_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Respetuoso"),
                            (2, "Socialmente Desenvuelto"),
                            (3, "Agresivo"),
                            (4, "Apacible"),
                        ]
                    ),
                ),
                (
                    "q12_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Aplomo"),
                            (2, "Convencional"),
                            (3, "Toma Riesgos"),
                            (4, "Servicial"),
                        ]
                    ),
                ),
                (
                    "q12_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Aplomo"),
                            (2, "Convencional"),
                            (3, "Toma Riesgos"),
                            (4, "Servicial"),
                        ]
                    ),
                ),
                (
                    "q13_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Seguro De Sí Mismo"),
                            (2, "Cooperativo"),
                            (3, "Disputador"),
                            (4, "Relajado Sin Tensiones"),
                        ]
                    ),
                ),
                (
                    "q13_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Seguro De Sí Mismo"),
                            (2, "Cooperativo"),
                            (3, "Disputador"),
                            (4, "Relajado Sin Tensiones"),
                        ]
                    ),
                ),
                (
                    "q14_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Inquieto"),
                            (2, "Disciplinado"),
                            (3, "Inspirador"),
                            (4, "Considerado"),
                        ]
                    ),
                ),
                (
                    "q14_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Inquieto"),
                            (2, "Disciplinado"),
                            (3, "Inspirador"),
                            (4, "Considerado"),
                        ]
                    ),
                ),
                (
                    "q15_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Diplomático"),
                            (2, "Valiente"),
                            (3, "Compasivo"),
                            (4, "Optimista"),
                        ]
                    ),
                ),
                (
                    "q15_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Diplomático"),
                            (2, "Valiente"),
                            (3, "Compasivo"),
                            (4, "Optimista"),
                        ]
                    ),
                ),
                (
                    "q16_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Encantador"),
                            (2, "Positivo"),
                            (3, "Indulgente"),
                            (4, "Riguroso"),
                        ]
                    ),
                ),
                (
                    "q16_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Encantador"),
                            (2, "Positivo"),
                            (3, "Indulgente"),
                            (4, "Riguroso"),
                        ]
                    ),
                ),
                (
                    "q17_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Aventurero"),
                            (2, "Entusiasta"),
                            (3, "Sigue Las Reglas"),
                            (4, "Leal"),
                        ]
                    ),
                ),
                (
                    "q17_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Aventurero"),
                            (2, "Entusiasta"),
                            (3, "Sigue Las Reglas"),
                            (4, "Leal"),
                        ]
                    ),
                ),
                (
                    "q18_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Humilde"),
                            (2, "Oyente Atento"),
                            (3, "Entretenido"),
                            (4, "Con Fuerza De Voluntad"),
                        ]
                    ),
                ),
                (
                    "q18_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Humilde"),
                            (2, "Oyente Atento"),
                            (3, "Entretenido"),
                            (4, "Con Fuerza De Voluntad"),
                        ]
                    ),
                ),
                (
                    "q19_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Divertido"),
                            (2, "Obediente"),
                            (3, "Discreto"),
                            (4, "Competitivo"),
                        ]
                    ),
                ),
                (
                    "q19_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Divertido"),
                            (2, "Obediente"),
                            (3, "Discreto"),
                            (4, "Competitivo"),
                        ]
                    ),
                ),
                (
                    "q20_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Cauteloso"),
                            (2, "Amistoso"),
                            (3, "Vigoroso"),
                            (4, "Persuasivo"),
                        ]
                    ),
                ),
                (
                    "q20_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Cauteloso"),
                            (2, "Amistoso"),
                            (3, "Vigoroso"),
                            (4, "Persuasivo"),
                        ]
                    ),
                ),
                (
                    "q21_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Reservado"),
                            (2, "Franco"),
                            (3, "Estricto"),
                            (4, "Elocuente"),
                        ]
                    ),
                ),
                (
                    "q21_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Reservado"),
                            (2, "Franco"),
                            (3, "Estricto"),
                            (4, "Elocuente"),
                        ]
                    ),
                ),
                (
                    "q22_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Cortés"),
                            (2, "Animado"),
                            (3, "Decisivo"),
                            (4, "Preciso"),
                        ]
                    ),
                ),
                (
                    "q22_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Cortés"),
                            (2, "Animado"),
                            (3, "Decisivo"),
                            (4, "Preciso"),
                        ]
                    ),
                ),
                (
                    "q23_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Asertivo"),
                            (2, "Sociable"),
                            (3, "Estable"),
                            (4, "Metódico"),
                        ]
                    ),
                ),
                (
                    "q23_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Asertivo"),
                            (2, "Sociable"),
                            (3, "Estable"),
                            (4, "Metódico"),
                        ]
                    ),
                ),
                (
                    "q24_minus",
                    models.IntegerField(
                        choices=[
                            (1, "Extrovertido"),
                            (2, "Intrepido"),
                            (3, "Moderado"),
                            (4, "Perfeccionista"),
                        ]
                    ),
                ),
                (
                    "q24_plus",
                    models.IntegerField(
                        choices=[
                            (1, "Extrovertido"),
                            (2, "Intrepido"),
                            (3, "Moderado"),
                            (4, "Perfeccionista"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TmmsInput",
            fields=[
                (
                    "onboard",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="onboard.onboard",
                    ),
                ),
                (
                    "q1",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q2",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q3",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q4",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q5",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q6",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q7",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q8",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q9",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q10",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q11",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q12",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q13",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q14",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q15",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q16",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q17",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q18",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q19",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q20",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q21",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q22",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q23",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
                (
                    "q24",
                    models.IntegerField(
                        choices=[(1, ""), (2, ""), (3, ""), (4, ""), (5, "")]
                    ),
                ),
            ],
        ),
    ]
