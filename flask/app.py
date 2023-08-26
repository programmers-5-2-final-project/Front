from flask import Flask, render_template, redirect, url_for, request, Response, jsonify
from views import main_views

from dotenv import dotenv_values


app = Flask(__name__, static_url_path="/static")


## 블루 프린트 사용
# 블루 프린트 등록
from views import main_views


# main_views에서 생성한 객체 등록
app.register_blueprint(main_views.bp)


if __name__ == "__main__":
    with app.app_context():
        app.run(host="127.0.0.1", port="5000", debug=True)


# 좀 있다 다 지우기


def conn_db_get_json(table):
    """rds 접속해서
    컬럼 리스트, 데이터 (json형식) 가져오기

    - input : table - rds에 적재된 스키마.테이블 명 ex) raw_data.gold
    - output : column_names(list), json_data(list : [{}, {}])
    """

    import psycopg2
    import json

    # rds 데이터 베이스 연결
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # 쿼리 실행 및 데이터 가져오기
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    data = cursor.fetchall()

    # 컬럼 이름 가져오기
    column_names = [desc[0] for desc in cursor.description]

    # 연결 종료
    cursor.close()
    conn.close()

    # 데이터 딕셔너리로 변환
    json_data = []
    for row in data:
        row_dict = {col_name: value for col_name, value in zip(column_names, row)}
        json_data.append(row_dict)

    return column_names, json_data


@app.route("/gold")
def gold():
    # from models import Gold
    # gold_list = Gold.query.order_by(Gold.date.desc())
    # return render_template('metal/gold.html', gold_list=gold_list)
    # return render_template('metal/gold.html', data=db.session.query(Gold).all())

    label = "gold"  # 종류 이름

    # 데이터 가져오기
    column_names, json_data = conn_db_get_json(f"raw_data.{label}")

    xlabels = []
    dataset = []
    for row in json_data:
        xlabels.append(row["date"])
        dataset.append(row["usd_am"])
    return render_template("metal/gold.html", **locals())

    # return render_template('metal/gold.html', columns = column_names,  data=json_data)


@app.route("/gold/chart")
def gold_chart():
    label = "gold"  # 종류 이름

    # 데이터 가져오기
    column_names, json_data = conn_db_get_json(f"raw_data.{label}")

    xlabels = []
    dataset = []
    for row in json_data:
        xlabels.append(row["date"])
        dataset.append(row["usd_am"])

    return render_template("metal/gold_chart.html", **locals())

    # return render_template('metal/gold_chart.html', columns = column_names,  data=json_data)


@app.route("/test")
def test():  # 컴퍼니 값을 받으면 심볼로 가져오는거겠지 ?
    import datetime

    # symbol = request.args.get("company", "") # 매개변수로부터 가져오는 것
    symbol = "000140"
    print("****", symbol)
    from views import krx_stock

    _, json_data = krx_stock.conn_test_db_get_json(f"analytics.krx_stock_{symbol}")
    dates = []
    values = []
    for row in json_data:
        dates.append(
            "-".join(
                [str(row["date"].year), str(row["date"].month), str(row["date"].day)]
            )
        )
        values.append(int(row["close"]))

    # 반환하는거 : List
    # [row, row] row : dict
    return render_template("krx_stock/dashboard_test.html", **locals())


@app.route("/test2")
def test2():  # 컴퍼니 값을 받으면 심볼로 가져오는거겠지 ?
    import datetime

    # symbol = request.args.get("company", "") # 매개변수로부터 가져오는 것
    symbol = "000140"
    print("****", symbol)
    from views import krx_stock

    _, json_data = krx_stock.conn_test_db_get_json(f"analytics.krx_stock_{symbol}")
    dates = []
    values = []
    for row in json_data:
        dates.append(
            "-".join(
                [str(row["date"].year), str(row["date"].month), str(row["date"].day)]
            )
        )
        values.append(int(row["close"]))

    # 반환하는거 : List
    # [row, row] row : dict
    return render_template("chart_js.html", **locals())


@app.route("/kospi_list")
def kospi_list():
    from views import krx_stock

    label = "kospi_list"  # 종류 이름

    # 데이터 가져오기
    column_names, json_data = krx_stock.conn_test_db_get_json(f"analytics.{label}")

    xlabels = []
    dataset = []
    # for row in json_data:
    #     xlabels.append(row['date'])
    #     dataset.append(row['usd_am'])
    return render_template("metal/gold.html", **locals())
