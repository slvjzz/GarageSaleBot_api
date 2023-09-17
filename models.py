from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)  # VARCHAR(MAX)
    sale_price = db.Column(db.Integer, default=0)
    auction_start_price = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Lot %r>' % self.id


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    start_date = db.Column(db.DateTime, default=datetime.utcnow())
    end_date = db.Column(db.DateTime, default=datetime.utcnow())
    active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Auction %r>' % self.id


class LotsCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<LotsCategories %r>' % self.id
