"""delete status table

Revision ID: a9d8fd90c08a
Revises: cd72f0de2017
Create Date: 2023-03-11 19:53:39.863960

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a9d8fd90c08a'
down_revision = 'cd72f0de2017'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status',
    sa.Column('status_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('last_update', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('status_id', name='status_pkey')
    )
    # ### end Alembic commands ###
