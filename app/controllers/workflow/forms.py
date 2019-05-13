from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateStateForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    upload = SelectMultipleField('Documentos A Subir')
    review = SelectMultipleField('Documentos A Revisar')
    role = SelectMultipleField('Roles que revisan este nodo')
    submit = SubmitField('Crear')

class EditStateForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    upload = SelectMultipleField('Documentos A Subir')
    review = SelectMultipleField('Documentos A Revisar')
    role = SelectMultipleField('Roles que revisan este nodo')
    submit = SubmitField('Editar')
