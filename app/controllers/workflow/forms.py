from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Length


class CreateForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    submit = SubmitField('Crear')


class EditForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    submit = SubmitField('Editar')


class InsertForm(FlaskForm):
    state = SelectField('Estado')
    submit = SubmitField('Insertar')
