from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class CreateTravelForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(1, 64, message='El nombre \
        debe tener un máximo de 64 letras.')])
    concept = SelectField('Concepto')
    country = SelectField('País')
    departure_date_minute = IntegerField('Minuto', validators=[DataRequired()])
    departure_date_hour = IntegerField('Hora', validators=[DataRequired()])
    departure_date_day = IntegerField('Día', validators=[DataRequired()])
    departure_date_month = IntegerField('Mes', validators=[DataRequired()])
    departure_date_year = IntegerField('Año', validators=[DataRequired()])
    duration = IntegerField('Duración (Días)',
                            validators=[DataRequired(message='La duración debe ser mayor que 0.'),
                                        NumberRange(min=0,
                                                    message='La duración debe ser mayor que 0.')])
    submit = SubmitField('Crear')


class CommentForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Comentar')
