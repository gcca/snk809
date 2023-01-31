# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from neom.kit.template.library import Library
from neom.templatetags.neom_webtools import keytoken as _kt

register = Library()


@register.directtag
def neodash_md2_fonts():
    return f"""
    {{% load static %}}
    <style>
    @font-face {{
    font-family: 'Alata';
    font-style: normal;
    font-weight: 400;
    src: url({{% static 'neodash/fonts/Alata.woff2' %}}) format('woff2');
    }}
    @font-face {{
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 400;
    src: url({{% static 'neodash/fonts/Montserrat.woff2' %}}) format('woff2');
    }}
    .{_kt("mdc-typography--headline1")} {{
    font-family: 'Alata';
    font-size: 94}}
    .{_kt("mdc-typography--headline2")} {{
    font-family: 'Alata';
    font-size: 59}}
    .{_kt("mdc-typography--headline3")} {{
    font-family: 'Alata';
    font-size: 47}}
    .{_kt("mdc-typography--headline4")} {{
    font-family: 'Alata';
    font-size: 33}}
    .{_kt("mdc-typography--headline5")} {{
    font-family: 'Alata';
    font-size: 23}}
    .{_kt("mdc-typography--headline6")} {{
    font-family: 'Alata';
    font-size: 20}}
    .{_kt("mdc-typography--body1")} {{
    font-family: 'Montserrat';
    font-size: 14}}
    .{_kt("mdc-typography--body2")} {{
    font-family: 'Montserrat';
    font-size: 12}}
    .{_kt("mdc-typography--subtitle1")} {{
    font-family: 'Alata';
    font-size: 16}}
    .{_kt("mdc-typography--subtitle2")} {{
    font-family: 'Alata';
    font-size: 14}}
    .{_kt("mdc-typography--button")} {{
    font-family: 'Montserrat';
    font-size: 12}}
    .{_kt("mdc-typography--overline")} {{
    font-family: 'Montserrat';
    font-size: 9}}
    .{_kt("mdc-typography--caption")} {{
    font-family: 'Montserrat';
    font-size: 10}}
    </style>
    """


@register.composetag
def neodash_md2_card_elevated():
    return f'<div class="{_kt("mdc-card")}">', "</div>"


@register.composetag
def neodash_md2_card_outlined():
    return (
        f'<div class="{_kt("mdc-card")} {_kt("mdc-card--outlined")}">',
        "</div>",
    )


@register.composetag
def neodash_md2_card_actions():
    return f'<div class="{_kt("mdc-card__actions")}">', "</div>"


@register.composetag
def neodash_md2_card_actions_full_bleed():
    return (
        "<div"
        f' class="{_kt("mdc-card__actions")} '
        f'{_kt("mdc-card__actions--full-bleed")}">',
        "</div>",
    )


@register.singletag
def neodash_md2_card_action_button(label: str):
    return (
        "<button"
        f' class="{_kt("mdc-button")} {_kt("mdc-card__action")} '
        f'{_kt("mdc-card__action--button")}"><div'
        f' class="{_kt("mdc-button__ripple")}"></div><span'
        f' class="{_kt("mdc-button__label")}">{label}</span></button>'
    )


@register.singletag
def neodash_md2_card_action_link(label: str, link: str):
    return (
        f'<a class="{_kt("mdc-button")} {_kt("mdc-card__action")} '
        f'{_kt("mdc-card__action--button")}"'
        f' href="{link}"><div class="{_kt("mdc-button__ripple")}"></div><span'
        f' class="{_kt("mdc-button__label")}">{label}</span></a>'
    )


@register.composetag
def neodash_md2_top_app_bar():
    return (
        f'<header class="{_kt("mdc-top-app-bar")}">',
        "</header>"
        "<script>"
        "new mdc.topAppBar.MDCTopAppBar("
        f"document.querySelector('.{_kt('mdc-top-app-bar')}'));"
        "</script>",
    )


@register.composetag
def neodash_md2_main_top_bar():
    return (f'<main class="{_kt("mdc-top-app-bar--fixed-adjust")}">', "</main>")


@register.composetag
def neodash_md2_top_app_bar_row():
    return f'<div class="{_kt("mdc-top-app-bar__row")}">', "</div>"


@register.composetag
def neodash_md2_top_app_bar_section_align_start():
    return (
        f'<section class="{_kt("mdc-top-app-bar__section")} '
        f'{_kt("mdc-top-app-bar__section--align-start")}">',
        "</section>",
    )


@register.composetag
def neodash_md2_top_app_bar_section_align_end():
    return (
        f'<section class="{_kt("mdc-top-app-bar__section")} '
        f'{_kt("mdc-top-app-bar__section--align-end")}">',
        "</section>",
    )


@register.composetag
def neodash_md2_top_app_bar_title():
    return f'<span class="{_kt("mdc-top-app-bar__title")}">', "</span>"


@register.singletag
def neodash_md2_top_app_bar_navigation_icon(icon: str):
    return (
        f'<button class="{_kt("material-icons")} '
        f' {_kt("mdc-top-app-bar__navigation-icon")} '
        f' {_kt("mdc-icon-button")}">{icon}</button>'
    )


@register.singletag
def neodash_md2_top_app_bar_action_icon_button(icon: str):
    return (
        f'<button class="{_kt("material-icons")} '
        f'{_kt("mdc-top-app-bar__action-item")} '
        f'{_kt("mdc-icon-button")}">'
        f"{icon}</button>"
    )


@register.singletag
def neodash_md2_icon_button_contained(icon: str, label: str):
    button_classes = (
        f'{_kt("mdc-button")}'
        f' {_kt("mdc-button--raised")}'
        f' {_kt("mdc-button--leading")}'
    )
    icon_classes = f'{_kt("material-icons")} {_kt("mdc-button__icon")}'
    return (
        f'<button class="{button_classes}"><span'
        f' class="{_kt("mdc-button__ripple")}"></span><i'
        f' class="{icon_classes}">{icon}</i><span'
        f' class="{_kt("mdc-button__label")}">{label}</span></button>'
    )
