from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()

user_role = db.Table('user_role',
                     db.Column('user_id',
                               db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id',
                               db.Integer, db.ForeignKey('role.id'), primary_key=True))

role_permission = db.Table('role_permission',
                           db.Column('role_id',
                                     db.Integer, db.ForeignKey('role.id'), primary_key=True),
                           db.Column('permission_id',
                                     db.Integer, db.ForeignKey('permission.id'), primary_key=True))


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=role_permission, backref='permissions')

    def __repr__(self):
        return f'{self.name}'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_role, backref='roles')

    def __repr__(self):
        return f'{self.name}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    activated = db.Column(db.Boolean, default=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'{self.username}'
