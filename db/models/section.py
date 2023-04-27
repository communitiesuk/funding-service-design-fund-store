from db import db
from flask_sqlalchemy import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import LtreeType

BaseModel: DefaultMeta = db.Model


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
