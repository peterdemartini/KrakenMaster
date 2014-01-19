from flask_wtf import Form
from wtforms import TextField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, AnyOf

from .models import AlarmSetting

class AllSettings(Form):

    # Alarm Status Enabled or Disabled
    alarm_status = SelectField('Alarm Status', default='1',choices=[('0','Disabled'), ('1', 'Enabled')], validators=[DataRequired()])
    # Alarm Hours
    alarm_hours = SelectField('Alarm Hours', default='06', choices=[],
                    validators=[DataRequired()])
    # Alarm Minutes
    alarm_minutes = SelectField('Alarm Minutes', default='00', choices=[],
                    validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(AllSettings, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(AllSettings, self).validate()
        if not initial_validation:
            return False
        return True
