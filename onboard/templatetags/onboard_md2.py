# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from neom.kit.template.library import Library
from neom.templatetags.neom_webtools import keytoken as _kt

register = Library()


@register.directtag
def onboard_md2_quiz_card_style():
    return """
    {% load neom_webtools %}
    .{% _kt 'onboard-md2-quiz-card__head' %} {
    margin: 0.2rem 0;
    padding: 16px;
    display: flex;
    align-items: center;
    }
    .{% _kt 'mdc-card' %} .{% _kt 'onboard-md2-quiz-card__thumbnail' %} {
    padding-right: 8px;
    }
    .{% _kt 'onboard-md2-quiz-card__head' %} h2,
    .{% _kt 'onboard-md2-quiz-card__head' %} h3 {
    margin: 0;
    }
    .{% _kt 'onboard-md2-quiz-card__body' %} {
    padding: 16px;
    }
    .{% _kt 'onboard-md2-quiz-card__thumbnail' %} img {
    border-radius: 50%;
    height: 50px;
    width: 50px;
    }
    """


@register.directtag
def onboard_md2_quiz_card(
    title: str, duration: str, thumbnail: str, description: str, link: str
):
    prefix = "onboard-md2-quiz-card"
    head_classname = f"{prefix}__head"
    body_classname = f"{prefix}__body"
    thumbnail_classname = f"{prefix}__thumbnail"
    title_classname = f"{prefix}__title"

    headline_classname = f'{_kt("mdc-typography--headline6")}'
    subtitle_classname = f'{_kt("mdc-typography--subtitle2")}'
    description_classname = (
        f'{_kt(body_classname)} {_kt("mdc-typography--body2")}'
    )

    return (
        "{% load neodash_md2 %}{% neodash_md2_card_outlined %}<div"
        f' class="{_kt(head_classname)}"><div'
        f' class="{_kt(thumbnail_classname)}"><img src="{thumbnail}"></div><div'
        f' class="{_kt(title_classname)}"><h2'
        f' class="{headline_classname}">{title}</h2><h3'
        f' class="{subtitle_classname}">{duration} </h3></div></div><div'
        f' class="{description_classname}">{description}</div>{{%'
        " neodash_md2_card_actions_full_bleed %}{%"
        f' neodash_md2_card_action_link "TOMAR TEST" "{link}" %}}{{%'
        " end_neodash_md2_card_actions_full_bleed %}{%"
        " end_neodash_md2_card_outlined %}"
    )


@register.directtag
def onboard_top_bar():
    header_image = "onboard/images/logo-neomadas-white-header.png"
    return (
        "{% load neodash_md2 %}"
        "{% load static %}"
        "{% neodash_md2_top_app_bar %}"
        "{% neodash_md2_top_app_bar_row %}"
        "{% neodash_md2_top_app_bar_section_align_start %}"
        "{% neodash_md2_top_app_bar_title %}"
        '<img style="height: 75%" '
        f" src=\"{{% static '{header_image}' %}}\" />"
        "{% end_neodash_md2_top_app_bar_title %}"
        "{% end_neodash_md2_top_app_bar_section_align_start %}"
        "{% end_neodash_md2_top_app_bar_row %}"
        "{% end_neodash_md2_top_app_bar %}"
    )
