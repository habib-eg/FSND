"""empty message

Revision ID: 4d727593ca1f
Revises: 90d4e0345858
Create Date: 2021-02-20 23:01:26.167903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d727593ca1f'
down_revision = '90d4e0345858'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('image_link', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('image_link', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'image_link')
    op.drop_column('Show', 'image_link')
    # ### end Alembic commands ###