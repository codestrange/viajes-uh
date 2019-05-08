from flask_wtf import FlaskForm
from wtforms import FileField,  SelectField, StringField, SubmitField 
from wtforms.validators import DataRequired, Length


class UploadDocumentForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    file_document = FileField('Archivo', validators=[DataRequired()])
    travel = SelectField('Viaje')
    type_document = SelectField('Tipo de Documento')
    submit = SubmitField('Subir')
