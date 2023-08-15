from flask import Flask, render_template, redirect, url_for, request, Response
from db_model.postgres import *

@app.route("/index", methods=["GET", "POST"])
def choose():
    krx_list = db.session.query(KrxList).all()
    symbols = {}
    for row in krx_list[1:]:
        symbols[row.code] = row.name

    if request.method == "GET":
        return render_template("index.html", mydict = symbols)

@app.route("/dashboard")
def dashboard():
    symbol = request.args.get("company", "")
    print("****", symbol)
    table_classes = globals()
    krx_stock = db.session.query(table_classes[f"Krx_stock_{symbol}"]).filter(table_classes[f"Krx_stock_{symbol}"].date.like('%-%-%')).all()
    data=[]
    for row in krx_stock:
        row = row.__dict__
        row.pop("_sa_instance_state")
        row['close'] = int(row['close'])
        data.append(row)
        
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    with app.app_context():
        classes = create_table_models()
        for k, v in classes.items():
            globals()[k] = v
        app.run(host="0.0.0.0", port="8082",debug=True)
