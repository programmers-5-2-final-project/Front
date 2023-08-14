from db.postgres import DataPoint, app, db

with app.app_context():
    data = db.session.query(DataPoint).order_by(DataPoint.date).filter(DataPoint.date.like('%-%-%')).all()
    print(data)
