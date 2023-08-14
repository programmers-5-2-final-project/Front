from flask import Flask
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates')
CONFIG = dotenv_values(".flaskenv")
connection_uri = "postgresql://{}:{}@{}:{}/postgres".format(
    CONFIG["POSTGRES_USER"],
    CONFIG["POSTGRES_PASSWORD"],
    CONFIG["POSTGRES_HOST"],
    CONFIG["POSTGRES_PORT"],
)

app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
db = SQLAlchemy(app)

class DataPoint(db.Model):
    __tablename__ = 'krx_stock_000210'
    date = db.Column(db.String(50), primary_key=True)
    open = db.Column(db.String(50))  
    high = db.Column(db.String(50))
    low = db.Column(db.String(50))
    close = db.Column(db.String(50))
    volume = db.Column(db.String(50))