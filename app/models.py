from json import load
from os.path import abspath, dirname, join
from flask_login import LoginManager, AnonymousUserMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy(session_options={"autoflush": False})

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'

user_role = db.Table('user_role',
                     db.Column('user_id',
                               db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id',
                               db.Integer, db.ForeignKey('role.id'), primary_key=True))

workflow_state_type_document = db.Table('workflow_state_type_document',
                                       db.Column('workflow_state_id',
                                                 db.Integer,
                                                 db.ForeignKey('workflow_state.id'),
                                                 primary_key=True),
                                       db.Column('type_document_id',
                                                 db.Integer,
                                                 db.ForeignKey('type_document.id'),
                                                 primary_key=True))


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='area', lazy='dynamic')
    workflow_states = db.relationship('WorkflowState', backref='area', lazy='dynamic')
    ancestor_id = db.Column(db.Integer, db.ForeignKey('area.id'))

    @property
    def ancestor(self):
        return Area.query.get(self.ancestor_id)

    @ancestor.setter
    def ancestor(self, ancestor):
        self.ancestor_id = ancestor.id

    @property
    def descendants(self):
        return Area.query.filter(Area.ancestor_id == self.id).all()
    
    @staticmethod
    def insert():
        areas = []
        areas.append(Area(name='General'))
        areas.append(Area(name='MatCom', ancestor=areas[-1]))
        areas.append(Area(name='Cibernetica', ancestor=areas[-1]))
        areas.append(Area(name='Matematica', ancestor=areas[-2]))
        for item in areas:
            db.session.add(item)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    workflow_state_id = db.Column(db.Integer, db.ForeignKey('workflow_state.id'))
    travels = db.relationship('Travel', backref='country', lazy='dynamic')

    @staticmethod
    def insert():
        for country in Country.query.all():
            db.session.delete(country)
        for region in Region.query.all():
            db.session.delete(region)
        db.session.commit()
        basedir = abspath(dirname(__file__))
        json = load(open(join(basedir, 'static/country-by-region.json')))
        regions = {}
        for item in json:
            if item['region'] in regions:
                regions[item['region']].append(item['country'])
            else:
                regions[item['region']] = [item['country']]
        for region_name in regions:
            countries = regions[region_name]
            region = Region(name=region_name)
            db.session.add(region)
            for country_name in countries:
                country = Country(name=country_name)
                country.region = region
                db.session.add(country)
            db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    path = db.Column(db.String(256), unique=True, nullable=True)
    confirmed = db.Column(db.Boolean, default=False, index=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type_document.id'))
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'))

    @staticmethod
    def insert():
        type1 = TypeDocument.query.get(1)
        type2 = TypeDocument.query.get(2)
        document1 = Document(name='Documento 1', type_document=type1, travel=Travel.query.get(1))
        document2 = Document(name='Documento 2', type_document=type2, travel=Travel.query.get(1))
        document3 = Document(name='Documento 3', type_document=type1, travel=Travel.query.get(2))
        document4 = Document(name='Documento 4', type_document=type2, travel=Travel.query.get(2))
        db.session.add(document1)
        db.session.add(document2)
        db.session.add(document3)
        db.session.add(document4)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    countries = db.relationship('Country', backref='region', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', secondary=user_role, 
                            backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')
    workflow_states = db.relationship('WorkflowState', backref='role')

    @staticmethod
    def insert():
        roles = []
        viajero = Role(name='Viajero', default=True)
        estudiante = Role(name='Estudiante')
        profesor = Role(name='Profesor')
        decano = Role(name='Decano')
        especialista = Role(name='Especialista')
        db.session.add(viajero)
        db.session.add(estudiante)
        db.session.add(profesor)
        db.session.add(decano)
        db.session.add(especialista)
        db.session.commit()
        leynier = User.query.get(1)
        carlos = User.query.get(2)
        martinez = User.query.get(3)
        roberto = User.query.get(4)
        leynier.roles.append(estudiante)
        carlos.roles.append(profesor)
        martinez.roles.append(especialista)
        roberto.roles.append(decano)
        db.session.add(leynier)
        db.session.add(carlos)
        db.session.add(martinez)
        db.session.add(roberto)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    workflow_state_id = db.Column(db.Integer, db.ForeignKey('workflow_state.id'))
    documents = db.relationship('Document', backref='travel', lazy='dynamic')

    @staticmethod
    def insert():
        travel1 = Travel(name='Viaje uno')
        travel1.user = User.query.get(1)
        travel1.country = Country.query.get(41)
        travel1.workflow_state = WorkflowState.query.get(2)
        travel2 = Travel(name='Viaje dos')
        travel2.user = User.query.get(2)
        travel2.country = Country.query.get(25)
        travel2.workflow_state = WorkflowState.query.get(2)
        db.session.add(travel1)
        db.session.add(travel2)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class TypeDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    documents = db.relationship('Document', backref='type_document', lazy='dynamic')

    @staticmethod
    def insert():
        types = []
        types.append(TypeDocument(name='Visa'))
        types.append(TypeDocument(name='Pasaporte'))
        types.append(TypeDocument(name='Carta de Invitación'))
        types.append(TypeDocument(name='Otros'))
        for item in types:
            db.session.add(item)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False, index=True)
    activated = db.Column(db.Boolean, default=True, index=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    travels = db.relationship('Travel', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        roles = Role.query.filter_by(default=True).all()
        for role in roles:
            role.users.append(self)
            db.session.add(role)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('La contraseña no es un atributo legible.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    @staticmethod
    def insert():
        leynier = User(username='l.gutierrez', email='l.gutierrez@gmail.com', password='1234')
        carlos = User(username='c.bermudez', email='c.bermudez@gmail.com', password='1234')
        martinez = User(username='c.martinez', email='c.martinez@gmail.com', password='1234')
        roberto = User(username='r.marti', email='r.marti@gmail.com', password='1234')
        leynier.confirmed = carlos.confirmed = martinez.confirmed = roberto.confirmed = True
        general = Area.query.get(1)
        matcom = Area.query.get(2)
        computacion = Area.query.get(3)
        matematica = Area.query.get(4)
        leynier.area = computacion
        carlos.area = matematica
        martinez.area = general
        roberto.area = matcom
        db.session.add(leynier)
        db.session.add(carlos)
        db.session.add(martinez)
        db.session.add(roberto)
        db.session.commit()

    def have_decissions(self):
        return True

    def __repr__(self):
        return f'{self.username}'


class WorkflowState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    next_id = db.Column(db.Integer, db.ForeignKey('workflow_state.id'))
    travels = db.relationship('Travel', backref='workflow_state', lazy='dynamic')
    countries = db.relationship('Country', backref='workflow_state', lazy='dynamic')
    requirements = db.relationship('TypeDocument',
                                   secondary=workflow_state_type_document,
                                   backref=db.backref('workflow_states', lazy='dynamic'),
                                   lazy='dynamic')

    @property
    def next(self):
        return WorkflowState.query.get(self.next_id)

    @next.setter
    def next(self, next):
        self.next_id = next.id

    @property
    def previous(self):
        return WorkflowState.query.filter(WorkflowState.next_id == self.id).all()

    @staticmethod
    def insert():
        item0 = WorkflowState(name='Paso Dos')
        item0.role = Role.query.filter_by(name='Especialista').first()
        item0.requirements.append(TypeDocument.query.get(1))
        item1 = WorkflowState(name='Paso Uno')
        item1.role = Role.query.filter_by(name='Decano').first()
        item1.requirements.append(TypeDocument.query.get(2))
        item1.next = item0
        item1.countries.append(Country.query.get(41))
        item1.countries.append(Country.query.get(25))
        db.session.add(item0)
        db.session.add(item1)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class AnonymousUserModel(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUserModel


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
