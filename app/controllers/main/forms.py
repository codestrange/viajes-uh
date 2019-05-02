from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length


class CreateTravelForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64)])
    country = SelectField('País', validators=[DataRequired()])
    submit = SubmitField('Crear')


class UploadDocumentForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64)])
    file_document = FileField('Archivo', validators=[DataRequired()])
    travel = SelectField('Viaje', validators=[DataRequired()])
    type_document = SelectField('Tipo de Documento', validators=[DataRequired()])
    submit = SubmitField('Subir')
