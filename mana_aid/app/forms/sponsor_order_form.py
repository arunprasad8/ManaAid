from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, TimeField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import date, time

class SponsorOrderForm(FlaskForm):
    title = StringField('Order Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    meal_type = SelectField('Meal Type', choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
        ('Mixed', 'Mixed Meals')
    ], validators=[DataRequired()])
    quantity = IntegerField('Number of Meals', validators=[DataRequired(), NumberRange(min=1, max=10000)])
    target_recipients = StringField('Target Recipients (e.g., Children, Elderly)', validators=[Optional(), Length(max=200)])
    delivery_location = StringField('Delivery Location', validators=[DataRequired(), Length(min=5, max=200)])
    delivery_date = DateField('Delivery Date', validators=[DataRequired()])
    delivery_time = TimeField('Delivery Time', validators=[DataRequired()])
    budget = FloatField('Budget (USD)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Create Sponsored Order') 