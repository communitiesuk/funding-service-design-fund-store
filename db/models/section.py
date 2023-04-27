from db import db
from db import metadata
from flask_sqlalchemy import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import LtreeType


BaseModel: DefaultMeta = db.Model


section_field_table = Table(
    "section_field",
    metadata,
    Column("section_id", ForeignKey("section.id"), primary_key=True),
    Column("field_id", ForeignKey("assessment_field.id"), primary_key=True),
    Column("display_order", Integer, nullable=False, unique=False),
)


class AssessmentField(BaseModel):
    id = Column(db.String, primary_key=True, nullable=False, unique=True)
    field_type = Column(
        "field_type",
        db.String(),
        nullable=False,
        unique=False,
    )
    display_type = Column(
        "display_type", db.String(), nullable=False, unique=False
    )
    title = Column("title", db.String(), nullable=False, unique=False)
    sections = relationship(
        "Section", secondary=section_field_table, back_populates="fields"
    )


class Section(BaseModel):
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        nullable=False,
    )
    title = Column("title", db.String(), nullable=False, unique=False)
    round_id = Column(
        UUID(as_uuid=True),
        ForeignKey("round.id"),
        nullable=False,
    )
    weighting = Column(
        Integer,
        nullable=True,
    )
    path = Column(LtreeType, nullable=False)
    fields = relationship(
        "AssesmentField",
        secondary=section_field_table,
        back_populates="sections",
    )
