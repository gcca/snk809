# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django import template, urls
from django.template.exceptions import TemplateSyntaxError
from django.utils.html import format_html

register = template.Library()


@register.tag
def neodash_nav_item(parser, token):
    bits = token.split_contents()[1:]

    if len(bits) < 2:
        raise TemplateSyntaxError("neodash_nav_item at least two parameters")

    pathFilter = parser.compile_filter(bits[0])
    labelFilter = parser.compile_filter(bits[1])
    # TODO: acá manejar argumentos variables en lugar de sólo uno
    extraKwarg = (
        template.library.token_kwargs([bits[2]], parser)
        if len(bits) > 2
        else {}
    )

    return NeodashNavItemNode(pathFilter, labelFilter, extraKwarg)


@register.tag
def neodash_nav_mark(parser, token):
    bits = token.split_contents()[1:]

    if len(bits) != 1:
        raise TemplateSyntaxError("neodash_nav_mark one parameter")

    markFilter = parser.compile_filter(bits[0])

    return NeodashNavMarkNode(markFilter)


@register.tag
def neodash_nav(parser, token):
    nodelist = parser.parse(("end_neodash_nav",))
    parser.delete_first_token()
    return NeodashNavNode(nodelist)


class NeodashNavItemNode(template.Node):
    def __init__(self, pathFilter, labelFilter, extraKwarg):
        self.pathFilter = pathFilter
        self.labelFilter = labelFilter
        self.extraKwarg = extraKwarg

    def render(self, context):
        kwargs = {
            key: value.resolve(context)
            for key, value in self.extraKwarg.items()
        }
        url = urls.reverse(self.pathFilter.resolve(context), kwargs=kwargs)
        label = self.labelFilter.resolve(context)
        return format_html(f'<li><a href="{url}">{label}</a></li>')


class NeodashNavMarkNode(template.Node):
    def __init__(self, markFilter):
        self.markFilter = markFilter

    def render(self, context):
        mark = self.markFilter.resolve(context)
        return format_html(f'<li><em style="color:gray;">{mark}</em></li>')


class NeodashNavNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return f"<header><nav><ul>{output}</ul></nav></header>"
