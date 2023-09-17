from flask import Flask, redirect
from flask_migrate import Migrate
from models import db
from routes_lots import bp as lots_bp
from routes_auctions import bp as auctions_bp

UPLOAD_FOLDER = "D:/GarageSale/uploaded_files/lots/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://API_User:API123@localhost/GarageSale_DB?driver=ODBC+Driver+17+for+SQL+Server'

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(lots_bp)
app.register_blueprint(auctions_bp)


@app.route('/')
def index():
    return redirect('/lots')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

