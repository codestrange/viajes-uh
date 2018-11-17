from sqlalchemy import MetaData, Table, Column, Integer, Unicode
from sqlalchemy.orm import sessionmaker, mapper
from ..models.user import User


class Database:
    def __init__(self, session=None):
        self.session = session

    def init_app(self, app):
        metadata = MetaData(app.config['DATABASE_URL'])

        user_table = Table('tf_user', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('username', Unicode(64), unique=True, nullable=False),
                           Column('email', Unicode(64), unique=True, nullable=False),
                           Column('password_hash', Unicode(128), nullable=False))

        mapper(User, user_table)

        metadata.create_all()

        Session = sessionmaker()
        self.session = Session()

        app.db = self
