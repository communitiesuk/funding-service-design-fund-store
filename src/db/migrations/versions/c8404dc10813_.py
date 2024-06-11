"""empty message

Revision ID: c8404dc10813
Revises: afc0d0e35053
Create Date: 2023-05-30 16:51:27.718110

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c8404dc10813"
down_revision = "afc0d0e35053"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("application_guidance", sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("application_guidance")

    # ### end Alembic commands ###