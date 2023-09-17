import json
from flask import Blueprint, request, jsonify
from models import Lot

bp = Blueprint('bot', __name__)
#TEST


@bp.route('/bot', methods=['GET'])
def bot_home():
    if request.method == "POST":
        print(request.json)
        resp = request.json
    else:
        resp = {"ok": True, 'home': 'home'}
        resp = json.dumps(resp)
    return resp


@bp.route('/bot/lots', methods=['GET'])
def get_lots():
    lot_dicts = {}
    lots = Lot.query.order_by(Lot.date_created).all()
    for lot in lots:
        lot_dicts[lot.id] = {
            'id': lot.id,
            'name': lot.name,
            'description': lot.description,
            'sale_price': lot.sale_price,
            'auction_start_price': lot.auction_start_price,
            'currency': lot.currency,
            'active': lot.active,
            'date_created': lot.date_created,
        }
    print(lot_dicts)
    return jsonify(lot_dicts)
