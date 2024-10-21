"""Add funding type to the fund table

Revision ID: de8d7954ffda
Revises: f5d2a21f372e
Create Date: 2024-10-17 08:18:08.965508

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "de8d7954ffda"
down_revision = "f5d2a21f372e"
branch_labels = None
depends_on = None

# it looks like alembic won't autogenerate the enum type with postgres, we can explicitly prompt it
# to create and drop during upgrade and downgrade
# https://github.com/sqlalchemy/alembic/issues/278
funding_type_enum = sa.Enum("COMPETITIVE", "UNCOMPETED", "EOI", name="fundingtype")


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # make sure we've got the type before using it in the new column
    funding_type_enum.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "funding_type",
                funding_type_enum,
                nullable=True,
            )
        )

    # all original funds will we competitive funds so default to this, this will be overriden
    # per environment
    op.get_bind().execute(
        sa.text(
            """
            UPDATE fund SET funding_type = 'COMPETITIVE'
            """
        )
    )

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column("funding_type", nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.drop_column("funding_type")

    funding_type_enum.drop(op.get_bind())
    # ### end Alembic commands ###