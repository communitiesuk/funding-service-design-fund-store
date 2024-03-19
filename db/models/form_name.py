from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import JSON
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from db import db

BaseModel: DefaultMeta = db.Model


class FormName(BaseModel):
    section_id = Column(
        "section_id",
        Integer,
        ForeignKey("section.id"),
        nullable=False,
        primary_key=True,
    )
    form_name_json = Column(
        "form_name_json",
        JSON(none_as_null=True),
        nullable=False,
        unique=False,
    )
