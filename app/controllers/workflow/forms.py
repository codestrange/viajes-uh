from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class AppendWorkflowStateForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    role = SelectField('Rol')
    requirements = SelectMultipleField('Requerimientos')
    submit = SubmitField('Crear')


class CreateWorkflowStateForm(AppendWorkflowStateForm):
    next_node = SelectField('Siguiente Nodo')


class EditWorkflowStateForm(CreateWorkflowStateForm):
    submit = SubmitField('Guardar')
