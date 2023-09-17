from flask import Blueprint, render_template, request, redirect

from models import db, LotsCategories

bp = Blueprint('categories', __name__)


@bp.route('/categories', methods=['GET'])
def categories():
    categories = LotsCategories.query.order_by(LotsCategories.id).all()
    return render_template('categories.html', categories=categories)


@bp.route('/categories/<int:id>/delete', methods=['GET'])
def delete(id):
    return 'DELETE'


@bp.route('/categories/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    return 'UPDATE'


@bp.route('/categories/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        category_name = request.form['name']

        new_category = LotsCategories(name=category_name,)

        try:
            db.session.add(new_category)
            db.session.commit()

            return redirect('/categories')
        except Exception as e:
            return f'Ooops... \n{e}'
    return render_template('categories_editor.html', action='/categories/add')
