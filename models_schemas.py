from marshmallow import Schema, fields


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
