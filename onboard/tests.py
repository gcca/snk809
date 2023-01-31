# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

import os
from typing import Optional
from unittest.mock import MagicMock

from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.test import Client, TestCase

from . import forms, models, views

User = get_user_model()


class NeodashDangerGroupTestCase(TestCase):
    def test_forbidden(self):
        client = Client()
        CreateUserAndLogin(client, "dummy")
        response = client.get(urls.reverse("onboard:dashboard"))
        self.assertEqual(response.status_code, 403)


class RootDashboardTestCase(TestCase):
    fixtures = ["initial-data"]

    def setUp(self):
        self.client = Client()
        CreateValidUserAndLogin(self.client, "dummy")

    def test_neodash_nav_mark(self):
        response = self.client.get(urls.reverse("onboard:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].username, "dummy")


# -----------------------------------------------------------------------------
# applicant


class ApplicantTestCase(TestCase):
    fixtures = ["initial-data", "onboard-test"]

    def setUp(self):
        CreateValidUserAndLogin(self.client, "dummy")

    def test_create(self):
        response = self.client.post(
            urls.reverse("onboard:applicant:create"),
            data={
                "name": "foo",
                "email": "foo@bar.com",
                "gender": models.Applicant.Gender.MALE,
            },
        )

        self.assertEqual(response.status_code, 302)

        applicant = models.Applicant.objects.get(email="foo@bar.com")

        self.assertEqual(applicant.name, "foo")
        self.assertGreater(len(applicant.onboard.slug), 0)

    def test_detail(self):
        applicant_id = 1  # see fixtures

        response = self.client.get(
            urls.reverse(
                "onboard:applicant:detail",
                kwargs={"applicant_id": applicant_id},
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("applicant", response.context)

        applicant = response.context["applicant"]

        self.assertEqual(applicant.name, "Dionisio Aguado")
        self.assertEqual(applicant.email, "dionisio@aguado.com")
        self.assertEqual(applicant.gender, models.Applicant.Gender.MALE)

    def test_update_process_information(self):
        applicant_id = 1
        applicant = models.Applicant.objects.get(id=applicant_id)

        response = self.client.post(
            urls.reverse(
                "onboard:applicant:onboard:update",
                kwargs={
                    "applicant_id": applicant.id,
                },
            ),
            data={"process_name": "test", "process_link": "https://te.st"},
        )

        self.assertEquals(response.url, "/neodash/onboard/applicant/1/detail/")

    def test_update_resume(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        resume = SimpleUploadedFile(
            "dummy.file", b"dummy", content_type="app/dummy"
        )

        applicant_id = 1

        response = self.client.post(
            urls.reverse(
                "onboard:applicant:onboard:cv-upload",
                kwargs={"applicant_id": applicant_id},
            ),
            data={"resume": resume},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEquals(
            response.url,
            urls.reverse(
                "onboard:applicant:detail",
                kwargs={"applicant_id": applicant_id},
            ),
        )

        onboard = models.Onboard.objects.get(applicant_id=applicant_id)

        self.assertEqual(onboard.resume.name, "resumes/1/dummy.file")
        self.assertEqual(onboard.resume.read(), b"dummy")

        # test existing file
        resume.seek(os.SEEK_SET)
        response = self.client.post(
            urls.reverse(
                "onboard:applicant:onboard:cv-upload",
                kwargs={"applicant_id": applicant_id},
            ),
            data={"resume": resume},
        )

        import shutil

        shutil.rmtree("uploads/resumes/1/")


class ApplicantResumeTestCase(TestCase):

    fixtures = ["initial-data", "applicant-resume-test"]

    def test_download(self):
        client = Client()
        CreateValidUserAndLogin(client, "dummy")

        os.makedirs("uploads/resumes/1/")
        with open("uploads/resumes/1/dummy.file", "wt") as file:
            file.write("dummy")

        applicant_id = 1  # see fixtures

        response = client.get(
            urls.reverse(
                "onboard:applicant:resume",
                kwargs={"applicant_id": applicant_id},
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)
        self.assertEqual(response.filename, "dummy.file")
        self.assertEqual(response.getvalue(), b"dummy")

        import shutil

        shutil.rmtree("uploads/resumes/1/")


# -----------------------------------------------------------------------------
# onboard


class OnboardTestCase(TestCase):
    fixtures = ["initial-data", "onboard-test"]

    def setUp(self):
        self.client = Client()
        CreateValidUserAndLogin(self.client, "dummy")
        self.slug = "ce220ef060bb11edbbd1cf17990de5ba"  # see fixture

    def test_dashboard(self):
        response = self.client.get(
            urls.reverse(
                "onboard:onboard:dashboard", kwargs={"slug": self.slug}
            )
        )

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertIn("slug", context)
        self.assertEquals(context["slug"], self.slug)

        self.assertIn("resume_form", context)
        self.assertIsInstance(context["resume_form"], forms.OnboardResumeForm)

    def test_update_resume(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        resume = SimpleUploadedFile(
            "dummy.file", b"dummy", content_type="app/dummy"
        )

        response = self.client.post(
            urls.reverse("onboard:onboard:resume", kwargs={"slug": self.slug}),
            data={"resume": resume},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEquals(
            response.url,
            urls.reverse("onboard:onboard:saved", kwargs={"slug": self.slug}),
        )

        onboard = models.Onboard.objects.get(slug=self.slug)

        self.assertEqual(onboard.resume.name, "resumes/1/dummy.file")
        self.assertEqual(onboard.resume.read(), b"dummy")

        # test existing file
        resume.seek(os.SEEK_SET)
        response = self.client.post(
            urls.reverse("onboard:onboard:resume", kwargs={"slug": self.slug}),
            data={"resume": resume},
        )

        import shutil

        shutil.rmtree("uploads/resumes/1/")

    def test_toggle_visibility(self):
        onboard = models.Onboard.objects.get(slug=self.slug)

        assessments = ["disc", "tmms", "complex_instructions", "career_anchors"]
        for assessment in assessments:
            self.client.post(
                urls.reverse(
                    "onboard:onboard:toggle-visibility",
                    kwargs={"slug": self.slug, "assessment_name": assessment},
                ),
            )

        onboard.refresh_from_db()

        self.assertEqual(onboard.show_disc, False)
        self.assertEqual(onboard.show_tmms, False)
        self.assertEqual(onboard.show_career_anchors, False)
        self.assertEqual(onboard.show_complex_instructions, False)

    def test_toggle_visibility_invalid(self):
        invalid_name = "invalid"

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:toggle-visibility",
                kwargs={"slug": self.slug, "assessment_name": invalid_name},
            )
        )

        self.assertEqual(response.status_code, 400)

    def test_toggle_googleform_visibility_off(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        googleform_model = models.GoogleForm.objects.create(
            title="dummy",
            description="dummy",
            shared_url="https://dummy/viewform",
            view_link="https://dummy/view",
        )

        onboard.google_forms.add(googleform_model)

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:googleform-toggle-visibility",
                kwargs={
                    "slug": self.slug,
                    "googleform_id": googleform_model.id,
                },
            ),
        )

        onboard.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(onboard.google_forms.all()), 0)

    def test_toggle_googleform_visibility_on(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        googleform_model = models.GoogleForm.objects.create(
            title="dummy",
            description="dummy",
            shared_url="https://dummy/viewform",
            view_link="https://dummy/view",
        )

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:googleform-toggle-visibility",
                kwargs={
                    "slug": self.slug,
                    "googleform_id": googleform_model.id,
                },
            ),
        )

        onboard.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertIn(googleform_model, onboard.google_forms.all())

    def test_assessment_get(self):
        onboard = models.Onboard.objects.get(slug=self.slug)

        assessments = ["disc", "tmms", "complex", "career-anchors"]
        for assessment in assessments:
            response = self.client.get(
                urls.reverse(
                    f"onboard:onboard:assessment:{assessment}",
                    kwargs={"slug": self.slug},
                ),
            )
            self.assertEqual(response.status_code, 200)

        onboard.show_tmms = False
        onboard.save()

        response = self.client.get(
            urls.reverse(
                "onboard:onboard:assessment:tmms",
                kwargs={"slug": self.slug},
            ),
        )
        self.assertEqual(response.status_code, 403)


class OnboardBadSlugTestCase(TestCase):
    fixtures = ["initial-data"]

    def test_dashboard(self):
        self.client = Client()
        CreateValidUserAndLogin(self.client, "dummy")

        self.slug = "a" * 300  # greater then max length slug

        response = self.client.get(
            urls.reverse(
                "onboard:onboard:dashboard", kwargs={"slug": self.slug}
            )
        )

        self.assertEqual(response.status_code, 403)


class OnboardAssessmentDiscTestCase(TestCase):
    fixtures = ["initial-data", "onboard-test"]

    def setUp(self):
        self.client = Client()
        CreateValidUserAndLogin(self.client, "dummy")
        self.slug = "ce220ef060bb11edbbd1cf17990de5ba"  # see fixture

    def test_get_initial(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        models.DiscInput.objects.create(
            onboard=onboard,
            q1_minus=1,
            q1_plus=2,
            q2_minus=1,
            q2_plus=2,
            q3_minus=1,
            q3_plus=2,
            q4_minus=1,
            q4_plus=2,
            q5_minus=1,
            q5_plus=2,
            q6_minus=1,
            q6_plus=2,
            q7_minus=1,
            q7_plus=2,
            q8_minus=1,
            q8_plus=2,
            q9_minus=1,
            q9_plus=2,
            q10_minus=1,
            q10_plus=2,
            q11_minus=1,
            q11_plus=2,
            q12_minus=1,
            q12_plus=2,
            q13_minus=1,
            q13_plus=2,
            q14_minus=1,
            q14_plus=2,
            q15_minus=1,
            q15_plus=2,
            q16_minus=1,
            q16_plus=2,
            q17_minus=1,
            q17_plus=2,
            q18_minus=1,
            q18_plus=2,
            q19_minus=1,
            q19_plus=2,
            q20_minus=1,
            q20_plus=2,
            q21_minus=1,
            q21_plus=2,
            q22_minus=1,
            q22_plus=2,
            q23_minus=1,
            q23_plus=2,
            q24_minus=1,
            q24_plus=2,
        )
        response = self.client.get(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            ),
        )
        initial = response.context_data["form"].initial
        self.assertEqual(initial["q1"].minus, 1)
        self.assertEqual(initial["q1"].plus, 2)
        self.assertEqual(initial["q2"].minus, 1)
        self.assertEqual(initial["q2"].plus, 2)
        self.assertEqual(initial["q3"].minus, 1)
        self.assertEqual(initial["q3"].plus, 2)
        self.assertEqual(initial["q4"].minus, 1)
        self.assertEqual(initial["q4"].plus, 2)
        self.assertEqual(initial["q5"].minus, 1)
        self.assertEqual(initial["q5"].plus, 2)
        self.assertEqual(initial["q6"].minus, 1)
        self.assertEqual(initial["q6"].plus, 2)
        self.assertEqual(initial["q7"].minus, 1)
        self.assertEqual(initial["q7"].plus, 2)
        self.assertEqual(initial["q8"].minus, 1)
        self.assertEqual(initial["q8"].plus, 2)
        self.assertEqual(initial["q9"].minus, 1)
        self.assertEqual(initial["q9"].plus, 2)
        self.assertEqual(initial["q10"].minus, 1)
        self.assertEqual(initial["q10"].plus, 2)
        self.assertEqual(initial["q11"].minus, 1)
        self.assertEqual(initial["q11"].plus, 2)
        self.assertEqual(initial["q12"].minus, 1)
        self.assertEqual(initial["q12"].plus, 2)
        self.assertEqual(initial["q13"].minus, 1)
        self.assertEqual(initial["q13"].plus, 2)
        self.assertEqual(initial["q14"].minus, 1)
        self.assertEqual(initial["q14"].plus, 2)
        self.assertEqual(initial["q15"].minus, 1)
        self.assertEqual(initial["q15"].plus, 2)
        self.assertEqual(initial["q16"].minus, 1)
        self.assertEqual(initial["q16"].plus, 2)
        self.assertEqual(initial["q17"].minus, 1)
        self.assertEqual(initial["q17"].plus, 2)
        self.assertEqual(initial["q18"].minus, 1)
        self.assertEqual(initial["q18"].plus, 2)
        self.assertEqual(initial["q19"].minus, 1)
        self.assertEqual(initial["q19"].plus, 2)
        self.assertEqual(initial["q20"].minus, 1)
        self.assertEqual(initial["q20"].plus, 2)
        self.assertEqual(initial["q21"].minus, 1)
        self.assertEqual(initial["q21"].plus, 2)
        self.assertEqual(initial["q22"].minus, 1)
        self.assertEqual(initial["q22"].plus, 2)
        self.assertEqual(initial["q23"].minus, 1)
        self.assertEqual(initial["q23"].plus, 2)
        self.assertEqual(initial["q24"].minus, 1)
        self.assertEqual(initial["q24"].plus, 2)

    def test_send_form(self):
        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            ),
            data=self.DiscData(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Location", response.headers)
        self.assertEqual(
            response.headers["Location"],
            urls.reverse("onboard:onboard:saved", kwargs={"slug": self.slug}),
        )

        onboard = models.Onboard.objects.get(slug=self.slug)
        discInput = onboard.discinput

        self.assertEqual(discInput.q1_minus, 1)
        self.assertEqual(discInput.q1_plus, 2)
        self.assertEqual(discInput.q2_minus, 1)
        self.assertEqual(discInput.q2_plus, 2)
        self.assertEqual(discInput.q3_minus, 1)
        self.assertEqual(discInput.q3_plus, 2)
        self.assertEqual(discInput.q4_minus, 1)
        self.assertEqual(discInput.q4_plus, 2)
        self.assertEqual(discInput.q5_minus, 1)
        self.assertEqual(discInput.q5_plus, 2)
        self.assertEqual(discInput.q6_minus, 1)
        self.assertEqual(discInput.q6_plus, 2)
        self.assertEqual(discInput.q7_minus, 1)
        self.assertEqual(discInput.q7_plus, 2)
        self.assertEqual(discInput.q8_minus, 1)
        self.assertEqual(discInput.q8_plus, 2)
        self.assertEqual(discInput.q9_minus, 1)
        self.assertEqual(discInput.q9_plus, 2)
        self.assertEqual(discInput.q10_minus, 1)
        self.assertEqual(discInput.q10_plus, 2)
        self.assertEqual(discInput.q11_minus, 1)
        self.assertEqual(discInput.q11_plus, 2)
        self.assertEqual(discInput.q12_minus, 1)
        self.assertEqual(discInput.q12_plus, 2)
        self.assertEqual(discInput.q13_minus, 1)
        self.assertEqual(discInput.q13_plus, 2)
        self.assertEqual(discInput.q14_minus, 1)
        self.assertEqual(discInput.q14_plus, 2)
        self.assertEqual(discInput.q15_minus, 1)
        self.assertEqual(discInput.q15_plus, 2)
        self.assertEqual(discInput.q16_minus, 1)
        self.assertEqual(discInput.q16_plus, 2)
        self.assertEqual(discInput.q17_minus, 1)
        self.assertEqual(discInput.q17_plus, 2)
        self.assertEqual(discInput.q18_minus, 1)
        self.assertEqual(discInput.q18_plus, 2)
        self.assertEqual(discInput.q19_minus, 1)
        self.assertEqual(discInput.q19_plus, 2)
        self.assertEqual(discInput.q20_minus, 1)
        self.assertEqual(discInput.q20_plus, 2)
        self.assertEqual(discInput.q21_minus, 1)
        self.assertEqual(discInput.q21_plus, 2)
        self.assertEqual(discInput.q22_minus, 1)
        self.assertEqual(discInput.q22_plus, 2)
        self.assertEqual(discInput.q23_minus, 1)
        self.assertEqual(discInput.q23_plus, 2)
        self.assertEqual(discInput.q24_minus, 1)
        self.assertEqual(discInput.q24_plus, 2)

    def test_send_form_without_q1(self):
        data = self.DiscData()
        del data["q1-minus"]
        del data["q1-plus"]

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            ),
            data=data,
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn("q1", form.errors)
        self.assertEqual(form.errors["q1"], ["Este campo es obligatorio."])

    def test_send_form_without_q1_minus(self):
        data = self.DiscData()
        del data["q1-minus"]

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            ),
            data=data,
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn("q1", form.errors)
        self.assertEqual(
            form.errors["q1"], ["Selecciona una opción para la columna menos."]
        )

    def test_send_form_without_q1_plus(self):
        data = self.DiscData()
        del data["q1-plus"]

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            ),
            data=data,
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn("q1", form.errors)
        self.assertEqual(
            form.errors["q1"], ["Selecciona una opción para la columna más."]
        )

    def test_send_form_q1_with_minus_equal_plus(self):
        data = self.DiscData()
        data["q1-plus"] = "1"

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            ),
            data=data,
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn("q1", form.errors)
        self.assertEqual(
            form.errors["q1"],
            [
                "No puede seleccionar ambas opciones para una sola"
                " característica."
            ],
        )

    def test_already_saved(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        self.CreateDiscInput(onboard)

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            ),
            data=self.DiscData(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Location", response.headers)
        self.assertEqual(
            response.headers["Location"],
            urls.reverse(
                "onboard:onboard:already-saved", kwargs={"slug": self.slug}
            ),
        )

    def test_show_saved(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        self.CreateDiscInput(onboard)

        response = self.client.get(
            urls.reverse(
                "onboard:onboard:assessment:disc", kwargs={"slug": self.slug}
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)

        form = response.context["form"]
        for index in range(1, 25):
            self.assertEqual(form[f"q{index}"].value(), (1, 2))

    def test_get_personality(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        self.CreateDiscInput(onboard)
        disc_input = onboard.discinput

        compounds = disc_input.results.compounds

        self.assertEqual(compounds.d, 3)
        self.assertEqual(compounds.i, 1)
        self.assertEqual(compounds.s, 0)
        self.assertEqual(compounds.c, -4)
        baremos = disc_input.baremos

        self.assertEqual(baremos.d, 84)
        self.assertEqual(baremos.i, 60)
        self.assertEqual(baremos.s, 40)
        self.assertEqual(baremos.c, 30)

        personality = disc_input.personality
        self.assertEqual(personality.name, "Emprendedor")

    @staticmethod
    def DiscData():
        return {
            "q1-minus": "1",
            "q1-plus": "2",
            "q2-minus": "1",
            "q2-plus": "2",
            "q3-minus": "1",
            "q3-plus": "2",
            "q4-minus": "1",
            "q4-plus": "2",
            "q5-minus": "1",
            "q5-plus": "2",
            "q6-minus": "1",
            "q6-plus": "2",
            "q7-minus": "1",
            "q7-plus": "2",
            "q8-minus": "1",
            "q8-plus": "2",
            "q9-minus": "1",
            "q9-plus": "2",
            "q10-minus": "1",
            "q10-plus": "2",
            "q11-minus": "1",
            "q11-plus": "2",
            "q12-minus": "1",
            "q12-plus": "2",
            "q13-minus": "1",
            "q13-plus": "2",
            "q14-minus": "1",
            "q14-plus": "2",
            "q15-minus": "1",
            "q15-plus": "2",
            "q16-minus": "1",
            "q16-plus": "2",
            "q17-minus": "1",
            "q17-plus": "2",
            "q18-minus": "1",
            "q18-plus": "2",
            "q19-minus": "1",
            "q19-plus": "2",
            "q20-minus": "1",
            "q20-plus": "2",
            "q21-minus": "1",
            "q21-plus": "2",
            "q22-minus": "1",
            "q22-plus": "2",
            "q23-minus": "1",
            "q23-plus": "2",
            "q24-minus": "1",
            "q24-plus": "2",
        }

    @staticmethod
    def CreateDiscInput(onboard: models.Onboard):
        models.DiscInput.objects.create(
            onboard=onboard,
            q1_minus=1,
            q1_plus=2,
            q2_minus=1,
            q2_plus=2,
            q3_minus=1,
            q3_plus=2,
            q4_minus=1,
            q4_plus=2,
            q5_minus=1,
            q5_plus=2,
            q6_minus=1,
            q6_plus=2,
            q7_minus=1,
            q7_plus=2,
            q8_minus=1,
            q8_plus=2,
            q9_minus=1,
            q9_plus=2,
            q10_minus=1,
            q10_plus=2,
            q11_minus=1,
            q11_plus=2,
            q12_minus=1,
            q12_plus=2,
            q13_minus=1,
            q13_plus=2,
            q14_minus=1,
            q14_plus=2,
            q15_minus=1,
            q15_plus=2,
            q16_minus=1,
            q16_plus=2,
            q17_minus=1,
            q17_plus=2,
            q18_minus=1,
            q18_plus=2,
            q19_minus=1,
            q19_plus=2,
            q20_minus=1,
            q20_plus=2,
            q21_minus=1,
            q21_plus=2,
            q22_minus=1,
            q22_plus=2,
            q23_minus=1,
            q23_plus=2,
            q24_minus=1,
            q24_plus=2,
        )


class OnboardAssessmentComplexInstructionsTestCase(TestCase):
    fixtures = ["initial-data", "onboard-test"]

    def setUp(self):
        self.client = Client()
        CreateValidUserAndLogin(self.client, "dummy")
        self.slug = "ce220ef060bb11edbbd1cf17990de5ba"  # see fixture

    def test_get_initial(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        models.ComplexInstructionsInput.objects.create(
            onboard=onboard,
            q1_a=True,
            q1_b=False,
            q1_c=True,
            q2_a=True,
            q2_b=False,
            q2_c=True,
            q3_a=True,
            q3_b=False,
            q3_c=True,
            q4_a=True,
            q4_b=False,
            q4_c=True,
            q5_a=True,
            q5_b=False,
            q5_c=True,
            q6_a=True,
            q6_b=False,
            q6_c=True,
            q7_a=True,
            q7_b=False,
            q7_c=True,
            q8_a=True,
            q8_b=False,
            q8_c=True,
            q9_a=True,
            q9_b=False,
            q9_c=True,
            q10_a=True,
            q10_b=False,
            q10_c=True,
            q11_a=True,
            q11_b=False,
            q11_c=True,
            q12_a=True,
            q12_b=False,
            q12_c=True,
            q13_a=True,
            q13_b=False,
            q13_c=True,
            q14_a=True,
            q14_b=False,
            q14_c=True,
            q15_a=True,
            q15_b=False,
            q15_c=True,
            q16_a=True,
            q16_b=False,
            q16_c=True,
            q17_a=True,
            q17_b=False,
            q17_c=True,
            q18_a=True,
            q18_b=False,
            q18_c=True,
            q19_a=True,
            q19_b=False,
            q19_c=True,
            q20_a=True,
            q20_b=False,
            q20_c=True,
            q21_a=True,
            q21_b=False,
            q21_c=True,
            q22_a=True,
            q22_b=False,
            q22_c=True,
            q23_a=True,
            q23_b=False,
            q23_c=True,
            q24_a=True,
            q24_b=False,
            q24_c=True,
            q25_a=True,
            q25_b=False,
            q25_c=True,
        )
        response = self.client.get(
            urls.reverse(
                "onboard:onboard:assessment:complex", kwargs={"slug": self.slug}
            ),
        )
        initial = response.context_data["form"].initial
        self.assertEqual(initial["q1"], ("a", "c"))
        self.assertEqual(initial["q2"], ("a", "c"))
        self.assertEqual(initial["q3"], ("a", "c"))
        self.assertEqual(initial["q4"], ("a", "c"))
        self.assertEqual(initial["q5"], ("a", "c"))
        self.assertEqual(initial["q6"], ("a", "c"))
        self.assertEqual(initial["q7"], ("a", "c"))
        self.assertEqual(initial["q8"], ("a", "c"))
        self.assertEqual(initial["q9"], ("a", "c"))
        self.assertEqual(initial["q10"], ("a", "c"))
        self.assertEqual(initial["q11"], ("a", "c"))
        self.assertEqual(initial["q12"], ("a", "c"))
        self.assertEqual(initial["q13"], ("a", "c"))
        self.assertEqual(initial["q14"], ("a", "c"))
        self.assertEqual(initial["q15"], ("a", "c"))
        self.assertEqual(initial["q16"], ("a", "c"))
        self.assertEqual(initial["q17"], ("a", "c"))
        self.assertEqual(initial["q18"], ("a", "c"))
        self.assertEqual(initial["q19"], ("a", "c"))
        self.assertEqual(initial["q20"], ("a", "c"))
        self.assertEqual(initial["q21"], ("a", "c"))
        self.assertEqual(initial["q22"], ("a", "c"))
        self.assertEqual(initial["q23"], ("a", "c"))
        self.assertEqual(initial["q24"], ("a", "c"))
        self.assertEqual(initial["q25"], ("a", "c"))

    def test_send_form(self):
        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:complex", kwargs={"slug": self.slug}
            ),
            data=self.ComplexInstructionsData(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Location", response.headers)
        self.assertEqual(
            response.headers["Location"],
            urls.reverse("onboard:onboard:saved", kwargs={"slug": self.slug}),
        )

        onboard = models.Onboard.objects.get(slug=self.slug)
        complex_instructions_input = onboard.complexinstructionsinput

        self.assertEqual(complex_instructions_input.q1, (True, False, True))
        self.assertEqual(complex_instructions_input.q2, (True, False, True))
        self.assertEqual(complex_instructions_input.q3, (True, False, True))
        self.assertEqual(complex_instructions_input.q4, (True, False, True))
        self.assertEqual(complex_instructions_input.q5, (True, False, True))
        self.assertEqual(complex_instructions_input.q6, (True, False, True))
        self.assertEqual(complex_instructions_input.q7, (True, False, True))
        self.assertEqual(complex_instructions_input.q8, (True, False, True))
        self.assertEqual(complex_instructions_input.q9, (True, False, True))
        self.assertEqual(complex_instructions_input.q10, (True, False, True))
        self.assertEqual(complex_instructions_input.q11, (True, False, True))
        self.assertEqual(complex_instructions_input.q12, (True, False, True))
        self.assertEqual(complex_instructions_input.q13, (True, False, True))
        self.assertEqual(complex_instructions_input.q14, (True, False, True))
        self.assertEqual(complex_instructions_input.q15, (True, False, True))
        self.assertEqual(complex_instructions_input.q16, (True, False, True))
        self.assertEqual(complex_instructions_input.q17, (True, False, True))
        self.assertEqual(complex_instructions_input.q18, (True, False, True))
        self.assertEqual(complex_instructions_input.q19, (True, False, True))
        self.assertEqual(complex_instructions_input.q20, (True, False, True))
        self.assertEqual(complex_instructions_input.q21, (True, False, True))
        self.assertEqual(complex_instructions_input.q22, (True, False, True))
        self.assertEqual(complex_instructions_input.q23, (True, False, True))
        self.assertEqual(complex_instructions_input.q24, (True, False, True))
        self.assertEqual(complex_instructions_input.q25, (True, False, True))

    def test_send_form_without_answers(self):
        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:complex", kwargs={"slug": self.slug}
            ),
            data={},
        )

        self.assertEqual(response.status_code, 302)

        onboard = models.Onboard.objects.get(slug=self.slug)
        complex_instructions_input = onboard.complexinstructionsinput

        self.assertEqual(complex_instructions_input.q1, (False, False, False))
        self.assertEqual(complex_instructions_input.q2, (False, False, False))
        self.assertEqual(complex_instructions_input.q3, (False, False, False))
        self.assertEqual(complex_instructions_input.q4, (False, False, False))
        self.assertEqual(complex_instructions_input.q5, (False, False, False))
        self.assertEqual(complex_instructions_input.q6, (False, False, False))
        self.assertEqual(complex_instructions_input.q7, (False, False, False))
        self.assertEqual(complex_instructions_input.q8, (False, False, False))
        self.assertEqual(complex_instructions_input.q9, (False, False, False))
        self.assertEqual(complex_instructions_input.q10, (False, False, False))
        self.assertEqual(complex_instructions_input.q11, (False, False, False))
        self.assertEqual(complex_instructions_input.q12, (False, False, False))
        self.assertEqual(complex_instructions_input.q13, (False, False, False))
        self.assertEqual(complex_instructions_input.q14, (False, False, False))
        self.assertEqual(complex_instructions_input.q15, (False, False, False))
        self.assertEqual(complex_instructions_input.q16, (False, False, False))
        self.assertEqual(complex_instructions_input.q17, (False, False, False))
        self.assertEqual(complex_instructions_input.q18, (False, False, False))
        self.assertEqual(complex_instructions_input.q19, (False, False, False))
        self.assertEqual(complex_instructions_input.q20, (False, False, False))
        self.assertEqual(complex_instructions_input.q21, (False, False, False))
        self.assertEqual(complex_instructions_input.q22, (False, False, False))
        self.assertEqual(complex_instructions_input.q23, (False, False, False))
        self.assertEqual(complex_instructions_input.q24, (False, False, False))
        self.assertEqual(complex_instructions_input.q25, (False, False, False))

    def test_send_form_with_illegal_values(self):
        data = self.ComplexInstructionsData()
        data["q1"] = ["d"]

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:complex", kwargs={"slug": self.slug}
            ),
            data=data,
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn("q1", form.errors)
        self.assertEqual(
            form.errors["q1"],
            [
                "Escoja una opción válida. d no es una de las opciones"
                " disponibles."
            ],
        )

    def test_already_saved(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        models.ComplexInstructionsInput.objects.create(
            onboard=onboard,
            **self.ComplexInstructionsData(),
        )

        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:complex", kwargs={"slug": self.slug}
            ),
            data=self.ComplexInstructionsData(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Location", response.headers)
        self.assertEqual(
            response.headers["Location"],
            urls.reverse(
                "onboard:onboard:already-saved", kwargs={"slug": self.slug}
            ),
        )

    def test_compare_function(self):
        a = (True, True, True)
        b = (True, True, True, False)
        onboard = models.Onboard.objects.get(slug=self.slug)
        complex_instructions_input = (
            models.ComplexInstructionsInput.objects.create(
                onboard=onboard,
                **self.ComplexInstructionsData(),
            )
        )
        self.assertRaises(
            ValueError, complex_instructions_input._CalculateDifference, a, b
        )

    def test_perfect_score(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        complex_input = models.ComplexInstructionsInput.objects.create(
            onboard=onboard,
            q1="ac",
            q2="b",
            q3="a",
            q4="",
            q5="c",
            q6="a",
            q7="c",
            q8="",
            q9="",
            q10="a",
            q11="c",
            q12="",
            q13="b",
            q14="",
            q15="c",
            q16="",
            q17="",
            q18="",
            q19="ac",
            q20="ab",
            q21="c",
            q22="c",
            q23="a",
            q24="",
            q25="ab",
        )
        self.assertEqual(complex_input.LabeledScore[0], 0)
        self.assertEqual(complex_input.LabeledScore[1], "Adecuado")

    def test_regular_score(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        complex_input = models.ComplexInstructionsInput.objects.create(
            onboard=onboard,
            q1="ac",
            q2="b",
            q3="a",
            q4="c",
            q5="c",
            q6="a",
            q7="c",
            q8="a",
            q9="a",
            q10="a",
            q11="c",
            q12="b",
            q13="b",
            q14="b",
            q15="c",
            q16="a",
            q17="",
            q18="",
            q19="ac",
            q20="ab",
            q21="c",
            q22="c",
            q23="a",
            q24="",
            q25="ab",
        )
        self.assertEqual(complex_input.LabeledScore[0], 6)
        self.assertEqual(complex_input.LabeledScore[1], "Regular")

    def test_inferior_score(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        complex_input = models.ComplexInstructionsInput.objects.create(
            onboard=onboard,
            q1="ac",
            q2="b",
            q3="a",
            q4="abc",
            q5="c",
            q6="a",
            q7="c",
            q8="ab",
            q9="ac",
            q10="a",
            q11="c",
            q12="ac",
            q13="b",
            q14="bc",
            q15="c",
            q16="",
            q17="a",
            q18="",
            q19="ac",
            q20="ab",
            q21="c",
            q22="c",
            q23="a",
            q24="",
            q25="ab",
        )
        self.assertEqual(complex_input.LabeledScore[0], 12)
        self.assertEqual(
            complex_input.LabeledScore[1], "Inferior (Contraindicado)"
        )

    @staticmethod
    def ComplexInstructionsData():
        return {
            "q1": ["a", "c"],
            "q2": ["a", "c"],
            "q3": ["a", "c"],
            "q4": ["a", "c"],
            "q5": ["a", "c"],
            "q6": ["a", "c"],
            "q7": ["a", "c"],
            "q8": ["a", "c"],
            "q9": ["a", "c"],
            "q10": ["a", "c"],
            "q11": ["a", "c"],
            "q12": ["a", "c"],
            "q13": ["a", "c"],
            "q14": ["a", "c"],
            "q15": ["a", "c"],
            "q16": ["a", "c"],
            "q17": ["a", "c"],
            "q18": ["a", "c"],
            "q19": ["a", "c"],
            "q20": ["a", "c"],
            "q21": ["a", "c"],
            "q22": ["a", "c"],
            "q23": ["a", "c"],
            "q24": ["a", "c"],
            "q25": ["a", "c"],
        }


class OnboardAssessmentCareerAnchorsTestCase(TestCase):
    fixtures = ["initial-data", "onboard-test"]

    def setUp(self):
        self.client = Client()
        CreateValidUserAndLogin(self.client, "dummy")
        self.slug = "ce220ef060bb11edbbd1cf17990de5ba"  # see fixture

    def test_get_initial(self):
        onboard = models.Onboard.objects.get(slug=self.slug)
        models.CareerAnchorsInput.objects.create(
            onboard=onboard,
            q1=6,
            q2=6,
            q3=6,
            q4=6,
            q5=6,
            q6=6,
            q7=6,
            q8=6,
            q9=6,
            q10=6,
            q11=6,
            q12=6,
            q13=6,
            q14=6,
            q15=6,
            q16=6,
            q17=6,
            q18=6,
            q19=6,
            q20=6,
            q21=6,
            q22=6,
            q23=6,
            q24=6,
            q25=6,
            q26=6,
            q27=6,
            q28=6,
            q29=6,
            q30=6,
            q31=6,
            q32=6,
            q33=6,
            q34=6,
            q35=6,
            q36=6,
            q37=6,
            q38=6,
            q39=6,
            q40=6,
            favorite1=1,
            favorite2=2,
            favorite3=3,
        )
        response = self.client.get(
            urls.reverse(
                "onboard:onboard:assessment:career-anchors",
                kwargs={"slug": self.slug},
            ),
        )

        initial = response.context_data["form"].questions.initial

        self.assertEqual(initial["q1"], 6)
        self.assertEqual(initial["q2"], 6)
        self.assertEqual(initial["q3"], 6)
        self.assertEqual(initial["q4"], 6)
        self.assertEqual(initial["q5"], 6)
        self.assertEqual(initial["q6"], 6)
        self.assertEqual(initial["q7"], 6)
        self.assertEqual(initial["q8"], 6)
        self.assertEqual(initial["q9"], 6)
        self.assertEqual(initial["q10"], 6)
        self.assertEqual(initial["q11"], 6)
        self.assertEqual(initial["q12"], 6)
        self.assertEqual(initial["q13"], 6)
        self.assertEqual(initial["q14"], 6)
        self.assertEqual(initial["q15"], 6)
        self.assertEqual(initial["q16"], 6)
        self.assertEqual(initial["q17"], 6)
        self.assertEqual(initial["q18"], 6)
        self.assertEqual(initial["q19"], 6)
        self.assertEqual(initial["q20"], 6)
        self.assertEqual(initial["q21"], 6)
        self.assertEqual(initial["q22"], 6)
        self.assertEqual(initial["q23"], 6)
        self.assertEqual(initial["q24"], 6)
        self.assertEqual(initial["q25"], 6)
        self.assertEqual(initial["q26"], 6)
        self.assertEqual(initial["q27"], 6)
        self.assertEqual(initial["q28"], 6)
        self.assertEqual(initial["q29"], 6)
        self.assertEqual(initial["q30"], 6)
        self.assertEqual(initial["q31"], 6)
        self.assertEqual(initial["q32"], 6)
        self.assertEqual(initial["q33"], 6)
        self.assertEqual(initial["q34"], 6)
        self.assertEqual(initial["q35"], 6)
        self.assertEqual(initial["q36"], 6)
        self.assertEqual(initial["q37"], 6)
        self.assertEqual(initial["q38"], 6)
        self.assertEqual(initial["q39"], 6)
        self.assertEqual(initial["q40"], 6)

        initial = response.context_data["form"].favorites.initial

        self.assertEqual(initial["favorite1"], 1)
        self.assertEqual(initial["favorite2"], 2)
        self.assertEqual(initial["favorite3"], 3)

    def test_send_form(self):
        response = self.client.post(
            urls.reverse(
                "onboard:onboard:assessment:career-anchors",
                kwargs={"slug": self.slug},
            ),
            data=self.CareerAnchorsData(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Location", response.headers)
        self.assertEqual(
            response.headers["Location"],
            urls.reverse("onboard:onboard:saved", kwargs={"slug": self.slug}),
        )

        onboard = models.Onboard.objects.get(slug=self.slug)
        career_anchors_input = onboard.careeranchorsinput

        self.assertEqual(career_anchors_input.q1, 6)
        self.assertEqual(career_anchors_input.q2, 6)
        self.assertEqual(career_anchors_input.q3, 6)
        self.assertEqual(career_anchors_input.q4, 6)
        self.assertEqual(career_anchors_input.q5, 6)
        self.assertEqual(career_anchors_input.q6, 6)
        self.assertEqual(career_anchors_input.q7, 6)
        self.assertEqual(career_anchors_input.q8, 6)
        self.assertEqual(career_anchors_input.q9, 6)
        self.assertEqual(career_anchors_input.q10, 6)
        self.assertEqual(career_anchors_input.q11, 6)
        self.assertEqual(career_anchors_input.q12, 6)
        self.assertEqual(career_anchors_input.q13, 6)
        self.assertEqual(career_anchors_input.q14, 6)
        self.assertEqual(career_anchors_input.q15, 6)
        self.assertEqual(career_anchors_input.q16, 6)
        self.assertEqual(career_anchors_input.q17, 6)
        self.assertEqual(career_anchors_input.q18, 6)
        self.assertEqual(career_anchors_input.q19, 6)
        self.assertEqual(career_anchors_input.q20, 6)
        self.assertEqual(career_anchors_input.q21, 6)
        self.assertEqual(career_anchors_input.q22, 6)
        self.assertEqual(career_anchors_input.q23, 6)
        self.assertEqual(career_anchors_input.q24, 6)
        self.assertEqual(career_anchors_input.q25, 6)
        self.assertEqual(career_anchors_input.q26, 6)
        self.assertEqual(career_anchors_input.q27, 6)
        self.assertEqual(career_anchors_input.q28, 6)
        self.assertEqual(career_anchors_input.q29, 6)
        self.assertEqual(career_anchors_input.q30, 6)
        self.assertEqual(career_anchors_input.q31, 6)
        self.assertEqual(career_anchors_input.q32, 6)
        self.assertEqual(career_anchors_input.q33, 6)
        self.assertEqual(career_anchors_input.q34, 6)
        self.assertEqual(career_anchors_input.q35, 6)
        self.assertEqual(career_anchors_input.q36, 6)
        self.assertEqual(career_anchors_input.q37, 6)
        self.assertEqual(career_anchors_input.q38, 6)
        self.assertEqual(career_anchors_input.q39, 6)
        self.assertEqual(career_anchors_input.q40, 6)
        self.assertEqual(career_anchors_input.favorite1, 1)
        self.assertEqual(career_anchors_input.favorite2, 2)
        self.assertEqual(career_anchors_input.favorite3, 3)

    def test_favorites_validation(self):
        invalid_data = (
            {
                "favorite1": 9,
                "favorite2": 9,
            },
            {
                "favorite1": 9,
                "favorite3": 9,
            },
            {
                "favorite2": 9,
                "favorite3": 9,
            },
        )

        error_messages = (
            "La elección 1 debe ser distinta a la 2",
            "La elección 3 debe ser distinta a la 1",
            "La elección 2 debe ser distinta a la 3",
        )

        for data, error in zip(invalid_data, error_messages):
            response = self.client.post(
                urls.reverse(
                    "onboard:onboard:assessment:career-anchors",
                    kwargs={"slug": self.slug},
                ),
                data=dict(self.CareerAnchorsData(), **data),
            )

            self.assertEqual(response.status_code, 200)

            form = response.context_data["form"].favorites

            self.assertIn(error, form.errors["__all__"])

    @staticmethod
    def CareerAnchorsData():
        return {
            "q1": 6,
            "q2": 6,
            "q3": 6,
            "q4": 6,
            "q5": 6,
            "q6": 6,
            "q7": 6,
            "q8": 6,
            "q9": 6,
            "q10": 6,
            "q11": 6,
            "q12": 6,
            "q13": 6,
            "q14": 6,
            "q15": 6,
            "q16": 6,
            "q17": 6,
            "q18": 6,
            "q19": 6,
            "q20": 6,
            "q21": 6,
            "q22": 6,
            "q23": 6,
            "q24": 6,
            "q25": 6,
            "q26": 6,
            "q27": 6,
            "q28": 6,
            "q29": 6,
            "q30": 6,
            "q31": 6,
            "q32": 6,
            "q33": 6,
            "q34": 6,
            "q35": 6,
            "q36": 6,
            "q37": 6,
            "q38": 6,
            "q39": 6,
            "q40": 6,
            "favorite1": 1,
            "favorite2": 2,
            "favorite3": 3,
        }


class GoogleFormTestCase(TestCase):

    fixtures = ["initial-data", "onboard-test"]

    def setUp(self):
        CreateValidUserAndLogin(self.client, "dummy")

    def test_valid_url(self):
        GOOGLE_FORM_VALID_URL_TEST = (
            "https://docs.google.com/forms/d/e/"
            "1FAIpQLScxjC1-n5cP10ynWOmErM2g-UzInMlN44rxfUcXqiDl2ZH2Eg/viewform"
        )

        response = self.client.post(
            urls.reverse("onboard:googleform:create"),
            data={
                "title": "dummy",
                "description": "dummy",
                "shared_url": f"{GOOGLE_FORM_VALID_URL_TEST}",
                "view_link": f"{GOOGLE_FORM_VALID_URL_TEST}",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Location", response.headers)
        self.assertEqual(
            response.headers["Location"],
            urls.reverse("onboard:googleform:list"),
        )

    def test_invalid_url(self):

        GOOGLE_FORM_INVALID_URL_TEST = (
            "https://docs.google.com/forms/d/e/"
            "1FAIpQLScxjC1-n5cP10ynWOmErM2g-UzInMlN44rxfUcXqiDl2ZH2Eg/viewform"
            "?usp=sf_link"
        )

        response = self.client.post(
            urls.reverse("onboard:googleform:create"),
            data={
                "title": "dummy",
                "description": "dummy",
                "shared_url": f"{GOOGLE_FORM_INVALID_URL_TEST}",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "shared_url",
            f"{GOOGLE_FORM_INVALID_URL_TEST} has a not allowed query string."
            " Please write this with this structure:"
            " https://docs.google.com/forms/d/e/string_code/viewform",
        )

    def test_embed_view(self):
        googleform = models.GoogleForm.objects.create(
            title="dummy",
            description="dummy",
            shared_url="https://dummy/viewform",
            view_link="https://dummy/view",
        )
        self.slug = "ce220ef060bb11edbbd1cf17990de5ba"  # see fixture

        response = self.client.get(
            urls.reverse(
                "onboard:onboard:googleform",
                kwargs={"slug": self.slug, "googleform_id": googleform.id},
            )
        )

        self.assertEqual(response.context_data["object"], googleform)


# -----------------------------------------------------------------------------
# models


class ApplicantModelTestCase(TestCase):
    def test_str(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        self.assertEqual(str(applicant), "dummy")


class TmmsInputModelTestCase(TestCase):
    def test_male_labeled_scores(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        onboard = models.Onboard.objects.create(applicant=applicant)
        tmmsInput = models.TmmsInput(
            onboard=onboard,
            q1=1,
            q2=1,
            q3=1,
            q4=1,
            q5=1,
            q6=1,
            q7=1,
            q8=1,
            q9=1,
            q10=1,
            q11=1,
            q12=1,
            q13=1,
            q14=1,
            q15=1,
            q16=1,
            q17=1,
            q18=1,
            q19=1,
            q20=1,
            q21=1,
            q22=1,
            q23=1,
            q24=1,
        )

        labeled_scores = tmmsInput.labeled_scores

        self.assertEqual(
            labeled_scores,
            (
                (8, "Presta poca atención"),
                (8, "Deficiente comprensión"),
                (8, "Deficiente regulación"),
            ),
        )

    def test_female_labeled_scores(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.FEMALE
        )
        onboard = models.Onboard.objects.create(applicant=applicant)
        tmmsInput = models.TmmsInput(
            onboard=onboard,
            q1=1,
            q2=1,
            q3=1,
            q4=1,
            q5=1,
            q6=1,
            q7=1,
            q8=1,
            q9=1,
            q10=1,
            q11=1,
            q12=1,
            q13=1,
            q14=1,
            q15=1,
            q16=1,
            q17=1,
            q18=1,
            q19=1,
            q20=1,
            q21=1,
            q22=1,
            q23=1,
            q24=1,
        )

        labeled_scores = tmmsInput.labeled_scores

        self.assertEqual(
            labeled_scores,
            (
                (8, "Presta poca atención"),
                (8, "Deficiente comprensión"),
                (8, "Deficiente regulación"),
            ),
        )

    def test_invalid_gender(self):
        applicant = models.Applicant.objects.create(name="dummy", gender=3)
        onboard = models.Onboard.objects.create(applicant=applicant)
        tmmsInput = models.TmmsInput(
            onboard=onboard,
            q1=1,
            q2=1,
            q3=1,
            q4=1,
            q5=1,
            q6=1,
            q7=1,
            q8=1,
            q9=1,
            q10=1,
            q11=1,
            q12=1,
            q13=1,
            q14=1,
            q15=1,
            q16=1,
            q17=1,
            q18=1,
            q19=1,
            q20=1,
            q21=1,
            q22=1,
            q23=1,
            q24=1,
        )

        self.assertRaises(RuntimeError, lambda: tmmsInput.labeled_scores)

    def test_upper_bound_labeled_scores(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        onboard = models.Onboard.objects.create(applicant=applicant)
        tmmsInput = models.TmmsInput(
            onboard=onboard,
            q1=5,
            q2=5,
            q3=5,
            q4=5,
            q5=5,
            q6=5,
            q7=5,
            q8=5,
            q9=5,
            q10=5,
            q11=5,
            q12=5,
            q13=5,
            q14=5,
            q15=5,
            q16=5,
            q17=5,
            q18=5,
            q19=5,
            q20=5,
            q21=5,
            q22=5,
            q23=5,
            q24=5,
        )

        labeled_scores = tmmsInput.labeled_scores

        self.assertEqual(
            labeled_scores,
            (
                (40, "Presta demasiada atención"),
                (40, "Excelente compresión"),
                (40, "Excelente regulación"),
            ),
        )

    def test_out_bound_labeled_scores(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        onboard = models.Onboard.objects.create(applicant=applicant)
        tmmsInput = models.TmmsInput(
            onboard=onboard,
            q1=4,
            q2=4,
            q3=4,
            q4=4,
            q5=4,
            q6=4,
            q7=4,
            q8=4,
            q9=4,
            q10=4,
            q11=4,
            q12=4,
            q13=4,
            q14=4,
            q15=4,
            q16=4,
            q17=4,
            q18=4,
            q19=4,
            q20=4,
            q21=4,
            q22=4,
            q23=4,
            q24=4,
        )

        labeled_scores = tmmsInput.labeled_scores

        self.assertEqual(
            labeled_scores,
            (
                (32, "Adecuada atención"),
                (32, "Adecuada compresión"),
                (32, "Adecuada regulación"),
            ),
        )


class CareerAnchorsInputModelTestCase(TestCase):
    def test_most_scored_tf_df_ai(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        onboard = models.Onboard.objects.create(applicant=applicant)
        careerAnchorInput = models.CareerAnchorsInput(
            onboard=onboard,
            q1=1,
            q2=1,
            q3=1,
            q4=1,
            q5=1,
            q6=1,
            q7=1,
            q8=1,
            q9=1,
            q10=1,
            q11=1,
            q12=1,
            q13=1,
            q14=1,
            q15=1,
            q16=1,
            q17=1,
            q18=1,
            q19=1,
            q20=1,
            q21=1,
            q22=1,
            q23=1,
            q24=1,
            q25=1,
            q26=1,
            q27=1,
            q28=1,
            q29=1,
            q30=1,
            q31=1,
            q32=1,
            q33=1,
            q34=1,
            q35=1,
            q36=1,
            q37=1,
            q38=1,
            q39=1,
            q40=1,
            favorite1=1,
            favorite2=2,
            favorite3=3,
        )

        scores = careerAnchorInput.TopThreeRanking

        self.assertEqual(len(scores), 3)

        self.assertEqual(scores[0].name, "Técnica Funcional")
        self.assertEqual(scores[1].name, "Dirección General")
        self.assertEqual(scores[2].name, "Autonomía - Independencia")

        self.assertLessEqual(scores[1].score, scores[0].score)
        self.assertLessEqual(scores[2].score, scores[1].score)

    def test_most_scored_se_ce_sc(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        onboard = models.Onboard.objects.create(applicant=applicant)
        careerAnchorInput = models.CareerAnchorsInput(
            onboard=onboard,
            q1=1,
            q2=1,
            q3=1,
            q4=1,
            q5=1,
            q6=1,
            q7=1,
            q8=1,
            q9=1,
            q10=1,
            q11=1,
            q12=1,
            q13=1,
            q14=1,
            q15=1,
            q16=1,
            q17=1,
            q18=1,
            q19=1,
            q20=1,
            q21=1,
            q22=1,
            q23=1,
            q24=1,
            q25=1,
            q26=1,
            q27=1,
            q28=1,
            q29=1,
            q30=1,
            q31=1,
            q32=1,
            q33=1,
            q34=1,
            q35=1,
            q36=1,
            q37=1,
            q38=1,
            q39=1,
            q40=1,
            favorite1=4,
            favorite2=5,
            favorite3=6,
        )

        scores = careerAnchorInput.TopThreeRanking

        self.assertEqual(len(scores), 3)

        self.assertEqual(scores[0].name, "Seguridad y Estabilidad")
        self.assertEqual(scores[1].name, "Creatividad Empresarial")
        self.assertEqual(scores[2].name, "Servicio-Dedicación a una causa")

        self.assertLessEqual(scores[1].score, scores[0].score)
        self.assertLessEqual(scores[2].score, scores[1].score)

    def test_most_scored_sc_ed_ev(self):
        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        onboard = models.Onboard.objects.create(applicant=applicant)
        careerAnchorInput = models.CareerAnchorsInput(
            onboard=onboard,
            q1=1,
            q2=1,
            q3=1,
            q4=1,
            q5=1,
            q6=1,
            q7=1,
            q8=1,
            q9=1,
            q10=1,
            q11=1,
            q12=1,
            q13=1,
            q14=1,
            q15=1,
            q16=1,
            q17=1,
            q18=1,
            q19=1,
            q20=1,
            q21=1,
            q22=1,
            q23=1,
            q24=1,
            q25=1,
            q26=1,
            q27=1,
            q28=1,
            q29=1,
            q30=1,
            q31=1,
            q32=1,
            q33=1,
            q34=1,
            q35=1,
            q36=1,
            q37=1,
            q38=1,
            q39=1,
            q40=1,
            favorite1=6,
            favorite2=7,
            favorite3=8,
        )

        scores = careerAnchorInput.TopThreeRanking

        self.assertEqual(len(scores), 3)

        self.assertEqual(scores[0].name, "Servicio-Dedicación a una causa")
        self.assertEqual(scores[1].name, "Exclusivamente desafío")
        self.assertEqual(scores[2].name, "Estilo de vida")

        self.assertLessEqual(scores[1].score, scores[0].score)
        self.assertLessEqual(scores[2].score, scores[1].score)


# -----------------------------------------------------------------------------
# utils


def CreateValidUserAndLogin(
    client: Client,
    username: str,
    password: Optional[str] = None,
) -> User:
    user = CreateUser(client, username, password)

    neonautsDangerGroup = Group.objects.get(name="neonauts_onboard")
    user.groups.add(neonautsDangerGroup)

    client.force_login(user)
    return user


def CreateUserAndLogin(
    client: Client,
    username: str,
    password: Optional[str] = None,
) -> User:
    user = CreateUser(client, username, password)
    client.force_login(user)
    return user


def CreateUser(
    client: Client,
    username: str,
    password: Optional[str] = None,
) -> User:
    email = f"{username}@neomadas-test.com"
    return User.objects.create_user(username, email, password)


# -----------------------------------------------------------------------------
# base views


class BaseOnboardAssessmentViewTestCase(TestCase):
    """Este test debería ser mejorado creando un View hijo que implemente
    un modelform validando la apertura, guardado, reguardado y reapertura."""

    def test_form_valid(self):
        class TestView(views.BaseOnboardAssessmentView):
            pass

        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        onboard = models.Onboard.objects.create(slug="123", applicant=applicant)

        formMock = MagicMock()

        view = TestView()
        view.kwargs = {"slug": "123"}

        view.form_valid(formMock)

        self.assertEqual(formMock.instance.onboard, onboard)
        formMock.save.assert_called()

    def test_get_form_kwargs(self):
        class TestView(views.BaseOnboardAssessmentView):
            pass

        applicant = models.Applicant.objects.create(
            name="dummy", gender=models.Applicant.Gender.MALE
        )
        models.Onboard.objects.create(slug="123", applicant=applicant)

        modelMock = MagicMock()
        modelMock.onboard.field.related_query_name.return_value = "id"

        view = TestView()
        view.model = modelMock
        view.model.DoesNotExist = Exception
        view.kwargs = {"slug": "123"}
        view.request = MagicMock()
        view.request.method = "GET"

        view.get_form_kwargs()

        modelMock.onboard.field.related_query_name.assert_called()

    def test_get_validator(self):
        class TestView(views.BaseOnboardAssessmentView):
            pass

        self.assertRaises(ValueError, TestView()._GetValidator)


# -----------------------------------------------------------------------------
# email views


class EmailSenderBaseViewTestCase(TestCase):
    def test_send_email(self):
        class TestView(views.EmailSenderBaseView):
            pass

        test_view = TestView()

        self.assertEqual(test_view.get_html_message(), None)

        test_view.send_email("test subject", "test@test.com")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "test subject")

        recipients = mail.outbox[0].recipients()

        self.assertEqual(len(recipients), 1)
        self.assertEqual(recipients[0], "test@test.com")


class ApplicantOnboardEmailTestCase(TestCase):
    fixtures = ["initial-data", "onboard-test"]

    def setUp(self):
        self.applicant_id = 1
        self.client = Client()
        CreateValidUserAndLogin(self.client, "dummy")

    def test_detail_redirect(self):
        response = self.client.post(
            urls.reverse(
                "onboard:applicant:email-onboard",
                kwargs={"applicant_id": self.applicant_id},
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_send_email(self):
        self.client.post(
            urls.reverse(
                "onboard:applicant:email-onboard",
                kwargs={"applicant_id": self.applicant_id},
            )
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "#Snk809Jobs | Avanzaste a la 1ª Etapa🎉 | Puesto: ",
        )

        recipients = mail.outbox[0].recipients()

        self.assertEqual(len(recipients), 1)
        self.assertEqual(recipients[0], "dionisio@aguado.com")
