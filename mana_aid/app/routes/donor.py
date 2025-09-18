from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import SurplusPost, FoodRequest
from app.forms import SurplusPostForm
from app import db
from datetime import datetime

donor_bp = Blueprint('donor', __name__)

@donor_bp.route('/donor/dashboard')
@login_required
def dashboard():
    if current_user.role != 'donor':
        flash('Access denied. Donor role required.', 'error')
        return redirect(url_for('main.index'))
    
    # Get donor's posts
    posts = SurplusPost.query.filter_by(donor_id=current_user.id).order_by(SurplusPost.created_at.desc()).all()
    
    # Get pending requests for donor's posts
    pending_requests = FoodRequest.query.join(SurplusPost).filter(
        SurplusPost.donor_id == current_user.id,
        FoodRequest.status == 'pending'
    ).order_by(FoodRequest.created_at.desc()).all()
    
    return render_template('donor/dashboard.html', posts=posts, pending_requests=pending_requests)

@donor_bp.route('/donor/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.role != 'donor':
        flash('Access denied. Donor role required.', 'error')
        return redirect(url_for('main.index'))
    
    form = SurplusPostForm()
    if form.validate_on_submit():
        post = SurplusPost(
            title=form.title.data,
            description=form.description.data,
            food_type=form.food_type.data,
            quantity=form.quantity.data,
            expiry_time=form.expiry_time.data,
            pickup_location=form.pickup_location.data,
            contact_phone=form.contact_phone.data,
            image_url=form.image_url.data,
            donor_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Food post created successfully!', 'success')
        return redirect(url_for('donor.dashboard'))
    
    return render_template('donor/new_post.html', form=form)

@donor_bp.route('/donor/post/<int:post_id>')
@login_required
def view_post(post_id):
    if current_user.role != 'donor':
        flash('Access denied. Donor role required.', 'error')
        return redirect(url_for('main.index'))
    
    post = SurplusPost.query.get_or_404(post_id)
    if post.donor_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('donor.dashboard'))
    
    requests = FoodRequest.query.filter_by(surplus_post_id=post.id).order_by(FoodRequest.created_at.desc()).all()
    return render_template('donor/view_post.html', post=post, requests=requests)

@donor_bp.route('/donor/request/<int:request_id>/<action>')
@login_required
def handle_request(request_id, action):
    if current_user.role != 'donor':
        flash('Access denied. Donor role required.', 'error')
        return redirect(url_for('main.index'))
    
    food_request = FoodRequest.query.get_or_404(request_id)
    post = SurplusPost.query.get(food_request.surplus_post_id)
    
    if post.donor_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('donor.dashboard'))
    
    if action == 'approve':
        food_request.status = 'approved'
        post.status = 'claimed'
        flash('Request approved!', 'success')
    elif action == 'reject':
        food_request.status = 'rejected'
        flash('Request rejected.', 'info')
    else:
        flash('Invalid action.', 'error')
        return redirect(url_for('donor.view_post', post_id=post.id))
    
    db.session.commit()
    return redirect(url_for('donor.view_post', post_id=post.id)) 