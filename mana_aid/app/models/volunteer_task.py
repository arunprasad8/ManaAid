from app import db
from datetime import datetime

class VolunteerTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(50), nullable=False)  # pickup, delivery, both
    pickup_location = db.Column(db.String(200), nullable=False)
    delivery_location = db.Column(db.String(200))
    status = db.Column(db.String(20), default='available')  # available, assigned, in_progress, completed, cancelled
    assigned_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    estimated_duration = db.Column(db.Integer)  # in minutes
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    surplus_post_id = db.Column(db.Integer, db.ForeignKey('surplus_post.id'))
    sponsor_order_id = db.Column(db.Integer, db.ForeignKey('sponsor_order.id'))
    
    # Relationships
    volunteer = db.relationship('User', backref='volunteer_tasks')
    surplus_post = db.relationship('SurplusPost', backref='volunteer_tasks')
    sponsor_order = db.relationship('SponsorOrder', backref='volunteer_tasks')
    
    def __repr__(self):
        return f'<VolunteerTask {self.id} - {self.task_type}>'
    
    @property
    def is_urgent(self):
        # Check if task is time-sensitive
        if self.surplus_post:
            return self.surplus_post.is_expired
        return False
    
    @property
    def duration_display(self):
        if self.estimated_duration:
            hours = self.estimated_duration // 60
            minutes = self.estimated_duration % 60
            if hours > 0:
                return f"{hours}h {minutes}m"
            return f"{minutes}m"
        return "Not specified" 