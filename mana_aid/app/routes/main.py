from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import SurplusPost, FoodRequest, VolunteerTask, SponsorOrder

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page showing available food posts and statistics"""
    # Get recent available food posts
    available_posts = SurplusPost.query.filter_by(status='available').order_by(SurplusPost.created_at.desc()).limit(6).all()
    
    # Filter out expired posts
    available_posts = [post for post in available_posts if not post.is_expired]
    
    # Get some statistics
    total_posts = SurplusPost.query.count()
    total_requests = FoodRequest.query.count()
    total_volunteers = VolunteerTask.query.filter_by(status='completed').count()
    total_sponsored = SponsorOrder.query.filter_by(status='completed').count()
    
    return render_template('main/index.html', 
                         available_posts=available_posts,
                         total_posts=total_posts,
                         total_requests=total_requests,
                         total_volunteers=total_volunteers,
                         total_sponsored=total_sponsored)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard redirect"""
    if current_user.role == 'donor':
        return redirect(url_for('donor.dashboard'))
    elif current_user.role == 'recipient':
        return redirect(url_for('recipient.dashboard'))
    elif current_user.role == 'volunteer':
        return redirect(url_for('volunteer.dashboard'))
    elif current_user.role == 'ngo':
        return redirect(url_for('ngo.dashboard'))
    else:
        return render_template('main/dashboard.html')

@main_bp.route('/browse')
def browse_food():
    """Public browse page for available food"""
    posts = SurplusPost.query.filter_by(status='available').order_by(SurplusPost.created_at.desc()).all()
    available_posts = [post for post in posts if not post.is_expired]
    return render_template('main/browse_food.html', posts=available_posts)
