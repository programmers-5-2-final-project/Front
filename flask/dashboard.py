from flask import Flask, render_template, render_template_string
from sqlalchemy import create_engine, text
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import json
from db.postgres import DataPoint, app, db

@app.route("/dashboard")
def dashboard():
    datapoints = db.session.query(DataPoint).filter(DataPoint.date.like('%-%-%')).all()
    data=[]
    for row in datapoints:
        row = row.__dict__
        row.pop("_sa_instance_state")
        row['close'] = int(row['close'])
        data.append(row)
        
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8082", debug=True)
