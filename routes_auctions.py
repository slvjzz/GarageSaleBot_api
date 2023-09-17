from flask import Blueprint, render_template, request, redirect, send_from_directory
from models import db, Auction, Lot, AuctionLots
from datetime import datetime

bp = Blueprint('auctions', __name__)


@bp.route('/auctions', methods=['GET'])
def auctions():
    auctions = Auction.query.order_by(Auction.date_created).all()
    return render_template('auctions.html', auctions=auctions)


@bp.route('/auctions/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        auction_start_date_str = request.form['start_date']
        auction_end_date_str = request.form['end_date']
        checked_lots = []

        auction_name = request.form['name']
        auction_start_date = datetime.strptime(auction_start_date_str, '%Y-%m-%dT%H:%M')
        auction_end_date = datetime.strptime(auction_end_date_str, '%Y-%m-%dT%H:%M')
        if request.form.get('active') == 'on':
            auction_active = True
        else:
            auction_active = False

        for key in request.form:
            if key.startswith('lot_'):
                lot_id = int(key.replace('lot_', ''))
                if 'on' in request.form.getlist(key):
                    checked_lots.append(lot_id)
        print(checked_lots)

        new_auction = Auction(name=auction_name, start_date=auction_start_date, end_date=auction_end_date,
                              active=auction_active)

        try:
            db.session.add(new_auction)
            db.session.commit()

            auction_id = new_auction.id

            for lot_id in checked_lots:
                auction_lot = AuctionLots.query.filter_by(lot_id=lot_id, auction_id=auction_id).first()
                if not auction_lot:
                    auction_lot = AuctionLots(auction_id=auction_id, lot_id=lot_id)
                    db.session.add(auction_lot)
            db.session.commit()

            return redirect('/auctions')
        except Exception as e:
            return f'Ooops... \n{e}'
    else:
        lots = Lot.query.filter_by(active=True).order_by(Lot.date_created).all()
        return render_template('auction_editor.html', lots=lots)


@bp.route('/auctions/<int:id>/delete', methods=['GET'])
def delete(id):
    auction_to_delete = Auction.query.get_or_404(id)
    try:
        AuctionLots.query.filter_by(auction_id=id).delete()

        db.session.delete(auction_to_delete)
        db.session.commit()
        return redirect('/auctions')

    except Exception as e:
        print(f'OOOPS... Auction was not deleted \n{e}')
        return redirect('/auctions')


@bp.route('/auctions/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    checked_lots = []
    unchecked_lots = []

    auction = Auction.query.get_or_404(id)
    lots = Lot.query.filter_by(active=True).order_by(Lot.date_created).all()
    print(auction.name)
    if request.method == 'POST':
        auction_start_date_str = request.form['start_date']
        auction_end_date_str = request.form['end_date']

        auction.name = request.form['name']
        auction.start_date = datetime.strptime(auction_start_date_str, '%Y-%m-%dT%H:%M')
        auction.end_date = datetime.strptime(auction_end_date_str, '%Y-%m-%dT%H:%M')
        if request.form.get('active') == 'on':
            auction.active = True
        else:
            auction.active = False

        for key in request.form:
            if key.startswith('lot_'):
                lot_id = int(key.replace('lot_', ''))
                if 'on' in request.form.getlist(key):
                    checked_lots.append(lot_id)

        for lot in lots:
            if lot.id not in checked_lots:
                unchecked_lots.append(lot.id)

        print('Checked lots:', checked_lots)
        print('Unchecked lots:', unchecked_lots)

        try:
            db.session.commit()

            for lot_id in unchecked_lots:
                auction_lot = AuctionLots.query.filter_by(lot_id=lot_id, auction_id=id).first()
                if auction_lot:
                    db.session.delete(auction_lot)

            for lot_id in checked_lots:
                auction_lot = AuctionLots.query.filter_by(lot_id=lot_id, auction_id=id).first()
                if not auction_lot:
                    auction_lot = AuctionLots(auction_id=id, lot_id=lot_id)
                    db.session.add(auction_lot)

            db.session.commit()
            return redirect('/auctions')
        except Exception as e:
            return f'Ooops... \n{e}'
    else:
        assigned_lots = []
        for lot in lots:
            auction_lot = AuctionLots.query.filter_by(lot_id=lot.id, auction_id=id).first()
            if auction_lot:
                assigned_lots.append(lot.id)
        print('assigned lots:', assigned_lots)
        return render_template('auction_editor.html', action=f'/auctions/{id}/update', auction=auction, lots=lots,
                               assigned_lots=assigned_lots)
