"""empty message

Revision ID: 68bf0fb0ca89
Revises: 4d727593ca1f
Create Date: 2021-02-21 00:14:51.765738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68bf0fb0ca89'
down_revision = '4d727593ca1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('image_link', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'image_link')
    # ### end Alembic commands ###
