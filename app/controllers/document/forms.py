from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class UploadDocumentForm(FlaskForm):
    document_type = SelectField('Tipo de Documento')
    submit = SubmitField('Subir')


class UploadImageDocumentForm(UploadDocumentForm):
    file = FileField('Imagen', validators=[FileRequired(), FileAllowed(['jpg', 'png'], \
        'Solo imágenes ".jpg" o ".png"')])


class UploadOtherDocumentForm(UploadDocumentForm):
    file = FileField('Archivo', validators=[FileRequired()])


class UploadPDFDocumentForm(UploadDocumentForm):
    file = FileField('Documento PDF', validators=[FileRequired(), FileAllowed(['pdf'], \
        'Solo documentos ".pdf".')])


class UploadTextDocumentForm(UploadDocumentForm):
    text = TextAreaField('Texto', validators=[DataRequired()])


class EditDocumentForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    file_document = FileField('Archivo', validators=[FileRequired()])
    submit = SubmitField('Subir')


def get_upload_form(method):
    if method == 'image':
        return UploadImageDocumentForm()
    elif method == 'pdf':
        return UploadPDFDocumentForm()
    elif method == 'text':
        return UploadTextDocumentForm()
    return UploadOtherDocumentForm()
