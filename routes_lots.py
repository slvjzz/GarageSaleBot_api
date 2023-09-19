from PIL import Image
from flask import Blueprint, render_template, request, redirect, send_from_directory
from models import db, Lot, LotsCategories, LotCategory
from werkzeug.utils import secure_filename
import os
import pillow_heif
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


bp = Blueprint('lots', __name__)
UPLOAD_FOLDER = config['files']['UPLOAD_FOLDER']

CURRENCIES = ["GEL", "USD"]


def heic_to_jpg(file, filename):
    filename = os.path.splitext(filename)[0] + '.JPEG'

    pillow_heif.register_heif_opener()
    img = Image.open(file)
    return img, filename


def is_image(file):
    file_extension = os.path.splitext(file.filename)[1].lower()
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic']
    print(file_extension)
    print(file.filename)
    print(file.filename.lower().endswith('.heic'))
    if file.filename.lower().endswith('.heic'):
        print('HEIC!!!!!')
        heif_file = pillow_heif.HeifFile(file)
        return True
    else:
        if file_extension in supported_extensions:
            return True
        return False


def get_upload_folder(lot_pk, do_not_create=False):
    lot_folder = os.path.join(UPLOAD_FOLDER, f"lot_{lot_pk}")

    if not do_not_create:
        if not os.path.exists(lot_folder):
            os.makedirs(lot_folder)

    return lot_folder


@bp.route('/uploads/<int:id>/<filename>')
def image_folder(id, filename):
    way = get_upload_folder(id, do_not_create=True)
    return send_from_directory(way, filename)


@bp.route('/lots', methods=['GET'])
def lots():
    lots = Lot.query.order_by(Lot.date_created).all()
    return render_template('lots.html', lots=lots)


@bp.route('/lots/add', methods=['GET', 'POST'])
def add():
    categories = LotsCategories.query.order_by(LotsCategories.id).all()
    if request.method == 'POST':
        assigned_categories = []
        upload_path = ''
        lot_name = request.form['name']
        lot_description = request.form['description']
        lot_auction_start_price = request.form['auction_start_price']
        lot_sale_price = request.form['sale_price']
        lot_currency = request.form['currency']
        if request.form.get('active') == 'on':
            lot_active = True
        else:
            lot_active = False

        for key in request.form:
            if key.startswith('category_'):
                category_id = int(key.replace('category_', ''))
                if 'on' in request.form.getlist(key):
                    assigned_categories.append(category_id)
        print(assigned_categories)

        if 'images' in request.files and any(image.filename for image in request.files.getlist('images')):
            print('IMAAAGIESE\n', request.files)
            images = request.files.getlist('images')
            if images[0].filename != '':
                temp_identifier = secure_filename(lot_name)
                upload_path = get_upload_folder(temp_identifier)
                for image in images:
                    if image.filename != '' and is_image(image):
                        filename = secure_filename(image.filename)
                        if filename.lower().endswith('.heic'):
                            try:
                                converted_file = heic_to_jpg(image, filename)
                                image = converted_file
                                image[0].save(os.path.join(upload_path, image[1]), format('JPEG'),
                                              quality=100,
                                              optimize=True,
                                              progressive=True)
                            except Exception as e:
                                print('Was not converted:\n', e)
                        else:
                            image.save(os.path.join(upload_path, filename))

        new_lot = Lot(name=lot_name, description=lot_description, sale_price=lot_sale_price,
                      auction_start_price=lot_auction_start_price, active=lot_active, currency=lot_currency)

        try:
            db.session.add(new_lot)
            db.session.commit()

            lot_id = new_lot.id

            for category_id in assigned_categories:
                lot_category = LotCategory.query.filter_by(lot_id=lot_id, category_id=category_id).first()
                if not lot_category:
                    auction_lot = LotCategory(lot_id=lot_id, category_id=category_id)
                    db.session.add(auction_lot)
            db.session.commit()

            if any(image.filename for image in request.files.getlist('images')):
                lot_primary_key = new_lot.id
                new_upload_folder = get_upload_folder(lot_primary_key, do_not_create=True)
                try:
                    os.rename(upload_path, new_upload_folder)
                except Exception as e:
                    print(f'Ooops... \n{e}\n\n Folder was not renamed...')

            return redirect('/lots')
        except Exception as e:
            return f'Ooops... \n{e}'
    else:
        return render_template('lot_editor.html', lot=None, action='/lots/add', currencies=CURRENCIES,
                               categories=categories)


@bp.route('/lots/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    categories = LotsCategories.query.order_by(LotsCategories.id).all()
    lot = Lot.query.get_or_404(id)
    image_folder = get_upload_folder(lot.id, do_not_create=True)
    image_filenames = []

    assigned_categories = []
    unassigned_categories = []

    if os.path.exists(image_folder):
        image_filenames = os.listdir(image_folder)

    print(image_filenames)

    if request.method == 'POST':
        print(request.form)
        lot.name = request.form['name']
        lot.description = request.form['description']
        lot.auction_start_price = request.form['auction_start_price']
        lot.sale_price = request.form['sale_price']
        lot.currency = request.form['currency']
        if request.form.get('active') == 'on':
            lot.active = True
        else:
            lot.active = False

        for key in request.form:
            if key.startswith('category_'):
                category_id = int(key.replace('category_', ''))
                if 'on' in request.form.getlist(key):
                    assigned_categories.append(category_id)

        for category in categories:
            if category.id not in assigned_categories:
                unassigned_categories.append(category.id)

        if 'images' in request.files and any(image.filename for image in request.files.getlist('images')):
            print('IMAAAGIESE\n', request.files)
            images = request.files.getlist('images')
            if len(images) > 0:
                upload_path = get_upload_folder(lot.id)
                for image in images:
                    if image.filename != '' and is_image(image):
                        filename = secure_filename(image.filename)
                        if filename.lower().endswith('.heic'):
                            try:
                                converted_file = heic_to_jpg(image, filename)
                                image = converted_file
                                image[0].save(os.path.join(upload_path, image[1]), format('JPEG'),
                                              quality=100,
                                              optimize=True,
                                              progressive=True)
                            except Exception as e:
                                print('Was not converted:\n', e)
                        else:
                            image.save(os.path.join(upload_path, filename))
        try:
            db.session.commit()

            for category_id in unassigned_categories:
                lot_category = LotCategory.query.filter_by(lot_id=id, category_id=category_id).first()
                if lot_category:
                    db.session.delete(lot_category)

            for category_id in assigned_categories:
                lot_category = LotCategory.query.filter_by(lot_id=id, category_id=category_id).first()
                if not lot_category:
                    lot_category = LotCategory(lot_id=id, category_id=category_id)
                    db.session.add(lot_category)

            db.session.commit()
            return redirect('/lots')
        except Exception as e:
            return f'Ooops... \n{e}'
    else:
        assigned_categories = []
        for category in categories:
            lot_category = LotCategory.query.filter_by(lot_id=id, category_id=category.id).first()
            if lot_category:
                assigned_categories.append(category.id)
        print('assigned categories:', assigned_categories)
        return render_template('lot_editor.html', lot=lot, action=f'/lots/update/{id}',
                               image_filenames=image_filenames, image_folder=image_folder, currencies=CURRENCIES,
                               categories=categories, assigned_categories=assigned_categories)


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
            redirect('/lots')

        return redirect('/lots')
    except Exception as e:
        return f'OOOPS... {e}'
