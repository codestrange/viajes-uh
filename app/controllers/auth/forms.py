from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField, \
    ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from ...models import User


class LoginForm(FlaskForm):
    user = StringField('Email o Nombre de Usuario', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Iniciar')


class RegistrationForm(FlaskForm):
    firstname = StringField('Nombre')
    lastname = StringField('Apellidos')
    username = StringField('Nombre de usuario',
                           validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Los nombres de usuario solo deben tener letras, \
                                              números, puntos o guiones bajos.')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64, message='El email \
        debe tener un máximo de 64 letras.'), Email()])
    password = PasswordField('Contraseña',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Las contraseñas deben coincidir.')])
    password2 = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    category = SelectField('Categoría')
    area = SelectField('Área')
    submit = SubmitField('Registrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('El email ya registrado.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('El nombre de usuario ya está en uso.')


class EditProfileForm(FlaskForm):
    firstname = StringField('Nombre')
    lastname = StringField('Apellidos')
    submit = SubmitField('Guardar')
