"""empty message

Revision ID: 4c33c5e0a6c8
Revises: e8552f721767
Create Date: 2024-01-05 13:23:26.771444

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4c33c5e0a6c8"
down_revision = "68c0b3386e44"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("assessment_start", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("assessment_start")
    # ### end Alembic commands ###
