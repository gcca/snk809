# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from html.parser import HTMLParser
from unittest.mock import MagicMock

from django import urls
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError
from django.test import TestCase
from neom.templatetags.neom_webtools import keytoken as _kt

from . import mixins, templatetags

# -----------------------------------------------------------------------------
# mixins


class PermissionsAppMixinTestCase(TestCase):
    def test_no_app_label(self):
        mixin = mixins.PermissionsAppMixin()
        with self.assertRaisesRegex(
            AttributeError,
            "You need to define the `app_label` member in"
            " <neodash.mixins.PermissionsAppMixin object at 0x[\\w]+>",
        ):
            mixin.test_func()


# -----------------------------------------------------------------------------
# templatetags


class TemplateTagNeodashNavTestCase(TestCase):
    def setUp(self):
        self.parserMock = MagicMock()
        self.tokenMock = MagicMock()

    def test_nav_item_exception_without_parameters(self):
        self.tokenMock.split_contents.return_value = []

        with self.assertRaisesMessage(
            TemplateSyntaxError, "neodash_nav_item at least two parameters"
        ):
            templatetags.neodash_nav.neodash_nav_item(
                self.parserMock, self.tokenMock
            )

    def test_nav_mark_exception_without_parameters(self):
        self.tokenMock.split_contents.return_value = []

        with self.assertRaisesMessage(
            TemplateSyntaxError, "neodash_nav_mark one parameter"
        ):
            templatetags.neodash_nav.neodash_nav_mark(
                self.parserMock, self.tokenMock
            )

    def test_render_nav_item(self):
        self.tokenMock.split_contents.return_value = [
            None,
            '"onboard:dashboard"',
            '"Dashboard"',
        ]

        def compile_filter_mock(x):
            mock = MagicMock()
            mock.resolve.return_value = x[1:-1]
            return mock

        self.parserMock.compile_filter.side_effect = compile_filter_mock

        node = templatetags.neodash_nav.neodash_nav_item(
            self.parserMock, self.tokenMock
        )

        html = node.render({})

        url = urls.reverse("onboard:dashboard")
        self.assertEqual(html, f'<li><a href="{url}">Dashboard</a></li>')

    def test_render_nav(self):
        nodelistMock = MagicMock()
        nodelistMock.render.return_value = "dummy"

        self.parserMock.parse.return_value = nodelistMock

        node = templatetags.neodash_nav.neodash_nav(
            self.parserMock, self.tokenMock
        )

        html = node.render({})

        self.assertEqual(html, "<header><nav><ul>dummy</ul></nav></header>")


class TemplateTagNeodashOptionsTestCase(TestCase):
    def test_basic_usage(self):
        html = Template(
            "{% load neodash_options %}\n"
            "{% neodash_options %}\n"
            "{% neodash_options_separator %}\n"
            "{% neodash_option 'neodash:home' 'Home' %}"
            "{% end_neodash_options %}"
        ).render(Context())

        class BasicUsageParser(HTMLParser):
            enabled = False

            def handle_starttag(self, tag, attrs):
                if tag == "a":
                    attr_index = 0
                    value_index = 1
                    self.href = attrs[attr_index][value_index]
                    self.enabled = True

            def handle_endtag(self, tag):
                if tag == "a":
                    self.enabled = False

            def handle_data(self, data):
                if self.enabled:
                    self.text = data
                    self.enabled = False

        parser = BasicUsageParser()
        parser.feed(html)

        self.assertEqual(parser.text, "Home")
        self.assertEqual(urls.reverse("neodash:home"), parser.href)

    def test_bad_option_arguments(self):
        with self.assertRaisesMessage(
            TemplateSyntaxError, "neodash_option at least two arguments"
        ):
            Template(
                "{% load neodash_options %}\n"
                "{% neodash_options %}\n"
                "{% neodash_option 'neodash:home' %}"
                "{% end_neodash_options %}"
            ).render(Context())

    def test_bad_options_edit_arguments(self):
        with self.assertRaisesMessage(
            TemplateSyntaxError, "neodash_options_edit at least one arguments"
        ):
            Template(
                "{% load neodash_options %}\n"
                "{% neodash_options %}\n"
                "{% neodash_options_edit %}"
                "{% end_neodash_options %}"
            ).render(Context())


