"""empty message

Revision ID: eada7e01b1c2
Revises: afc0d0e35053
Create Date: 2023-05-31 15:18:39.533053

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "eada7e01b1c2"
down_revision = "afc0d0e35053"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("name_json", sa.JSON(none_as_null=True), nullable=False)
        )
        batch_op.add_column(
            sa.Column("title_json", sa.JSON(none_as_null=True), nullable=False)
        )
        batch_op.add_column(
            sa.Column("description_json", sa.JSON(none_as_null=True), nullable=False)
        )
        batch_op.drop_column("description")
        batch_op.drop_column("title")
        batch_op.drop_column("name")

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("title_json", sa.JSON(none_as_null=True), nullable=False)
        )
        batch_op.drop_column("title")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False)
        )
        batch_op.drop_column("title_json")

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False)
        )
        batch_op.add_column(
            sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False)
        )
        batch_op.add_column(
            sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=False)
        )
        batch_op.drop_column("description_json")
        batch_op.drop_column("title_json")
        batch_op.drop_column("name_json")

    # ### end Alembic commands ###
