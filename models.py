from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from datetime import datetime

db = SQLAlchemy()


class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    sale_price = db.Column(db.Float, default=0.0)
    auction_start_price = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(200), default='GEL')
    active = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Lot %r>' % self.id


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    start_date = db.Column(db.DateTime, default=datetime.now())
    end_date = db.Column(db.DateTime, default=datetime.now())
    active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Auction %r>' % self.id


class AuctionLots(db.Model):
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('auction_id', 'lot_id'),
    )


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    user = db.Column(db.String(200), nullable=True)


class LotsCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<LotsCategories %r>' % self.id


class LotCategory(db.Model):
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('lots_categories.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('lot_id', 'category_id'),
    )
