# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

import os.path
from typing import NamedTuple

from django.forms import widgets


class ResumeFileInput(widgets.ClearableFileInput):
    template_name = "onboard/forms/widgets/resume_file_input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {"basename": os.path.basename(value.path) if value else ""}
        )
        return context


class DiscInput(widgets.Widget):
    class ValueTuple(NamedTuple):
        minus: int
        plus: int

    template_name = "onboard/forms/widgets/disc_input.html"

    def format_value(self, value):
        return value

    def value_from_datadict(self, data, files, name):
        minus = data.get(f"{name}-minus")
        plus = data.get(f"{name}-plus")

        minus = 0 if minus is None else int(minus)
        plus = 0 if plus is None else int(plus)

        if not minus and not plus:
            return None

        return self.ValueTuple(minus, plus)
