from app import db
from datetime import datetime

class FoodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    preferred_pickup_time = db.Column(db.DateTime, nullable=False)
    delivery_address = db.Column(db.String(200))
    contact_phone = db.Column(db.String(20), nullable=False)
    delivery_preference = db.Column(db.String(20), nullable=False)  # pickup, delivery, either
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    surplus_post_id = db.Column(db.Integer, db.ForeignKey('surplus_post.id'), nullable=False)
    
    # Relationships
    recipient = db.relationship('User', backref='food_requests')
    
    def __repr__(self):
        return f'<FoodRequest {self.id} for {self.surplus_post.title}>'
    
    @property
    def is_urgent(self):
        # Check if pickup time is within 2 hours
        delta = self.preferred_pickup_time - datetime.utcnow()
        return delta.total_seconds() < 7200  # 2 hours in seconds 