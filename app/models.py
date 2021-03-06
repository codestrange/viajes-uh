from datetime import datetime
from json import load
from os.path import abspath, dirname, join
from flask_login import LoginManager, AnonymousUserMixin, UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
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

state_document_type_uploaded = db.Table('state_document_type_uploaded',
                                       db.Column('state_id', db.Integer,
                                                 db.ForeignKey('state.id'), primary_key=True),
                                       db.Column('document_type_id', db.Integer,
                                                 db.ForeignKey('document_type.id'), primary_key=True))

state_document_type_checked = db.Table('state_document_type_checked',
                                       db.Column('state_id', db.Integer,
                                                 db.ForeignKey('state.id'), primary_key=True),
                                       db.Column('document_type_id', db.Integer,
                                                 db.ForeignKey('document_type.id'), primary_key=True))

state_role = db.Table('state_role',
                      db.Column('state_id', db.Integer,
                                db.ForeignKey('state.id'), primary_key=True),
                      db.Column('role_id', db.Integer,
                                db.ForeignKey('role.id'), primary_key=True))

state_workflow = db.Table('state_workflow',
                          db.Column('state_id', db.Integer,
                                    db.ForeignKey('state.id'), primary_key=True),
                          db.Column('workflow_id', db.Integer,
                                    db.ForeignKey('workflow.id'), primary_key=True))


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='area', lazy='dynamic')
    ancestor_id = db.Column(db.Integer, db.ForeignKey('area.id'))

    def __init__(self, name=None, ancestor=None):
        self.name = name
        self.ancestor = ancestor

    @property
    def ancestor(self):
        return Area.query.get(self.ancestor_id) if self.ancestor_id is not None else None

    @ancestor.setter
    def ancestor(self, ancestor):
        self.ancestor_id = ancestor.id if ancestor is not None else None

    @property
    def descendants(self):
        return Area.query.filter(Area.ancestor_id == self.id).all()
    
    @staticmethod
    def insert():
        for area in Area.query.all():
            db.session.delete(area)
        db.session.commit()
        area = Area()
        area.name = 'General'
        db.session.add(area)
        db.session.commit()

    def contains(self, area):
        if self.id == area.id:
            return True
        sons = Area.query.filter_by(ancestor_id = self.id).all()
        for son in sons:
            if son.id == area.id or son.contains(area):
                return True
        return False

    def __repr__(self):
        return f'{self.name}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.user}: {self.text}'


class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    travels = db.relationship('Travel', backref='concept', lazy='dynamic')

    @staticmethod
    def insert():
        basedir = abspath(dirname(__file__))
        json = load(open(join(basedir, 'static/concepts.json')))
        for item in json:
            concept = Concept(name=item)
            db.session.add(concept)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
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
    confirmed = db.Column(db.Boolean, default=False, index=True)
    upload_by_node = db.Column(db.Boolean, default=False, index=True)
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_type.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'))
    type = db.Column(db.String(64), index=True)

    __mapper_args__ = {
        'polymorphic_on': type,
    }

    @staticmethod
    def insert():
        pass

    def __repr__(self):
        return f'Documento de tipo "{self.document_type}" del viaje "{self.travel}" \
            subido por el usuario "{self.user}"'


class TextDocument(Document):
    text = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity': 'text',
    }


class PDFDocument(Document):
    pdf_path = db.Column(db.String(256), unique=True, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pdf',
    }


class ImageDocument(Document):
    image_path = db.Column(db.String(256), unique=True, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'image',
    }


class OtherDocument(Document):
    path = db.Column(db.String(256), unique=True, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'other',
    }


class DocumentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    documents = db.relationship('Document', backref='document_type', lazy='dynamic')

    @staticmethod
    def insert():
        pass

    def __repr__(self):
        return f'{self.name}'


