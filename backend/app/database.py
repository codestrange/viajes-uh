from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy(session_options={"autoflush": False})

user_role = db.Table('user_role',
                     db.Column('user_id',
                               db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id',
                               db.Integer, db.ForeignKey('role.id'), primary_key=True))

workflowstate_type_document = db.Table('workflowstate_type_document',
                                       db.Column('workflowstate_id',
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
        return Area.query.filter(Area.ancestor_id==self.id).all()

    def __repr__(self):
        return f'{self.name}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    workflow_state_id = db.Column(db.Integer, db.ForeignKey('workflow_state.id'))
    travels = db.relationship('Travel', backref='country', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    path = db.Column(db.String(256), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False, index=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type_document.id'))
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'))

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

    def __repr__(self):
        return f'{self.name}'


class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    workflow_state_id = db.Column(db.Integer, db.ForeignKey('workflow_state.id'))
    documents = db.relationship('Document', backref='travel', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class TypeDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    documents = db.relationship('Document', backref='type', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    activated = db.Column(db.Boolean, default=True)
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
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'{self.username}'


class WorkflowState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    next_id = db.Column(db.Integer, db.ForeignKey('workflow_state.id'))
    travels = db.relationship('Travel', backref='workflowstate', lazy='dynamic')
    countries = db.relationship('Country', backref='workflowstate', lazy='dynamic')
    requirements = db.relationship('TypeDocument',
                                   secondary=workflowstate_type_document,
                                   backref=db.backref('workflowstates', lazy='dynamic'),
                                   lazy='dynamic')

    @property
    def next(self):
        return WorkflowState.query.get(self.next_id)

    @next.setter
    def next(self, next):
        self.next_id = next.id
    
    @property
    def previous(self):
        return WorkflowState.query.filter(WorkflowState.next_id==self.id).all()

    def __repr__(self):
        return f'{self.name}'
