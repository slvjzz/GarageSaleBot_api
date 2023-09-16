from flask import Flask
from flask_migrate import Migrate
from models import db
from routes_lots import bp as main_bp


app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://API_User:API123@localhost/GarageSale_DB?driver=ODBC+Driver+17+for+SQL+Server'

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

