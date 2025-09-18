from flask_wtf import FlaskForm
from wtforms import TextAreaField, DateTimeField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime, timedelta

class FoodRequestForm(FlaskForm):
    message = TextAreaField('Message to Donor', validators=[DataRequired(), Length(min=10, max=500)])
    preferred_pickup_time = DateTimeField('Preferred Pickup Time', format='%Y-%m-%dT%H:%M',
                                         default=datetime.utcnow() + timedelta(hours=2),
                                         validators=[DataRequired()])
    delivery_address = StringField('Delivery Address (if delivery preferred)', 
                                  validators=[Optional(), Length(min=5, max=200)])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(min=10, max=15)])
    delivery_preference = SelectField('Delivery Preference', choices=[
        ('pickup', 'I will pick up'),
        ('delivery', 'Please deliver'),
        ('either', 'Either is fine')
    ], validators=[DataRequired()])
    submit = SubmitField('Request Food') 