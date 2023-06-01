import contextlib
from operator import itemgetter

from db.models.section import Section
from db.models.section import SectionField
from marshmallow import post_dump
from marshmallow.fields import Method
from marshmallow.fields import String
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested


class SectionFieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SectionField

    field_id = auto_field()
    display_order = auto_field()

    def get_display_type(self, obj):
        return obj.field.display_type

    def get_field_type(self, obj):
        return obj.field.field_type

    display_type = Method("get_display_type")
    field_type = Method("get_field_type")


class SectionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Section

    def get_form_name(self, obj):
        raise NotImplementedError

    def get_title(
        self,
        obj,
    ):
        raise NotImplementedError

    def get_weighting(self, obj):
        return obj.weighting if obj.weighting else None

    path = String()
    fields = Nested("SectionFieldSchema", many=True, allow_none=True)
    weighting = Method("get_weighting")


class EnglishSectionSchema(SectionSchema):
    def get_form_name(self, obj):
        with contextlib.suppress(ValueError):
            (form_name_container,) = obj.form_name
            return form_name_container.form_name_json["en"]

    def get_title(
        self,
        obj,
    ):
        return obj.title_json.get("en")

    def sort_children(self, data):
        if data.get("children"):
            sorted_children = sorted(data["children"], key=itemgetter("path"))
            data["children"] = sorted_children
        return data

    @post_dump
    def sort_children_post_dump(self, data, **kwargs):
        return self.sort_children(data)

    children = Nested("EnglishSectionSchema", many=True, allow_none=True)
    form_name = Method("get_form_name")
    title = Method("get_title")


class WelshSectionSchema(SectionSchema):
    def get_form_name(self, obj):
        with contextlib.suppress(ValueError):
            (form_name_container,) = obj.form_name
            return form_name_container.form_name_json["cy"]

    def get_title(
        self,
        obj,
    ):
        return obj.title_json.get("cy")

    def sort_children(self, data):
        if data.get("children"):
            sorted_children = sorted(data["children"], key=itemgetter("path"))
            data["children"] = sorted_children
        return data

    @post_dump
    def sort_children_post_dump(self, data, **kwargs):
        return self.sort_children(data)

    children = Nested("WelshSectionSchema", many=True, allow_none=True)
    form_name = Method("get_form_name")
    title = Method("get_title")


SECTION_SCHEMA_MAP = {
    "en": EnglishSectionSchema,
    "cy": WelshSectionSchema,
}
