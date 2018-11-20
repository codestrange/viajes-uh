from sqlalchemy import MetaData, Table, Column, Integer, Unicode
from sqlalchemy.orm import sessionmaker, mapper
from ..entities.user_entity import UserEntity


class Database:
    def __init__(self, metadata=None, session=None):
        self.session = session
        self.metadata = metadata

    def init_app(self, app):
        if self.metadata is None:
            self.metadata = MetaData(app.config['DATABASE_URL'])

        user_table = Table('tf_user', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('username', Unicode(64), unique=True, nullable=False),
                           Column('email', Unicode(64), unique=True, nullable=False),
                           Column('password_hash', Unicode(128), nullable=False))

        mapper(UserEntity, user_table)

        self.metadata.create_all()

        if self.session is None:
            Session = sessionmaker()
            self.session = Session()

        app.db = self
