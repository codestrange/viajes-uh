from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash
from .entity import Entity
from .query import Query


class User(Entity):
    def __init__(self, username, email, password, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query().get(data['id'])

    @staticmethod
    def commit():
        current_app.db.session.commit()

    @staticmethod
    def add(entity):
        current_app.db.session.add(entity)

    @staticmethod
    def delete(entity):
        current_app.db.session.delete(entity)

    @staticmethod
    def query():
        return Query(current_app.db.session.query(User).all())

    def __repr__(self):
        return f'<{self.username}, {self.email}>'
