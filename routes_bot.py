from flask import Blueprint, request

bp = Blueprint('bot', __name__)


@bp.route('/bot', methods=['GET'])
def bot_home():
    if request.method == "POST":
        print(request.json)
    return {"ok": True}
