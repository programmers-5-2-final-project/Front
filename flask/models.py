# from db_model.postgres import db
from dashbord import db

class Gold(db.Model):
    __tablename__ = 'raw_data.gold'  # 데이터베이스 테이블 이름
    
    date = db.Column(db.Date, primary_key=True)
    usd_am = db.Column(db.Float)
    usd_pm = db.Column(db.Float)
    gbp_am = db.Column(db.Float)
    gbp_pm = db.Column(db.Float)
    euro_am = db.Column(db.Float)
    type = db.Column(db.Text)
