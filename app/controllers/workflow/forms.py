from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AppendStateForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    role = SelectField('Rol')
    requirements = SelectMultipleField('Requerimientos')
    submit = SubmitField('Crear')


class CreateStateForm(AppendStateForm):
    next_node = SelectField('Siguiente Nodo')


class EditStateForm(CreateStateForm):
    submit = SubmitField('Guardar')
