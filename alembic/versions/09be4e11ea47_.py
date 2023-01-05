"""empty message

Revision ID: 09be4e11ea47
Revises: ef55efde2f55
Create Date: 2023-01-04 16:19:36.816993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09be4e11ea47'
down_revision = 'ef55efde2f55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('about',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_uz', sa.String(), nullable=True),
    sa.Column('image_en', sa.String(), nullable=True),
    sa.Column('image_ru', sa.String(), nullable=True),
    sa.Column('info_uz', sa.Text(), nullable=True),
    sa.Column('info_ru', sa.Text(), nullable=True),
    sa.Column('info_en', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', name='aboutstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('advantage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_uz', sa.String(), nullable=True),
    sa.Column('image_en', sa.String(), nullable=True),
    sa.Column('image_ru', sa.String(), nullable=True),
    sa.Column('info_uz', sa.Text(), nullable=True),
    sa.Column('info_ru', sa.Text(), nullable=True),
    sa.Column('info_en', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', name='advantagestatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('advantage')
    op.drop_table('about')
    # ### end Alembic commands ###