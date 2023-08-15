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

with app.app_context():
    db.reflect()

class KrxStock(db.Model):
    __tablename__ = 'krx_stock_000210'
    __table_args__ = {'extend_existing': True} 
    date = db.Column(db.String(50), primary_key=True)
    open = db.Column(db.String(50))  
    high = db.Column(db.String(50))
    low = db.Column(db.String(50))
    close = db.Column(db.String(50))
    volume = db.Column(db.String(50))

class KrxList(db.Model):
    __tablename__ = 'krx_list'
    __table_args__ = {'extend_existing': True} 
    code = db.Column(db.String(50), primary_key=True)
    isu_cd = db.Column(db.String(50))  
    name = db.Column(db.String(50))
    market = db.Column(db.String(50))
    dept = db.Column(db.String(50))
    close = db.Column(db.String(50))
    changecode = db.Column(db.String(50))  
    changes = db.Column(db.String(50))
    changesratio = db.Column(db.String(50))
    open = db.Column(db.String(50))
    high = db.Column(db.String(50))
    low = db.Column(db.String(50))  
    volume = db.Column(db.String(50))
    amount = db.Column(db.String(50))
    marcap = db.Column(db.String(50))
    stocks = db.Column(db.String(50))
    marketid = db.Column(db.String(50))
