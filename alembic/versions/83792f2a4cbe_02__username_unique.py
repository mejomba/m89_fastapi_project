"""02_ username unique

Revision ID: 83792f2a4cbe
Revises: 2b9b4488581f
Create Date: 2023-03-13 19:28:54.399389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83792f2a4cbe'
down_revision = '2b9b4488581f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
