from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import PhysicalAsset, DigitalAsset, Debt
from app.utils.file_handler import save_image
import os

bp = Blueprint('assets', __name__, url_prefix='/assets')


# Physical Assets Routes
@bp.route('/physical')
@login_required
def physical_list():
    """List all physical assets"""
    assets = PhysicalAsset.query.filter_by(user_id=current_user.id).all()
    return render_template('assets/physical_list.html', assets=assets)


@bp.route('/physical/add', methods=['GET', 'POST'])
@login_required
def physical_add():
    """Add new physical asset"""
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        location = request.form.get('location')
        purchase_price = request.form.get('purchase_price')
        notes = request.form.get('notes')

        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                image_path = save_image(file, current_user.id)

        asset = PhysicalAsset(
            user_id=current_user.id,
            name=name,
            category=category,
            location=location,
            purchase_price=float(purchase_price) if purchase_price else None,
            notes=notes,
            image_path=image_path
        )

        db.session.add(asset)
        db.session.commit()

        flash('Physical asset added successfully!', 'success')
        return redirect(url_for('assets.physical_list'))

    return render_template('assets/physical_form.html')


@bp.route('/physical/<int:asset_id>')
@login_required
def physical_detail(asset_id):
    """View physical asset details"""
    asset = PhysicalAsset.query.filter_by(id=asset_id, user_id=current_user.id).first_or_404()
    return render_template('assets/physical_detail.html', asset=asset)


@bp.route('/physical/<int:asset_id>/edit', methods=['GET', 'POST'])
@login_required
def physical_edit(asset_id):
    """Edit physical asset"""
    asset = PhysicalAsset.query.filter_by(id=asset_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        asset.name = request.form.get('name')
        asset.category = request.form.get('category')
        asset.location = request.form.get('location')
        asset.purchase_price = float(request.form.get('purchase_price')) if request.form.get('purchase_price') else None
        asset.notes = request.form.get('notes')
        asset.status = request.form.get('status', 'active')

        # Handle new image upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                image_path = save_image(file, current_user.id)
                asset.image_path = image_path

        db.session.commit()
        flash('Physical asset updated successfully!', 'success')
        return redirect(url_for('assets.physical_detail', asset_id=asset.id))

    return render_template('assets/physical_form.html', asset=asset, edit=True)


@bp.route('/physical/<int:asset_id>/delete', methods=['POST'])
@login_required
def physical_delete(asset_id):
    """Delete physical asset"""
    asset = PhysicalAsset.query.filter_by(id=asset_id, user_id=current_user.id).first_or_404()
    db.session.delete(asset)
    db.session.commit()
    flash('Physical asset deleted successfully!', 'success')
    return redirect(url_for('assets.physical_list'))


# Digital Assets Routes
@bp.route('/digital')
@login_required
def digital_list():
    """List all digital assets"""
    assets = DigitalAsset.query.filter_by(user_id=current_user.id).all()
    return render_template('assets/digital_list.html', assets=assets)


@bp.route('/digital/add', methods=['GET', 'POST'])
@login_required
def digital_add():
    """Add new digital asset"""
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        platform = request.form.get('platform')
        license_key = request.form.get('license_key')
        purchase_price = request.form.get('purchase_price')
        notes = request.form.get('notes')

        asset = DigitalAsset(
            user_id=current_user.id,
            name=name,
            category=category,
            platform=platform,
            license_key=license_key,
            purchase_price=float(purchase_price) if purchase_price else None,
            notes=notes
        )

        db.session.add(asset)
        db.session.commit()

        flash('Digital asset added successfully!', 'success')
        return redirect(url_for('assets.digital_list'))

    return render_template('assets/digital_form.html')


# Debts Routes
@bp.route('/debts')
@login_required
def debt_list():
    """List all debts"""
    debts = Debt.query.filter_by(user_id=current_user.id).all()
    return render_template('assets/debt_list.html', debts=debts)


@bp.route('/debts/add', methods=['GET', 'POST'])
@login_required
def debt_add():
    """Add new debt"""
    if request.method == 'POST':
        from datetime import datetime

        person_name = request.form.get('person_name')
        amount = request.form.get('amount')
        debt_type = request.form.get('type')
        date_str = request.form.get('date')
        notes = request.form.get('notes')

        debt = Debt(
            user_id=current_user.id,
            person_name=person_name,
            amount=float(amount),
            type=debt_type,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            notes=notes
        )

        db.session.add(debt)
        db.session.commit()

        flash('Debt record added successfully!', 'success')
        return redirect(url_for('assets.debt_list'))

    return render_template('assets/debt_form.html')


# Search API
@bp.route('/search')
@login_required
def search():
    """Search across all assets"""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'results': []})

    # Search in physical assets
    physical = PhysicalAsset.query.filter_by(user_id=current_user.id).filter(
        PhysicalAsset.name.ilike(f'%{query}%')
    ).all()

    # Search in digital assets
    digital = DigitalAsset.query.filter_by(user_id=current_user.id).filter(
        DigitalAsset.name.ilike(f'%{query}%')
    ).all()

    # Search in debts
    debts = Debt.query.filter_by(user_id=current_user.id).filter(
        Debt.person_name.ilike(f'%{query}%')
    ).all()

    results = {
        'physical': [asset.to_dict() for asset in physical],
        'digital': [asset.to_dict() for asset in digital],
        'debts': [debt.to_dict() for debt in debts]
    }

    return jsonify(results)
