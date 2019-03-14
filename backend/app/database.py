from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()

user_role = db.Table('user_role',
                     db.Column('user_id',
                               db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id',
                               db.Integer, db.ForeignKey('role.id'), primary_key=True))

role_perm = db.Table('role_permission',
                     db.Column('role_id',
                               db.Integer, db.ForeignKey('role.id'), primary_key=True),
                     db.Column('permission_id',
                               db.Integer, db.ForeignKey('permission.id'), primary_key=True))

travel_inst = db.Table('travel_institution',
                       db.Column('travel_id',
                                 db.Integer, db.ForeignKey('travel.id'), primary_key=True),
                       db.Column('institution_id',
                                 db.Integer, db.ForeignKey('institution.id'), primary_key=True))

workf_trans = db.Table('workflow_transition',
                       db.Column('workflow_id',
                                 db.Integer, db.ForeignKey('workflow.id'), primary_key=True),
                       db.Column('transition_id',
                                 db.Integer, db.ForeignKey('transition.id'), primary_key=True))


class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    fullname = db.Column(db.String(256))

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)

    students = db.relationship('Student', backref='career')

    def __repr__(self):
        return f'{self.name}'


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    institutions = db.relationship('Institution', backref='city')

    def __repr__(self):
        return f'{self.name}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)

    cities = db.relationship('City', backref='country')

    def __repr__(self):
        return f'{self.name}'


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    fullname = db.Column(db.String(256))

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)

    teachers = db.relationship('Teacher', backref='department')

    def __repr__(self):
        return f'{self.name}'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    fullname = db.Column(db.String(256))

    departaments = db.relationship('Department', backref='faculty')
    careers = db.relationship('Career', backref='faculty')

    def __repr__(self):
        return f'{self.name}'


class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=role_perm, backref='permissions')

    def __repr__(self):
        return f'{self.name}'


class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    processes = db.relationship('Process', backref='procedure')

    def __repr__(self):
        return f'{self.name}'


class Process(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(32), nullable=False)

    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'), primary_key=True)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'), primary_key=True)

    def __repr__(self):
        return f'{self.id}'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_role, backref='roles')

    def __repr__(self):
        return f'{self.name}'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('career.id'), nullable=False)

    def __repr__(self):
        return f'{self.user.username}'


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    def __repr__(self):
        return f'{self.user.username}'


class Transition(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    procedure_start_id = db.Column(db.Integer, db.ForeignKey('procedure.id'), nullable=False)
    procedure_end_id = db.Column(db.Integer, db.ForeignKey('procedure.id'), nullable=False)
    procedure_start = db.relationship('Procedure', backref='transitions_start', primaryjoin='Procedure.id==Transition.procedure_start_id')
    procedure_end = db.relationship('Procedure', backref='transitions_end', primaryjoin='Procedure.id==Transition.procedure_end_id')

    def __repr__(self):
        return f'{self.procedure_start} -> {self.procedure_end}'


class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    institutions = db.relationship('Institution', secondary=travel_inst, backref='travels')

    processes = db.relationship('Process', backref='travel')

    def __repr__(self):
        return f'{self.id}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(256))
    lastname = db.Column(db.String(256))

    student = db.relationship('Student', backref='user', uselist=False)
    teacher = db.relationship('Teacher', backref='user', uselist=False)
    travels = db.relationship('Travel', backref='user')

    def __init__(self, username=None, email=None, password=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if password:
            self.password = password

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'{self.username}'


class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    countries = db.relationship('Country', backref='workflow')
    transitions = db.relationship('Transition', secondary=workf_trans, backref='workflows')

    def __repr__(self):
        return f'{self.id}'
