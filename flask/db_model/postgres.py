from flask import Flask
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import re

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
    __abstract__ = True
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

def get_table_names():
    tables = db.session.execute(text("SELECT code FROM krx_list;"))
    table_names = ["krx_stock_"+table[0] for table in tables]
    return table_names

def create_table_models():
    table_names = get_table_names()
    classes={}
    for table_name in table_names:
        if bool(re.search(r'krx_stock_\d', table_name)):
            model_name = table_name.capitalize()
            table_class = type(model_name, (KrxStock, db.Model), {"__tablename__": table_name})
            classes[model_name] = table_class
    return classes