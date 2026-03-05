from app import db
from datetime import datetime


class PhysicalAsset(db.Model):
    """Model for physical assets (laptop, mobile, electronics, etc.)"""
    __tablename__ = 'physical_assets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)  # laptop, mobile, watch, etc.
    location = db.Column(db.String(200))  # Where is it stored/located
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    currency = db.Column(db.String(10), default='USD')
    image_path = db.Column(db.String(500))  # Path to image file
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')  # active, sold, lost, broken
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PhysicalAsset {self.name}>'

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'location': self.location,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'purchase_price': self.purchase_price,
            'currency': self.currency,
            'image_path': self.image_path,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class DigitalAsset(db.Model):
    """Model for digital assets (software, games, licenses, etc.)"""
    __tablename__ = 'digital_assets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)  # software, game, tool, etc.
    platform = db.Column(db.String(100))  # PS3, PS5, Windows, Mac, etc.
    license_key = db.Column(db.String(500))  # Software license key
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    currency = db.Column(db.String(10), default='USD')
    expiry_date = db.Column(db.Date)  # For subscriptions
    url = db.Column(db.String(500))  # Download or purchase URL
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')  # active, expired, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<DigitalAsset {self.name}>'

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'platform': self.platform,
            'license_key': self.license_key,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'purchase_price': self.purchase_price,
            'currency': self.currency,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'url': self.url,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Debt(db.Model):
    """Model for tracking borrowed and lent money"""
    __tablename__ = 'debts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    person_name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    type = db.Column(db.String(20), nullable=False, index=True)  # 'borrowed' or 'lent'
    date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='unpaid', index=True)  # paid, unpaid, partial
    paid_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Debt {self.person_name} - {self.amount} {self.currency}>'

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'person_name': self.person_name,
            'amount': self.amount,
            'currency': self.currency,
            'type': self.type,
            'date': self.date.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'paid_amount': self.paid_amount,
            'remaining_amount': self.amount - self.paid_amount,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
