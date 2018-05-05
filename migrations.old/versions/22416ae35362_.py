"""empty message

Revision ID: 22416ae35362
Revises: 684985541c59
Create Date: 2018-05-04 02:33:27.581482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22416ae35362'
down_revision = '684985541c59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menu_meals', sa.Column('meal_id', sa.Integer(), nullable=True))
    op.add_column('menu_meals', sa.Column('menu_id', sa.Integer(), nullable=True))
    op.drop_constraint('menu_meals_id_fkey', 'menu_meals', type_='foreignkey')
    op.create_foreign_key(None, 'menu_meals', 'meals', ['meal_id'], ['id'])
    op.create_foreign_key(None, 'menu_meals', 'menus', ['menu_id'], ['id'])
    op.drop_column('menu_meals', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menu_meals', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'menu_meals', type_='foreignkey')
    op.drop_constraint(None, 'menu_meals', type_='foreignkey')
    op.create_foreign_key('menu_meals_id_fkey', 'menu_meals', 'meals', ['id'], ['id'])
    op.drop_column('menu_meals', 'menu_id')
    op.drop_column('menu_meals', 'meal_id')
    # ### end Alembic commands ###
