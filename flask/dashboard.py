from flask import Flask, render_template, redirect, url_for, request, Response
from db_model.postgres import *

def search_data(search_term, symbols):
    results = {}
    for symbol, value in symbols.items():
        if search_term.lower() in value[0].lower():
            results[symbol] = value
    
    return results

@app.route("/index", methods=["GET", "POST"])
def index():
    krx_list = db.session.query(KrxList).all()
    symbols = {}
    for row in krx_list[1:]:
        symbols[row.code] = [row.name, row.market, row.marcap]

    if request.method == "POST":
        search_term = request.form.get("search")
        results = search_data(search_term, symbols)
    else:
        results = symbols
    return render_template("index.html", mydict = results)

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
