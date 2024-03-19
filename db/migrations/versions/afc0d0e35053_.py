"""empty message

Revision ID: afc0d0e35053
Revises: f095a3913993
Create Date: 2023-05-25 12:56:46.068044

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "afc0d0e35053"
down_revision = "f095a3913993"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("feedback_link", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("project_name_field_id", sa.String(), nullable=True))
    op.execute(sa.text("Update round set project_name_field_id='KAgrBz';"))
    op.alter_column("round", "project_name_field_id", nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("project_name_field_id")
        batch_op.drop_column("feedback_link")

    # ### end Alembic commands ###
