from app import db
from datetime import datetime


class SurplusPost(db.Model):
	__tablename__ = 'surplus_post'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text, nullable=False)
	food_type = db.Column(db.String(100), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	expiry_time = db.Column(db.DateTime, nullable=False)
	pickup_location = db.Column(db.String(200), nullable=False)
	contact_phone = db.Column(db.String(20), nullable=False)
	image_url = db.Column(db.String(500))
	status = db.Column(db.String(20), default='available')  # available, claimed, completed, cancelled
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	# Foreign Keys
	donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	# Relationships
	donor = db.relationship('User', backref='surplus_posts')
	# Provide backref for FoodRequest.surplus_post used in FoodRequest.__repr__
	food_requests = db.relationship('FoodRequest', backref='surplus_post', cascade='all, delete-orphan')

	def __repr__(self):
		return f'<SurplusPost {self.title}>'

	@property
	def is_expired(self):
		if self.expiry_time is None:
			return False
		return self.expiry_time <= datetime.utcnow()

