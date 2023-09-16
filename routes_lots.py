from flask import Blueprint, render_template, request, redirect
from models import db, Lot, Auction
from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__)


def get_upload_folder(lot_pk, do_not_create=False):
    base_upload_folder = "D:/GarageSale/uploaded_files/lots/"
    lot_folder = os.path.join(base_upload_folder, f"lot_{lot_pk}")

    if not do_not_create:
        if not os.path.exists(lot_folder):
            os.makedirs(lot_folder)

    return lot_folder


@bp.route('/')
def index():
    return redirect('/lots')


@bp.route('/lots', methods=['GET', 'POST'])
def lots():
    lots = Lot.query.order_by(Lot.date_created).all()
    return render_template('lots.html', lots=lots)


@bp.route('/lots/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        temp_upload_folder = ''
        lot_name = request.form['name']
        lot_description = request.form['description']
        lot_auction_start_price = request.form['auction_start_price']
        lot_sale_price = request.form['sale_price']
        if request.form.get('active') == 'on':
            lot_active = True
        else:
            lot_active = False

        if 'images' in request.files:
            print('IMAAAGIESE\n', request.files)
            images = request.files.getlist('images')
            temp_identifier = secure_filename(lot_name)
            upload_path = get_upload_folder(temp_identifier)
            for image in images:
                if image.filename != '':
                    filename = secure_filename(image.filename)
                    temp_upload_folder = upload_path
                    image.save(os.path.join(upload_path, filename))

        new_lot = Lot(name=lot_name, description=lot_description, sale_price=lot_sale_price,
                      auction_start_price=lot_auction_start_price, active=lot_active)

        try:
            db.session.add(new_lot)
            db.session.commit()

            if 'image' in request.files:
                image = request.files['image']
                if image.filename != '':
                    lot_primary_key = new_lot.id
                    new_upload_folder = get_upload_folder(lot_primary_key, do_not_create=True)
                    os.rename(temp_upload_folder, new_upload_folder)

            return redirect('/lots')
        except Exception as e:
            return f'Ooops... \n{e}'
    else:
        return render_template('lot_editor.html', lot=None, action='/lots/add')


@bp.route('/lots/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    lot = Lot.query.get_or_404(id)

    if request.method == 'POST':
        print(request.form)
        lot.name = request.form['name']
        lot.description = request.form['description']
        lot.auction_start_price = request.form['auction_start_price']
        lot.sale_price = request.form['sale_price']
        if request.form.get('active') == 'on':
            lot.active = True
        else:
            lot.active = False

        if 'images' in request.files:
            print('IMAAAGIESE\n', request.files)
            images = request.files.getlist('images')
            upload_path = get_upload_folder(lot.id)
            for image in images:
                if image.filename != '':
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(upload_path, filename))
        try:
            db.session.commit()
            return redirect('/lots')
        except Exception as e:
            return f'Ooops... \n{e}'
    else:
        return render_template('lot_editor.html', lot=lot, action=f'/lots/update/{id}')


@bp.route('/lots/delete/<int:id>')
def delete(id):
    lot_to_delete = Lot.query.get_or_404(id)

    try:
        db.session.delete(lot_to_delete)
        db.session.commit()

        folder_to_delete = get_upload_folder(id, do_not_create=True)
        try:
            if os.path.exists(folder_to_delete):
                os.remove(folder_to_delete)
            else:
                print(f'No Folder for lot #{id}')
        except Exception as e:
            print(f'OOOPS... \n{e}\n\nFolder amd files were not deleted....')

        return redirect('/lots')
    except Exception as e:
        return f'OOOPS... {e}'


@bp.route('/about')
def about():
    return "ЭБАВАТ"
