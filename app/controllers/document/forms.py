from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class UploadDocumentForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
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
    submit = SubmitField('Editar')
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])


class EditImageDocumentForm(EditDocumentForm):
    file = FileField('Imagen', validators=[FileRequired(), FileAllowed(['jpg', 'png'], \
        'Solo imágenes ".jpg" o ".png"')])


class EditOtherDocumentForm(EditDocumentForm):
    file = FileField('Archivo', validators=[FileRequired()])


class EditPDFDocumentForm(EditDocumentForm):
    file = FileField('Documento PDF', validators=[FileRequired(), FileAllowed(['pdf'], \
        'Solo documentos ".pdf".')])


class EditTextDocumentForm(EditDocumentForm):
    text = TextAreaField('Texto', validators=[DataRequired()])


class EditAuthDocumentFrom(FlaskForm):
    document_type = SelectField('Tipo')
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])


class EditAuthImageDocumentForm(EditImageDocumentForm, EditAuthDocumentFrom):
    pass


class EditAuthOtherDocumentForm(EditOtherDocumentForm, EditAuthDocumentFrom):
    pass


class EditAuthPDFDocumentForm(EditPDFDocumentForm, EditAuthDocumentFrom):
    pass


class EditAuthTextDocumentForm(EditTextDocumentForm, EditAuthDocumentFrom):
    pass


def get_edit_form(method):
    if method == 'image':
        return EditImageDocumentForm()
    elif method == 'pdf':
        return EditPDFDocumentForm()
    elif method == 'text':
        return EditTextDocumentForm()
    return EditOtherDocumentForm()


def get_edit_auth_form(method):
    if method == 'image':
        return EditAuthImageDocumentForm()
    elif method == 'pdf':
        return EditAuthPDFDocumentForm()
    elif method == 'text':
        return EditAuthTextDocumentForm()
    return EditAuthOtherDocumentForm()


def get_upload_form(method):
    if method == 'image':
        return UploadImageDocumentForm()
    elif method == 'pdf':
        return UploadPDFDocumentForm()
    elif method == 'text':
        return UploadTextDocumentForm()
    return UploadOtherDocumentForm()
