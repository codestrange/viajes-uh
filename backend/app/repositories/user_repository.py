from flask import current_app
from . import Repository, query_decorator
from ..entities.user_entity import UserEntity


class UserRepository(Repository):

    def add(self, entity):
        current_app.db.session.add(entity)

    def delete(self, entity):
        current_app.db.session.delete(entity)

    @query_decorator
    def query(self):
        return current_app.db.session.query(UserEntity).all()
