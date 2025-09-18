from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class VolunteerTaskForm(FlaskForm):
    task_type = SelectField('Task Type', choices=[
        ('pickup', 'Pickup Only'),
        ('delivery', 'Delivery Only'),
        ('both', 'Pickup & Delivery')
    ], validators=[DataRequired()])
    pickup_location = StringField('Pickup Location', validators=[DataRequired(), Length(min=5, max=200)])
    delivery_location = StringField('Delivery Location', validators=[Optional(), Length(min=5, max=200)])
    estimated_duration = IntegerField('Estimated Duration (minutes)', validators=[Optional(), NumberRange(min=15, max=480)])
    notes = TextAreaField('Additional Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Create Task') 