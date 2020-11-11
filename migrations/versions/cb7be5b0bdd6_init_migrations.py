"""init migrations

Revision ID: cb7be5b0bdd6
Revises: 
Create Date: 2020-11-11 18:47:53.059613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb7be5b0bdd6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'author',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.create_foreign_key(None, 'event', 'user', ['author'], ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.alter_column('event', 'author',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###