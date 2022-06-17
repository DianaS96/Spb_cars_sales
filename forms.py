from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import EqualTo, NumberRange, DataRequired


class SelectAutoCharacteristics(FlaskForm):
    brand = SelectField('brand', choices=[], validators=[DataRequired("Wrong brand")])
    carcase = SelectField('carcase', choices=[], validators=[DataRequired("Wrong carcase")])
    year = IntegerField('year', validators=[DataRequired("Wrong year"), NumberRange(min=1990, max=2022)])
    engine_capacity = IntegerField('engine_capacity',
                                   validators=[DataRequired("Wrong capacity"), NumberRange(min=60, max=1000)])
    drive_unit = SelectField('drive_unit', choices=[], validators=[DataRequired("Wrong drive_unit")])
    transmission = SelectField('transmission', choices=[], validators=[DataRequired("Wrong transmission")])
    guarantee = IntegerField('guarantee', validators=[DataRequired("Wrong year"), NumberRange(min=2022)])
    submit = SubmitField('Check price')
