from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    """Dashboard home page"""
    return render_template('index.html', user=current_user)


@bp.route('/health')
def health():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy'}), 200


@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard view"""
    from app.models import PhysicalAsset, DigitalAsset, Debt

    # Get counts for dashboard
    physical_count = PhysicalAsset.query.filter_by(user_id=current_user.id).count()
    digital_count = DigitalAsset.query.filter_by(user_id=current_user.id).count()
    debt_count = Debt.query.filter_by(user_id=current_user.id, status='unpaid').count()

    stats = {
        'physical_assets': physical_count,
        'digital_assets': digital_count,
        'pending_debts': debt_count
    }

    return render_template('dashboard.html', stats=stats, user=current_user)
