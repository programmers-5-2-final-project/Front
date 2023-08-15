from db_model.postgres import app, db

with app.app_context():
    db.create_all()