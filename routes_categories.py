from flask import Blueprint, render_template, request, redirect

from models import db, LotsCategories, LotCategory

bp = Blueprint('categories', __name__)


@bp.route('/categories', methods=['GET'])
def categories():
    categories = LotsCategories.query.order_by(LotsCategories.id).all()
    return render_template('categories.html', categories=categories)


@bp.route('/categories/<int:id>/delete', methods=['GET'])
def delete(id):
    category_to_delete = LotsCategories.query.get_or_404(id)
    try:
        LotCategory.query.filter_by(category_id=id).delete()

        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect('/categories')

    except Exception as e:
        print(f'OOOPS... Category was not deleted \n{e}')
        return redirect('/categories')


@bp.route('/categories/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    category = LotsCategories.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/categories')
        except Exception as e:
            print(f'OOOPS... Category was not deleted \n{e}')
            return redirect('/categories')
    else:
        return render_template('categories_editor.html', category=category, action=f'/categories/{id}/update')


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
