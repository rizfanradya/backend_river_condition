"""rev

Revision ID: 2f6bc123b8a1
Revises: 
Create Date: 2024-08-09 08:01:31.914855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f6bc123b8a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=300), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('master_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('location', sa.Text(), nullable=True),
    sa.Column('site_condition', sa.Enum('Bersih', 'Kotor'), nullable=True),
    sa.Column('rivera_condition', sa.Enum('Pasang', 'Surut'), nullable=True),
    sa.Column('riverb_condition', sa.Enum('Mengalir', 'Tidak Mengalir'), nullable=True),
    sa.Column('riverc_condition', sa.Enum('Cepat', 'Lambat'), nullable=True),
    sa.Column('riverd_condition', sa.Enum('Bau', 'Tidak Bau'), nullable=True),
    sa.Column('rivere_condition', sa.Enum('Hitam', 'Hijau', 'Jernih', 'Putih Susu'), nullable=True),
    sa.Column('weather_condition', sa.Enum('Berawan', 'Cerah', 'Hujan'), nullable=True),
    sa.Column('origin_filepath', sa.String(length=255), nullable=True),
    sa.Column('thumbnail_filepath', sa.String(length=255), nullable=True),
    sa.Column('upload_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_data_id'), 'master_data', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_master_data_id'), table_name='master_data')
    op.drop_table('master_data')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_role_id'), table_name='role')
    op.drop_table('role')
    # ### end Alembic commands ###