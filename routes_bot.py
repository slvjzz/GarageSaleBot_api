import json
from flask import Blueprint, request, jsonify
from models import db, Lot, LotsCategories, LotCategory
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
    lots = Lot.query.filter(Lot.active == True).order_by(Lot.date_created).all()

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


@bp.route('/bot/lots/<int:id>/photos', methods=['GET'])
def get_lot_photos(id):
    print('get_photo')
    photos = []
    if os.path.exists(UPLOAD_FOLDER+f'/lot_{id}'):
        lst = os.listdir(UPLOAD_FOLDER+f'/lot_{id}')
        for i in lst:
            photos.append(str(UPLOAD_FOLDER+f'lot_{id}/'+i))
        print(photos)
    return jsonify(photos)


@bp.route('/bot/lots/<int:id>/buy', methods=['GET'])
def get_lot_buy(id):
    lot = Lot.query.get_or_404(id)
    lot.active = False
    db.session.commit()
    return jsonify({"ok": True})


@bp.route('/bot/categories/<int:category_id>', methods=['GET'])
def get_lots_by_category(category_id):
    lots = Lot.query.join(LotCategory).filter(LotCategory.category_id == category_id, Lot.active == True).all()

    schema = LotSchema(many=True)
    lot_data = schema.dump(lots)

    return jsonify(lot_data)

