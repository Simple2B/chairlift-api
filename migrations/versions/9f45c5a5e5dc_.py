"""empty message

Revision ID: 9f45c5a5e5dc
Revises: 
Create Date: 2022-10-19 15:06:29.339278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f45c5a5e5dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('firmwares',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=128), nullable=True),
    sa.Column('hardware', sa.String(length=256), nullable=True),
    sa.Column('hash', sa.String(length=256), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('bin', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('sensors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('upload_id', sa.Integer(), nullable=True),
    sa.Column('sensor_name', sa.String(length=128), nullable=True),
    sa.Column('sensor_location_x', sa.Float(), nullable=True),
    sa.Column('sensor_location_y', sa.Float(), nullable=True),
    sa.Column('config', sa.String(length=256), nullable=True),
    sa.Column('health', sa.String(length=256), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sensors_sensor_name'), 'sensors', ['sensor_name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('picture', sa.String(length=256), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('role', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('google_openid_key', sa.String(length=256), nullable=True),
    sa.Column('apple_openid_key', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('group_owner', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_owner'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('raw_datas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('upload_id', sa.Integer(), nullable=True),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('blob', sa.String(length=256), nullable=True),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.Column('parsed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('api_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('sensor_role', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('group_role', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('key_hash', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('group_invite_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('invite_code', sa.String(length=256), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=True),
    sa.Column('invitation_date', sa.DateTime(), nullable=True),
    sa.Column('group_role', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=False),
    sa.Column('sensor_role', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('invited_by_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['invited_by_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('sensor_datas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_id', sa.Integer(), nullable=True),
    sa.Column('sensor_id', sa.String(length=256), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('power_current', sa.Float(precision=3), nullable=True),
    sa.Column('power_voltage', sa.Float(precision=3), nullable=True),
    sa.Column('tmp_temp', sa.Float(precision=3), nullable=True),
    sa.Column('snodar_distance', sa.Float(precision=3), nullable=True),
    sa.Column('seosonal_snowfall', sa.Float(precision=3), nullable=True),
    sa.Column('seosonal_snowdepth', sa.Float(precision=3), nullable=True),
    sa.Column('new_snowfall', sa.Float(precision=3), nullable=True),
    sa.Column('doy_swe', sa.Float(precision=3), nullable=True),
    sa.Column('temp_swe', sa.Float(precision=3), nullable=True),
    sa.Column('health', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['data_id'], ['raw_datas.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('sensor_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('edit_roles', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('view_roles', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('share_roles', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('sensor_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('key_hash', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('sensor_role', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('group_role', sa.Enum('Admin', 'Owner', 'Client', 'NoneRole', name='role'), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('api_keys_domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key_id', sa.Integer(), nullable=True),
    sa.Column('domain', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['key_id'], ['api_keys.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_keys_domains')
    op.drop_table('user_groups')
    op.drop_table('sensor_keys')
    op.drop_table('sensor_groups')
    op.drop_table('sensor_datas')
    op.drop_table('group_invite_codes')
    op.drop_table('api_keys')
    op.drop_table('raw_datas')
    op.drop_table('groups')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_sensors_sensor_name'), table_name='sensors')
    op.drop_table('sensors')
    op.drop_table('firmwares')
    # ### end Alembic commands ###