# -----------------------------------------------------------------------------
# templatetags - pending


class NeodashMd2TopAppVarTestCase(TestCase):
    def setUp(self):
        self.parser = self.TopBarParser()

    def test_neodash_md2_top_app_bar_section_align_end(self):
        html = Template(
            "{% load neodash_md2 %}\n"
            "{% neodash_md2_top_app_bar_section_align_end %}"
            "{% end_neodash_md2_top_app_bar_section_align_end %}"
        ).render(Context())

        self.parser.feed(html)

        self.assertEqual(len(self.parser.sections), 1)

        classnames = self.parser.sections[0]["class"]

        self.assertIn(_kt("mdc-top-app-bar__section"), classnames)
        self.assertIn(_kt("mdc-top-app-bar__section--align-end"), classnames)

    def test_neodash_md2_top_app_bar_section_align_start(self):
        html = Template(
            "{% load neodash_md2 %}\n"
            "{% neodash_md2_top_app_bar_section_align_start %}"
            "{% end_neodash_md2_top_app_bar_section_align_start %}"
        ).render(Context())

        self.parser.feed(html)

        self.assertEqual(len(self.parser.sections), 1)

        classnames = self.parser.sections[0]["class"]

        self.assertIn(_kt("mdc-top-app-bar__section"), classnames)
        self.assertIn(_kt("mdc-top-app-bar__section--align-start"), classnames)

    def test_neodash_md2_top_app_bar_action_icon_button(self):
        html = Template(
            "{% load neodash_md2 %}\n"
            "{% neodash_md2_top_app_bar_action_icon_button 'android' %}"
        ).render(Context())

        self.parser.feed(html)

        self.assertEqual(len(self.parser.buttons), 1)

        classnames = self.parser.buttons[0]["class"]

        self.assertIn(_kt("material-icons"), classnames)
        self.assertIn(_kt("mdc-top-app-bar__action-item"), classnames)
        self.assertIn(_kt("mdc-icon-button"), classnames)
        self.assertIn("android", self.parser.datas)

    def test_neodash_md2_top_app_bar_navigation_icon(self):
        html = Template(
            "{% load neodash_md2 %}\n"
            "{% neodash_md2_top_app_bar_navigation_icon 'menu' %}"
        ).render(Context())

        self.parser.feed(html)

        self.assertEqual(len(self.parser.buttons), 1)

        classnames = self.parser.buttons[0]["class"]

        self.assertIn(_kt("material-icons"), classnames)
        self.assertIn(_kt("mdc-top-app-bar__navigation-icon"), classnames)
        self.assertIn(_kt("mdc-icon-button"), classnames)
        self.assertIn("menu", self.parser.datas)

    class TopBarParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sections = []
            self.buttons = []
            self.datas = []

        def handle_starttag(self, tag, attrs):
            if tag == "button":
                self.buttons.append(dict(attrs))

            if tag == "section":
                self.sections.append(dict(attrs))

        def handle_data(self, data):
            self.datas.append(data)


class TemplateTagNeodashMd2TestCase(TestCase):
    def setUp(self):
        self.parser = HTMLParser()

    def test_neodash_md2_card_elevated(self):
        html = Template(
            "{% load neodash_md2 %}\n"
            "{% neodash_md2_card_elevated %}"
            "{% end_neodash_md2_card_elevated %}"
        ).render(Context())

        self.parser.feed(html)

        self.assertEqual(self.parser.lasttag, "div")

    def test_neodash_md2_card_action_button(self):
        html = Template(
            "{% load neodash_md2 %}\n"
            '{% neodash_md2_card_action_button "ACCEPT" %}'
        ).render(Context())

        self.parser.feed(html)

    def test_neodash_md2_card_actions(self):
        html = Template(
            "{% load neodash_md2 %}\n"
            "{% neodash_md2_card_actions %}"
            "{% end_neodash_md2_card_actions %}"
        ).render(Context())

        self.parser.feed(html)
