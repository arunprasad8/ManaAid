from app import db
from datetime import datetime

class SponsorOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    meal_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    target_recipients = db.Column(db.String(200))
    delivery_location = db.Column(db.String(200), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='planned')  # planned, in_progress, completed, cancelled
    budget = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Foreign Keys
    ngo_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    ngo = db.relationship('User', backref='sponsored_orders')
    
    def __repr__(self):
        return f'<SponsorOrder {self.title} by {self.ngo.username}>'
    
    @property
    def delivery_datetime(self):
        return datetime.combine(self.delivery_date, self.delivery_time)
    
    @property
    def is_urgent(self):
        # Check if delivery is within 24 hours
        delta = self.delivery_datetime - datetime.utcnow()
        return delta.total_seconds() < 86400  # 24 hours in seconds
    
    @property
    def budget_display(self):
        if self.budget:
            return f"${self.budget:.2f}"
        return "Not specified" 