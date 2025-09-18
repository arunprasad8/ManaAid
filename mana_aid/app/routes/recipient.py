from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import SurplusPost, FoodRequest
from app.forms import FoodRequestForm
from app import db
from datetime import datetime

recipient_bp = Blueprint('recipient', __name__)

@recipient_bp.route('/recipient/dashboard')
@login_required
def dashboard():
    if current_user.role != 'recipient':
        flash('Access denied. Recipient role required.', 'error')
        return redirect(url_for('main.index'))
    
    # Get recipient's requests
    requests = FoodRequest.query.filter_by(recipient_id=current_user.id).order_by(FoodRequest.created_at.desc()).all()
    
    return render_template('recipient/dashboard.html', requests=requests)

@recipient_bp.route('/recipient/browse')
@login_required
def browse_food():
    if current_user.role != 'recipient':
        flash('Access denied. Recipient role required.', 'error')
        return redirect(url_for('main.index'))
    
    # Get available food posts
    posts = SurplusPost.query.filter_by(status='available').order_by(SurplusPost.created_at.desc()).all()
    
    # Filter out expired posts
    available_posts = [post for post in posts if not post.is_expired]
    
    return render_template('recipient/browse_food.html', posts=available_posts)

@recipient_bp.route('/recipient/post/<int:post_id>')
@login_required
def view_post(post_id):
    if current_user.role != 'recipient':
        flash('Access denied. Recipient role required.', 'error')
        return redirect(url_for('main.index'))
    
    post = SurplusPost.query.get_or_404(post_id)
    
    # Check if user has already requested this post
    existing_request = FoodRequest.query.filter_by(
        recipient_id=current_user.id,
        surplus_post_id=post.id
    ).first()
    
    return render_template('recipient/view_post.html', post=post, existing_request=existing_request)

@recipient_bp.route('/recipient/request/<int:post_id>', methods=['GET', 'POST'])
@login_required
def request_food(post_id):
    if current_user.role != 'recipient':
        flash('Access denied. Recipient role required.', 'error')
        return redirect(url_for('main.index'))
    
    post = SurplusPost.query.get_or_404(post_id)
    
    # Check if post is available
    if post.status != 'available' or post.is_expired:
        flash('This food is no longer available.', 'error')
        return redirect(url_for('recipient.browse_food'))
    
    # Check if user has already requested this post
    existing_request = FoodRequest.query.filter_by(
        recipient_id=current_user.id,
        surplus_post_id=post.id
    ).first()
    
    if existing_request:
        flash('You have already requested this food.', 'info')
        return redirect(url_for('recipient.view_post', post_id=post.id))
    
    form = FoodRequestForm()
    if form.validate_on_submit():
        food_request = FoodRequest(
            message=form.message.data,
            preferred_pickup_time=form.preferred_pickup_time.data,
            delivery_address=form.delivery_address.data,
            contact_phone=form.contact_phone.data,
            delivery_preference=form.delivery_preference.data,
            recipient_id=current_user.id,
            surplus_post_id=post.id
        )
        db.session.add(food_request)
        db.session.commit()
        flash('Food request submitted successfully!', 'success')
        return redirect(url_for('recipient.dashboard'))
    
    return render_template('recipient/request_food.html', form=form, post=post)

@recipient_bp.route('/recipient/request/<int:request_id>/cancel')
@login_required
def cancel_request(request_id):
    if current_user.role != 'recipient':
        flash('Access denied. Recipient role required.', 'error')
        return redirect(url_for('main.index'))
    
    food_request = FoodRequest.query.get_or_404(request_id)
    
    if food_request.recipient_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('recipient.dashboard'))
    
    if food_request.status != 'pending':
        flash('Cannot cancel a request that has already been processed.', 'error')
        return redirect(url_for('recipient.dashboard'))
    
    db.session.delete(food_request)
    db.session.commit()
    flash('Request cancelled successfully.', 'success')
    return redirect(url_for('recipient.dashboard')) 