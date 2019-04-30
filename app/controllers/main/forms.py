from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class CreateTravelForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64)])
    country = SelectField('País', validators=[DataRequired()])
    submit = SubmitField('Crear')
