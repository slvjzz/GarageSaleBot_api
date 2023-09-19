import json
from flask import Blueprint, request, jsonify
from models import Lot, LotsCategories
from models_schemas import LotsCategoriesSchema, LotSchema
import os

bp = Blueprint('bot', __name__)
UPLOAD_FOLDER = "D:/GarageSale/uploaded_files/lots/"


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
    lots = Lot.query.order_by(Lot.date_created).all()

    schema = LotSchema(many=True)
    lot_data = schema.dump(lots)

    return jsonify(lot_data)


@bp.route('/bot/categories', methods=['GET'])
def get_lots_categories():
    categories = LotsCategories.query.order_by(LotsCategories.name).all()

    schema = LotsCategoriesSchema(many=True)
    categories_data = schema.dump(categories)

    return jsonify(categories_data)


@bp.route('/bot/lots/<int:lot_id>', methods=['GET'])
def get_lot(lot_id):
    lot = Lot.query.get_or_404(lot_id)

    schema = LotSchema(many=False)
    lot_data = schema.dump(lot)

    return jsonify(lot_data)
