import sys

import click

sys.path.insert(1, ".")

from db.models.section import Section  # noqa: E402
from db.queries import (  # noqa: E402
    get_application_sections_for_round,
    get_round_by_short_name,
)  # noqa: E402
from app import create_app  # noqa: E402
from airium import Airium  # noqa: E402

air = Airium()

BOILERPLATE_START = """
{% extends "base.html" %}
{%- from 'govuk_frontend_jinja/components/inset-text/macro.html' import govukInsetText -%}
{%- from "govuk_frontend_jinja/components/button/macro.html" import govukButton -%}

{% from "partials/file-formats.html" import file_formats %}
{% set pageHeading %}{% trans %}Full list of application questions{% endtrans %}{% endset %}
{% block content %}
<div class="govuk-grid-row">
    <div class="govuk-grid-column-two-thirds">
        <span class="govuk-caption-l">{% trans %}{{fund_title}}{% endtrans %} {{round_title}}</span>
        <h1 class="govuk-heading-xl">{{pageHeading}}</h1>
"""

BOILERPLATE_END = """
    </div>
</div>
{% endblock %}
"""


def print_html(section_headers: dict) -> str:
    with air.div(klass="govuk-!-margin-bottom-8"):
        with air.h2(klass="govuk-heading-m "):
            air("{% trans %}Table of contents{% endtrans %}")
        with air.ol(klass="govuk-list govuk-list--number"):
            for anchor, text in section_headers.items():
                with air.li():
                    with air.a(klass="govuk-link", href=f"#{anchor}"):
                        air(text)
        index = 1
        for anchor, text in section_headers.items():
            air.hr(
                klass=(
                    "govuk-section-break govuk-section-break--l"
                    " govuk-section-break--visible"
                )
            )
            with air.h2(klass="govuk-heading-l", id=anchor):
                air(f"{index}. {text}")
            index += 1

    html = f"{BOILERPLATE_START}{str(air)}{BOILERPLATE_END}"
    print(html)
    return html


def build_section_headers(sections: list[Section], lang):
    section_headers = {}
    for s in sections:
        title = s.title_json[lang]
        i = title.find(". ")
        if i != -1:
            title = title[i + 2 :]
        else:
            title = title
        anchor = title.casefold().replace(" ", "-")
        section_headers[anchor] = title
    return section_headers


@click.command()
@click.option("--fund_short_code", default="CYP", help="Fund short code", prompt=True)
@click.option("--round_short_code", default="R1", help="Round short code", prompt=True)
@click.option(
    "--lang",
    default="en",
    help="Language - used when a round supports english and welsh",
    prompt=True,
    type=click.Choice(["en", "cy"]),
)
@click.option(
    "--output_location",
    default="/Users/sarahsloan/dev/temp/",
    help="Folder to write output html to",
    prompt=True,
)
def generate_all_questions(
    fund_short_code=None, round_short_code=None, lang=None, output_location=None
):
    app = create_app()
    with app.app_context():
        round = get_round_by_short_name(fund_short_code, round_short_code)
        sections = get_application_sections_for_round(round.fund_id, round.id)

        section_headers = build_section_headers(sections, lang)

        html_str = print_html(section_headers=section_headers)
        filename = f"{fund_short_code.casefold()}_{round_short_code.casefold()}_all_questions.html"
        with open(f"{output_location}{filename}", "w") as f:
            f.write(html_str)


if __name__ == "__main__":
    generate_all_questions()
