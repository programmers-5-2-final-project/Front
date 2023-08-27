from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
import os

# RDS connection setup
CONFIG = {}

# Check if a specific secret (e.g., POSTGRES_USER) is set in the environment
if "POSTGRES_USER" in os.environ:
    # Running in GitHub Actions or a similar environment with secrets
    CONFIG["POSTGRES_USER"] = os.environ["POSTGRES_USER"]
    CONFIG["POSTGRES_PASSWORD"] = os.environ["POSTGRES_PASSWORD"]
    CONFIG["POSTGRES_HOST"] = os.environ["POSTGRES_HOST"]
    CONFIG["POSTGRES_PORT"] = os.environ["POSTGRES_PORT"]
else:
    # Local development
    CONFIG = dotenv_values(".flaskenv")

connection_uri = "postgresql://{}:{}@{}:{}/postgres".format(
    CONFIG["POSTGRES_USER"],
    CONFIG["POSTGRES_PASSWORD"],
    CONFIG["POSTGRES_HOST"],
    CONFIG["POSTGRES_PORT"],
)

app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
db = SQLAlchemy(app)

# 데이터베이스 모델 생성
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Flask 라우트 설정
@app.route('/')
def index():
    # 데이터베이스에서 데이터 가져오기
    users = UserData.query.all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()
