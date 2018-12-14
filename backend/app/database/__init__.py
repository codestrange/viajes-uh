from sqlalchemy import MetaData, Table, Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import sessionmaker, mapper, relation
from ..entities.user_entity import UserEntity
from ..entities.role_entity import RoleEntity
from ..entities.permission_entity import PermissionEntity


class Database:
    def __init__(self, metadata=None, session=None):
        self.session = session
        self.metadata = metadata

    def init_app(self, app):
        if self.metadata is None:
            self.metadata = MetaData(app.config['DATABASE_URL'])

        user_table = Table('user', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('username', Unicode(64), unique=True, nullable=False),
                           Column('email', Unicode(64), unique=True, nullable=False),
                           Column('password_hash', Unicode(128), nullable=False))

        role_table = Table('role', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', Unicode(64), unique=True, nullable=False))

        permission_table = Table('permission', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', Unicode(64), unique=True, nullable=False))

        user_role_table = Table('user_role', self.metadata,
                                Column('user_id', None, ForeignKey('user.id'), primary_key=True),
                                Column('role_id', None, ForeignKey('role.id'), primary_key=True))

        role_permission_table = Table('role_permission', self.metadata,
                                      Column('role_id', None, ForeignKey('role.id'), primary_key=True),
                                      Column('permission_id', None, ForeignKey('permission.id'), primary_key=True))

        mapper(UserEntity, user_table, properties=dict(
            roles = relation(RoleEntity, secondary=user_role_table)
        ))

        mapper(RoleEntity, role_table, properties=dict(
            users = relation(UserEntity, secondary=user_role_table),
            permissions = relation(PermissionEntity, secondary=role_permission_table)
        ))

        mapper(PermissionEntity, permission_table, properties=dict(
            roles=relation(RoleEntity, secondary=role_permission_table)
        ))

        self.metadata.create_all()

        if self.session is None:
            Session = sessionmaker()
            self.session = Session()

        app.db = self
