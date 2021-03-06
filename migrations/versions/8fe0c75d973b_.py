"""empty message

Revision ID: 8fe0c75d973b
Revises: 
Create Date: 2020-02-23 17:35:41.128952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fe0c75d973b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pembayaran_spp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('siswa_id', sa.Integer(), nullable=False),
    sa.Column('dibayarkan', sa.Boolean(), nullable=True),
    sa.Column('beasiswa', sa.Boolean(), nullable=True),
    sa.Column('uangspp_id', sa.Integer(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['siswa_id'], ['siswa.id'], ),
    sa.ForeignKeyConstraint(['uangspp_id'], ['uang_spp.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint(None, 'jadwal_mapel', type_='foreignkey')
    op.create_foreign_key(None, 'jadwal_mapel', 'guru', ['guru_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'jadwal_mapel', type_='foreignkey')
    op.create_foreign_key(None, 'jadwal_mapel', 'user', ['guru_id'], ['id'])
    op.drop_table('pembayaran_spp')
    # ### end Alembic commands ###
