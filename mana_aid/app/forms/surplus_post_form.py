from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import datetime, timedelta

class SurplusPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    food_type = SelectField('Food Type', choices=[
        ('Bakery', 'Bakery'),
        ('Dairy', 'Dairy'),
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Meat', 'Meat'),
        ('Grains', 'Grains'),
        ('Canned Goods', 'Canned Goods'),
        ('Frozen Foods', 'Frozen Foods'),
        ('Prepared Meals', 'Prepared Meals'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantity (servings)', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    expiry_time = DateTimeField('Expiry Time', format='%Y-%m-%dT%H:%M', 
                               default=datetime.utcnow() + timedelta(hours=24),
                               validators=[DataRequired()])
    pickup_location = StringField('Pickup Location', validators=[DataRequired(), Length(min=5, max=200)])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(min=10, max=15)])
    image_url = StringField('Image URL (optional)', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Post Surplus Food') 