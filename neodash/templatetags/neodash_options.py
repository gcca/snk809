# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django import template, urls
from django.template.exceptions import TemplateSyntaxError

register = template.Library()


@register.tag
def neodash_option(parser, token):
    min_arguments_len = 2
    bits = token.split_contents()[1:]

    if len(bits) < min_arguments_len:
        raise TemplateSyntaxError("neodash_option at least two arguments")

    pathFilter = parser.compile_filter(bits[0])
    labelFilter = parser.compile_filter(bits[1])

    extraKwarg = (  # TODO: argumentos variables
        template.library.token_kwargs([bits[min_arguments_len]], parser)
        if len(bits) > min_arguments_len
        else {}
    )

    return NeodashOptionNode(pathFilter, labelFilter, extraKwarg)


@register.tag
def neodash_options(parser, token):
    nodelist = parser.parse(("end_neodash_options",))
    parser.delete_first_token()
    return NeodashOptionsNode(nodelist)


@register.tag
def neodash_options_edit(parser, token):
    min_arguments_len = 1
    bits = token.split_contents()[1:]

    if len(bits) < min_arguments_len:
        raise TemplateSyntaxError("neodash_options_edit at least one arguments")

    pathFilter = parser.compile_filter(bits[0])

    extraKwarg = (  # TODO: argumentos variables
        template.library.token_kwargs([bits[min_arguments_len]], parser)
        if len(bits) > min_arguments_len
        else {}
    )

    return NeodashOptionsEditNode(pathFilter, extraKwarg)


@register.tag
def neodash_options_separator(_, __):
    return NeodashOptionsSeparatorNode()


class NeodashOptionNode(template.Node):
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
        return (
            '<li style="list-style:none;display:inline;margin-right:1em">'
            f'<a href="{url}">{label}</a></li>'
        )


class NeodashOptionsNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return (
            "<div>Acciones:"
            '<ul style="user-select:none;display:inline;padding-left:10">'
            f"{output}</ul></div>"
        )


class NeodashOptionsEditNode(template.Node):
    def __init__(self, pathFilter, extraKwarg):
        self.pathFilter = pathFilter
        self.extraKwarg = extraKwarg

    EDIT_PAIRS = (
        (":update", "Update"),
        # TODO: delete
    )

    def render(self, context):
        kwargs = {
            key: value.resolve(context)
            for key, value in self.extraKwarg.items()
        }
        return "".join(
            self.ReverseLi(context, kwargs, pathname, label)
            for pathname, label in self.EDIT_PAIRS
        )

    def ReverseLi(self, context, kwargs, pathname, label):
        path = self.pathFilter.resolve(context) + pathname
        url = urls.reverse(path, kwargs=kwargs)
        return (
            '<li style="list-style:none;display:inline;margin-right:1em">'
            f'<a href="{url}">{label}</a></li>'
        )


class NeodashOptionsSeparatorNode(template.Node):
    def render(self, _):
        return (
            '<li style="list-style:none;display:inline;margin-right:1em">|</li>'
        )
