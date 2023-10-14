from marshmallow import Schema, fields, post_dump
from datetime import datetime
from models import Auction, AuctionLots, Bid


class LotsCategoriesSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class LotSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    sale_price = fields.Float()
    auction_start_price = fields.Float()
    currency = fields.Str()
    auction_id = fields.Int()

    def get_auction_id(self, lot_id):
        current_datetime = datetime.now()

        auction = Auction.query\
            .join(AuctionLots, Auction.id == AuctionLots.auction_id)\
            .filter(AuctionLots.lot_id == lot_id, Auction.start_date < current_datetime)\
            .order_by(Auction.end_date.asc()).first()

        return auction if auction else None

    def get_max_bid_amount(self, lot_id):
        max_bid = Bid.query \
            .filter_by(lot_id=lot_id) \
            .order_by(Bid.amount.desc()) \
            .first()

        return max_bid.amount if max_bid else None

    def get_chat_id(self, lot_id):
        max_bid = Bid.query \
            .filter_by(lot_id=lot_id) \
            .order_by(Bid.amount.desc()) \
            .first()

        return max_bid.chat_id if max_bid else None

    @post_dump
    def add_auction_id_field(self, data, **kwargs):
        lot_id = data.get('id')
        auction = self.get_auction_id(lot_id)
        max_bid_amount = self.get_max_bid_amount(lot_id)
        chat_id = self.get_chat_id(lot_id)

        if auction is not None:
            data['auction_id'] = auction.id
            data['auction_end_date'] = auction.end_date
            data['max_bid_amount'] = max_bid_amount
            data['chat_id'] = chat_id
        else:
            data['auction_id'] = None
            data['auction_end_date'] = None
            data['max_bid_amount'] = None
            data['chat_id'] = None
        return data