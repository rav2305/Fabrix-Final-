from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff')  # 'admin' or 'staff'

    def is_admin(self):
        return self.role == 'admin'

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    selling_price = db.Column(db.Float, nullable=False, default=0.0)
    cost_price = db.Column(db.Float, nullable=False, default=0.0)  # Price for us (cost price)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'selling_price': self.selling_price,
            'cost_price': self.cost_price
        }

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=True)
    customer_phone = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    discount = db.Column(db.Float, nullable=False, default=0.0)
    final_amount = db.Column(db.Float, nullable=False, default=0.0)
    amount_paid = db.Column(db.Float, nullable=False, default=0.0)  # Amount actually paid
    payment_status = db.Column(db.String(20), nullable=False, default='Paid')  # 'Paid', 'Partial', 'Unpaid'
    payment_method = db.Column(db.String(50), nullable=False, default='Cash')  # Cash, Card, UPI, etc.
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade="all, delete-orphan")

    @property
    def outstanding_amount(self):
        return max(0.0, self.final_amount - self.amount_paid)

class InvoiceItem(db.Model):
    __tablename__ = 'invoice_items'
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)

class DealerPurchase(db.Model):
    __tablename__ = 'dealer_purchases'
    id = db.Column(db.Integer, primary_key=True)
    dealer_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    total_cost = db.Column(db.Float, nullable=False, default=0.0)
    amount_paid = db.Column(db.Float, nullable=False, default=0.0)
    payment_status = db.Column(db.String(20), nullable=False, default='Unpaid')  # 'Paid', 'Partial', 'Unpaid'
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def outstanding_amount(self):
        return max(0.0, self.total_cost - self.amount_paid)
