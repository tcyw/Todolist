"""empty message

Revision ID: cfb365a4699e
Revises: d85c0acb012f
Create Date: 2020-03-13 22:58:05.639809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfb365a4699e'
down_revision = 'd85c0acb012f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('category_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'categories', ['category_id'], ['id'])
    op.drop_column('todos', 'catetory_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('catetory_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'todos', ['catetory_id'], ['id'])
    op.drop_column('todos', 'category_id')
    # ### end Alembic commands ###