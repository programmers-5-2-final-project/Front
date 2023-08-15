from db_model.postgres import app, db, create_table_models

with app.app_context():
    create_table_models()
    db.create_all()