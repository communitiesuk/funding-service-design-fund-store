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
import os.path  # noqa: E402
import json  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
from scripts.read_forms import strip_leading_numbers, build_form  # noqa: E402


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


def create_toc(air: Airium, section_headers: dict):
    with air.h2(klass="govuk-heading-m "):
        air("{% trans %}Table of contents{% endtrans %}")
    with air.ol(klass="govuk-list govuk-list--number"):
        for anchor, text in section_headers.items():
            with air.li():
                with air.a(klass="govuk-link", href=f"#{anchor}"):
                    air(text)


def find_forms_dir(path_to_form_jsons, fund_short_name, round_short_name, lang):
    round_folder_path = os.path.join(
        path_to_form_jsons,
        f"{fund_short_name.casefold()}_{round_short_name.casefold()}",
    )
    if not os.path.isdir(round_folder_path):
        print(f"ERROR Could not find form_jsons at {round_folder_path}")

    path_with_lang = os.path.join(round_folder_path, lang)
    if not os.path.isdir(path_with_lang):
        return round_folder_path
    else:
        return path_with_lang


def build_section_header(section: Section, lang="en"):
    title = section.title_json[lang]
    title = strip_leading_numbers(title)
    anchor = title.casefold().replace(" ", "-")
    return anchor, title
    # section_header[anchor] = title
    # section_headers[f"{anchor}_form_name"]= s["form_name"]["form_name_json"]["lang"]
    # return section_header


def build_components_from_page(p, include_html_components=True):
    components = []
    for c in p["components"]:
        text = []
        if (
            include_html_components
            and ("type" in c)
            and (c["type"].casefold() == "html" or c["type"].casefold() == "para")
        ):
            text = [c["content"]]
        elif "hint" in c:
            soup = BeautifulSoup(c["hint"], "html.parser")
            text = [e.text for e in soup.children]
        component = {
            "title": c["title"] if "title" in c else None,
            "text": text,
            "hide_title": c["options"]["hideTitle"]
            if "hideTitle" in c["options"]
            else False,
        }
        components.append(component)
    return components


def build_questions_for_form(air: Airium, form_name: str, path_to_forms: str):
    path_to_form = os.path.join(path_to_forms, f"{form_name}.json")
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    pages = {}
    index = 1
    start_page = form_data["startPage"]
    first_page = next(p for p in form_data["pages"] if p["path"] == start_page)
    is_just_html_start_page = all(
        [
            (c["type"].casefold() == "para" or c["type"].casefold() == "html")
            for c in first_page["components"]
        ]
    )
    if is_just_html_start_page:
        real_first_page_path = first_page["next"][0]["path"]
        real_first_page = next(
            p for p in form_data["pages"] if p["path"] == real_first_page_path
        )
        form_first_page = {
            "title": real_first_page["title"],
            "components": build_components_from_page(
                real_first_page, include_html_components=False
            ),
        }
    else:
        form_first_page = {
            "title": first_page["title"],
            "components": build_components_from_page(
                first_page, include_html_components=True
            ),
        }
    for p in form_data["pages"]:
        if p["path"] == "/summary" or p["path"] == start_page:
            continue
        components = build_components_from_page(p)

        page = {"title": p["title"], "components": components}
        pages[index] = page
        index += 1
    return form_first_page, pages


def print_components(air: Airium, components: list, level_above):
    idx_component = 1
    for c in components:
        if not c["hide_title"] and c["title"] is not None:
            with air.h4(klass="govuk-heading-s"):
                air(f"{level_above}{idx_component}. {c['title']}")

        for t in c["text"]:
            with air.p(klass="govuk-body"):
                air(t)


def print_html(
    sections: list[Section], fund_short_name, round_short_name, lang, path_to_form_jsons
) -> str:
    section_headers = {}
    section_children = {}
    for s in sections:
        anchor, text = build_section_header(s)
        section_headers[anchor] = text
        section_children[anchor] = s.children
    with air.div(klass="govuk-!-margin-bottom-8"):
        create_toc(air, section_headers)
        forms_dir = find_forms_dir(
            path_to_form_jsons, fund_short_name, round_short_name, lang
        )
        idx_section = 1
        for anchor, text in section_headers.items():
            air.hr(
                klass=(
                    "govuk-section-break govuk-section-break--l"
                    " govuk-section-break--visible"
                )
            )
            with air.h2(klass="govuk-heading-l", id=anchor):
                air(f"{idx_section}. {text}")

            idx_form = 1
            for child_form in section_children[anchor]:
                form_name = child_form.form_name[0].form_name_json[lang]

                form_index = build_form(form_name=form_name, path_to_forms=forms_dir)

                for page_idx, page in form_index.items():
                    if page_idx == 1:
                        with air.h3(klass="govuk-heading-m"):
                            air(f"{idx_section}.{idx_form}. {page['page_title']}")
                    else:
                        with air.h4(klass="govuk-heading-s"):
                            air(
                                f"{idx_section}.{idx_form}.{page_idx}."
                                f" {page['page_title']}"
                            )

                    print_components(air, page["page_children"], 0)
                    # print page["page_children"]

                # form_first_page, pages = build_questions_for_form(air, form_name, forms_dir)
                # with air.h3(klass="govuk-heading-m"):
                #     air(f"{idx_section}.{idx_form}. {form_first_page['title']}")
                # print_components(air, form_first_page["components"], f"{idx_section}.{idx_form}.")
                # for idx_page, page in pages.items():
                #     with air.h4(klass="govuk-heading-s"):
                #         air(f"{idx_section}.{idx_form}.{idx_page}. {page['title']}")
                #     print_components(air,page["components"], f"{idx_section}.{idx_form}.{idx_page}.")
                idx_form += 1

            idx_section += 1

    html = f"{BOILERPLATE_START}{str(air)}{BOILERPLATE_END}"
    print(html)
    print(forms_dir)
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
        sections = get_application_sections_for_round(round.fund_id, round.id)

        # section_headers = build_section_headers(sections, lang)

        html_str = print_html(
            sections,
            fund_short_name=fund_short_code,
            round_short_name=round_short_code,
            lang=lang,
            path_to_form_jsons=forms_dir,
        )
        filename = f"{fund_short_code.casefold()}_{round_short_code.casefold()}_all_questions.html"
        with open(f"{output_location}{filename}", "w") as f:
            f.write(html_str)


if __name__ == "__main__":
    generate_all_questions()
