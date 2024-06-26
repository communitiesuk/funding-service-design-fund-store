"""FS-4071: Add Boolean to determine whether we show email
or a link to the contact us page, differs per fund.

Revision ID: 8e4d1e36ebbf
Revises: e439c3fdea6d
Create Date: 2024-04-22 17:28:38.571656

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8e4d1e36ebbf"
down_revision = "e439c3fdea6d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("reference_contact_page_over_email", sa.Boolean(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
            UPDATE round
            SET reference_contact_page_over_email = FALSE
            """
        )
    )

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column(sa.Column("reference_contact_page_over_email", nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("reference_contact_page_over_email")

    # ### end Alembic commands ###
