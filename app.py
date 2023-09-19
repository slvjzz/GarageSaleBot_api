from flask import Flask, redirect
from flask_migrate import Migrate
from models import db
from routes_lots import bp as lots_bp
from routes_auctions import bp as auctions_bp
from routes_bot import bp as bot_bp
from routes_categories import bp as categories_bp
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

UPLOAD_FOLDER = config['files']['UPLOAD_FOLDER']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config[
    'SQLALCHEMY_DATABASE_URI'] = config['database']['DATABASE_URL']

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(lots_bp)
app.register_blueprint(auctions_bp)
app.register_blueprint(bot_bp)
app.register_blueprint(categories_bp)


@app.route('/')
def index():
    return redirect('/lots')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