class Index(db.Model):
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    index = db.Column(db.Integer, primary_key=True)


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    workflow_employee_id = db.Column(db.Integer, db.ForeignKey('workflow.id'))
    workflow_student_id = db.Column(db.Integer, db.ForeignKey('workflow.id'))
    workflow_teacher_id = db.Column(db.Integer, db.ForeignKey('workflow.id'))
    countries = db.relationship('Country', backref='region', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', secondary=user_role, 
                            backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')
    states = db.relationship('State', secondary=state_role, 
                             backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')

    @staticmethod
    def insert():
        for role in Role.query.all():
            db.session.delete(role)
        db.session.commit()
        role = Role()
        role.name = 'Administrador'
        db.session.add(role)
        db.session.commit()
        role = Role()
        role.name = 'Especialista'
        db.session.add(role)
        db.session.commit()
        role = Role()
        role.name = 'Usuario'
        role.default = True
        db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return f'{self.name}'


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    travels = db.relationship('Travel', backref='state', lazy='dynamic')
    need_uploaded = db.relationship('DocumentType',
                                   secondary=state_document_type_uploaded,
                                   backref=db.backref('states_uploaded', lazy='dynamic'),
                                   lazy='dynamic')
    need_checked = db.relationship('DocumentType',
                                   secondary=state_document_type_checked,
                                   backref=db.backref('states_checked', lazy='dynamic'),
                                   lazy='dynamic')
    workflows = db.relationship('Index', foreign_keys=[Index.state_id], backref=db.backref('state', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def insert():
        pass

    def __repr__(self):
        return f'{self.name}'


class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    justification = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'))
    documents = db.relationship('Document', backref='travel', lazy='dynamic')
    comments = db.relationship('Comment', backref='travel', lazy='dynamic')
    accepted = db.Column(db.Boolean, default=False, index=True)
    rejected = db.Column(db.Boolean, default=False, index=True)
    cancelled = db.Column(db.Boolean, default=False, index=True)
    confirmed_in_state = db.Column(db.Boolean, default=False, index=True)

    @staticmethod
    def insert():
        pass

    def __repr__(self):
        return f'{self.name}'

    def log(self, text, user):
        comment = Comment()
        comment.text = text
        comment.user = user
        comment.travel = self
        db.session.add(comment)
        db.session.commit()

    def can_move(self):
        if not self.confirmed_in_state:
            return False
        reqs_uploaded = self.state.need_uploaded.all()
        reqs_checked = self.state.need_checked.all()
        for req in reqs_uploaded:
            for doc in self.documents.all():
                if doc.document_type_id == req.id and doc.confirmed and doc.upload_by_node:
                    break
            else:
                return False
        for req in reqs_checked:
            for doc in self.documents.all():
                if doc.document_type_id == req.id and doc.confirmed and not doc.upload_by_node:
                    break
            else:
                return False
        return True


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    category = db.Column(db.String(64), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, index=True)
    activated = db.Column(db.Boolean, default=True, index=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    travels = db.relationship('Travel', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    documents = db.relationship('Document', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        roles = Role.query.filter_by(default=True).all()
        for role in roles:
            role.users.append(self)
            db.session.add(role)

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
        if self.firstname and self.lastname:
            return f'{self.firstname} {self.lastname}'
        elif self.firstname:
            return self.firstname
        elif self.lastname:
            return self.lastname
        return self.username

    @property
    def is_specialist(self):
        return Role.query.filter_by(name='Especialista').first().id in (role.id for role in self.roles)

    @property
    def is_administrator(self):
        return Role.query.filter_by(name='Administrador').first().id in (role.id for role in self.roles)

    @staticmethod
    def insert():
        for user in User.query.all():
            db.session.delete(user)
        db.session.commit()
        user = User()
        user.username = 'admin'
        user.email = 'admin@gmail.com'
        user.password = '1234'
        user.category = 'student'
        user.confirmed = True
        role = Role.query.filter_by(name='Administrador').first()
        area = Area.query.filter_by(name='General').first()
        user.roles.append(role)
        user.area = area
        db.session.add(user)
        db.session.commit()

    def decisions(self):
        travels_to_decide = []
        for role in self.roles:
            for state in State.query.all():
                if not role.id in [r.id for r in state.roles.all()]:
                    continue
                for travel in Travel.query.filter_by(state_id=state.id).all():
                    if (self.area.contains(travel.user.area) and role.name != 'Usuario' \
                        or current_user.id == travel.user.id and role.name == 'Usuario') \
                        and not travel.accepted and not travel.rejected and not travel.cancelled:
                        travels_to_decide.append(travel)
        return travels_to_decide


    def rejected_documents(self):
        messages = [
            doc
            for doc in self.documents
            if not doc.confirmed and not doc.upload_by_node
        ]
        return messages
    

    def have_rejected(self):
        return any(self.rejected_documents())


    def have_decisions(self):
        return len(self.decisions()) > 0

    
    def __repr__(self):
        return self.fullname


class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    employee_regions = db.relationship('Region', backref='workflow_employee', lazy='dynamic', \
                                       primaryjoin=id == Region.workflow_employee_id)
    student_regions = db.relationship('Region', backref='workflow_student', lazy='dynamic', \
                                      primaryjoin=id == Region.workflow_student_id)
    teacher_regions = db.relationship('Region', backref='workflow_teacher', lazy='dynamic', \
                                      primaryjoin=id == Region.workflow_teacher_id)
    states = db.relationship('Index', foreign_keys=[Index.workflow_id], backref=db.backref('workflow', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    travels = db.relationship('Travel', backref='workflow', lazy='dynamic')

    @staticmethod
    def move(travel):
        workflow = travel.workflow
        states = [index.state for index in workflow.states.order_by(Index.index).all()]
        if travel.state is None:
            travel.state = states[0]
            for document in travel.documents:
                document.upload_by_node = False
            travel.confirmed_in_state = False
            db.session.add(travel)
            return True
        else:
            for i in range(len(states)):
                if states[i].id == travel.state.id: 
                    if i + 1 == len(states):
                        travel.accepted = True
                    else:
                        travel.state = states[i + 1]
                    for document in travel.documents:
                        document.upload_by_node = False
                    travel.confirmed_in_state = False
                    db.session.add(travel)
                    return True
        return False

    def insert_state(workflow, state, position):
        position = min(position if position > -1 else 0, len(workflow.states.all()))
        for index in workflow.states.filter(Index.index >= position).order_by(Index.index.desc()):
            index.index += 1
            db.session.add(index)
            db.session.commit()
        index = Index()
        index.workflow = workflow
        index.state = state
        index.index = position
        db.session.add(index)
        db.session.commit()
    
    def remove_state(workflow, position):
        position = min(position if position > -1 else 0, len(workflow.states.all()) - 1)
        index = workflow.states.filter(Index.index == position).first()
        db.session.delete(index)
        db.session.commit()
        for index in workflow.states.filter(Index.index >= position).order_by(Index.index).all():
            index.index -= 1
            db.session.add(index)
            db.session.commit()

    def __repr__(self):
        return self.name


class AnonymousUserModel(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUserModel


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
