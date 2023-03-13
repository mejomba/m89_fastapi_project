"""03_ remove comment title

Revision ID: a179c5a4b86b
Revises: 83792f2a4cbe
Create Date: 2023-03-14 03:05:28.882818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a179c5a4b86b'
down_revision = '83792f2a4cbe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
