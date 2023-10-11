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
from scripts.all_questions.read_forms import (  # noqa: E402
    find_forms_dir,
)  # , build_form  # noqa: E402
from scripts.all_questions.metadata_utils import (  # noqa: E402
    generate_section_headings,
)  # noqa: E402


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


def print_html_toc(air: Airium, sections: dict):
    with air.h2(klass="govuk-heading-m "):
        air("{% trans %}Table of contents{% endtrans %}")
    with air.ol(klass="govuk-list govuk-list--number"):
        for anchor, details in sections.items():
            with air.li():
                with air.a(klass="govuk-link", href=f"#{anchor}"):
                    air(details["title_text"])


def print_components(air: Airium, components: list, level_above):
    for c in components:
        if not c["hide_title"] and c["title"] is not None:
            with air.h4(klass="govuk-heading-s"):
                air(f"{c['title']}")

        for t in c["text"]:
            if isinstance(t, list):
                with air.ul(klass="govuk-list govuk-list--bullet"):
                    for bullet in t:
                        with air.li(klass=""):
                            air(bullet)
            else:
                with air.p(klass="govuk-body"):
                    air(t)


def print_html(sections: dict, lang) -> str:
    with air.div(klass="govuk-!-margin-bottom-8"):
        print_html_toc(air, sections)
        idx_section = 1
        for anchor, details in sections.items():
            air.hr(
                klass=(
                    "govuk-section-break govuk-section-break--l"
                    " govuk-section-break--visible"
                )
            )
            with air.h2(klass="govuk-heading-l", id=anchor):
                air(f"{idx_section}. {details['title_text']}")

            form_print_headings = details["form_print_headings"]
            for heading in sorted(
                form_print_headings,
                key=lambda item: str((form_print_headings[item])["heading_number"]),
            ):
                header_info = form_print_headings[heading]
                if header_info["is_form_heading"]:
                    with air.h3(klass="govuk-heading-m"):
                        air(f"{header_info['heading_number']}. {header_info['title']}")

                else:
                    with air.h4(klass="govuk-heading-s"):
                        air(f"{header_info['heading_number']}. {header_info['title']}")

                print_components(air, header_info["components"], 0)

            idx_section += 1

    html = f"{BOILERPLATE_START}{str(air)}{BOILERPLATE_END}"
    print(html)
    return html


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
    default="/Users/sarahsloan/dev/CommunitiesUkWorkspace/funding-service-design-frontend/app/templates/",
    help="Folder to write output html to",
    prompt=True,
)
@click.option(
    "--forms_dir",
    default="/Users/sarahsloan/dev/CommunitiesUkWorkspace/digital-form-builder/fsd_config/form_jsons/",
    help="Local, absolute path, to the form JSONs to use to generate question lists",
    prompt=True,
)
def generate_all_questions(
    fund_short_code=None,
    round_short_code=None,
    lang=None,
    output_location=None,
    forms_dir=None,
):
    app = create_app()
    with app.app_context():
        round = get_round_by_short_name(fund_short_code, round_short_code)
        sections: list[Section] = get_application_sections_for_round(
            round.fund_id, round.id
        )

        path_to_form_jsons = find_forms_dir(
            forms_dir, fund_short_code, round_short_code, lang
        )

        section_map = generate_section_headings(
            sections=sections, path_to_form_jsons=path_to_form_jsons, lang=lang
        )

        html_str = print_html(
            sections=section_map,
            lang=lang,
        )
        filename = f"{fund_short_code.casefold()}_{round_short_code.casefold()}_all_questions.html"
        with open(f"{output_location}{filename}", "w") as f:
            f.write(html_str)


if __name__ == "__main__":
    generate_all_questions()
