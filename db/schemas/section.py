from db.models.section import Section
from marshmallow.fields import String
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested


class SectionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Section

    children = Nested("SectionSchema", many=True, allow_none=True)
    path = String()
