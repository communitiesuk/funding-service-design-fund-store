"""empty message

Revision ID: 024379c68dfe
Revises: 108033941f74
Create Date: 2023-07-18 13:41:18.671549

"""
import sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "024379c68dfe"
down_revision = "108033941f74"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(sa.Column("guidance_url", sa.String(), nullable=True))

    connection = op.get_bind()
    nstf_guidance_url = "https://mhclg.sharepoint.com.mcas.ms/:w:/s/HomelessnessandRoughSleeping/EZn-Dq3eBvFDtdBqhyEZxUUBj_BP53F9TVyI0imX3NdcPw?e=PtmLwH"  # noqa
    cof_guidance_url = "https://mhclg.sharepoint.com.mcas.ms/:w:/s/CommunityOwnershipFund/Ecv3iM7U0AtKtyHnzRrQ9dsB0HdMPvHWqAoGn1WrWM7EMA?e=6QpdUT"  # noqa
    connection.execute(
        sqlalchemy.text(
            f"""
            UPDATE fund
            SET guidance_url = '{nstf_guidance_url}'
            WHERE short_name = 'NSTF'
            """
        )
    )

    connection.execute(
        sqlalchemy.text(
            f"""
            UPDATE fund
            SET guidance_url = '{cof_guidance_url}'
            WHERE short_name = 'COF'
            """
        )
    )

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column(
            "guidance_url", nullable=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.drop_column("guidance_url")

    # ### end Alembic commands ###