import psycopg2
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import re


CONFIG = dotenv_values(".flaskenv")
connection_uri = "postgresql://{}:{}@{}:{}/postgres".format(
    CONFIG["POSTGRES_USER"],
    CONFIG["POSTGRES_PASSWORD"],
    CONFIG["POSTGRES_HOST"],
    CONFIG["POSTGRES_PORT"],
)


# app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
# db = SQLAlchemy(app)

def conn_postgres():
    # 커서 생성
    cur = conn.cursor()

    # 쿼리 실행 (예: 테이블 목록 조회)
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'raw_data';")
    cur.fetchall()


# app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
# db = SQLAlchemy(app)

# with app.app_context():
#     db.reflect()