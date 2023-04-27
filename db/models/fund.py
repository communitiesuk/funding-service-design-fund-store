import uuid

from db import db
from flask_sqlalchemy import DefaultMeta
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


BaseModel: DefaultMeta = db.Model


class Fund(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    name = Column("name", db.String(), nullable=False, unique=False)
    title = Column("title", db.String(), nullable=False, unique=False)
    short_name = Column("short_name", db.String(), nullable=False, unique=True)
    description = Column(
        "description", db.String(), nullable=False, unique=False
    )
