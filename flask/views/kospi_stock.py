from flask import Flask, render_template, Blueprint, request

"""
krx_stock에 대해서 조회하는 페이지였으나 임시적으로 analytics.kospi_list로 확인


-> 파티션으로 바뀌어서 다시 수정 

kospi_list

파티션 조회하기 
ex)
select *
from krx_partition_of_stock_by_code 
partition (krx_stock_000140);
"""

# 블루프린트 사용한다면

bp_krx = Blueprint("dashboard", __name__, url_prefix="/dashboard")
# 인수로 별칭, main_views, 접두어 url 전달


def kospi_get_individual_stock_json_data(simbol="000140"):
    """코스피 종목 코드 입력하면
    1) 컬럼 리스트,
    2) 가격 데이터 (json형식) 가져오기

    input:
        simbol (str): 종목 코드 입력
    output:

    """
    column_names, json_data = kospi_conn_test_db_get_json_data(
        f"analytics.krx_partition_of_stock_by_code PARTITION (krx_stock_{simbol})"
    )

    return column_names, json_data


def kospi_get_simbol_company_dict():
    """
    kospi_conn_test_db_get_json_data 함수 이용해서
    전체 리스트 목록으로 보여주기 받아오기

    - input : x
        - label = "kospi_list"
        - column_names, json_data = kospi_conn_test_db_get_json_data(f"analytics.{label}")
    - output : dict = {종목코드 : '회사이름'}

    테이블 이름 analyics.kospi_list (현재 test db에 위치)
    """

    # 데이터 가져오기
    label = "kospi_list"
    column_names, json_data = kospi_conn_test_db_get_json_data(f"analytics.{label}")

    symbols = {}
    for row in json_data:
        symbols[row["code"]] = row["name"]
    # {000140 : '회사이름'}

    return symbols


def kospi_conn_test_db_get_json_data(table):
    """rds 접속해서 -> de-5-2에 analytics스키마에 현재 있는 상황
    1) 컬럼 리스트,
    2) 데이터 (json형식) 가져오기

    - input : table - rds에 적재된 스키마.테이블 명 ex) raw_data.gold
        -  query = f"SELECT * FROM {table};"
    - output : column_names(list), json_data(list : [{}, {}])
    """
    from dotenv import dotenv_values

    CONFIG = dotenv_values(".flaskenv")
    db_config = {
        "dbname": "dev",
        "user": CONFIG["POSTGRES_USER"],
        "password": CONFIG["POSTGRES_PASSWORD"],
        "host": "de-5-2.ch4xfyi6stod.ap-northeast-2.rds.amazonaws.com",
        "port": CONFIG["POSTGRES_PORT"],
    }
    connection_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        db_config["user"],
        db_config["password"],
        db_config["host"],
        db_config["port"],
        db_config["dbname"],
    )

    import psycopg2
    import json

    # rds 데이터 베이스 연결
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # 쿼리 실행 및 데이터 가져오기
    query = f"SELECT * FROM {table};"
    print(query)
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


@bp_krx.route("/index", methods=["GET", "POST"])
def choose():
    """전체 리스트 목록으로 보여주기 받아오기"""
    # krx_list = db.session.query(KrxList).all()
    # 데이터 가져오기
    label = "kospi_list"
    column_names, json_data = conn_test_db_get_json(f"analytics.{label}")

    # symbols = {}
    # for row in krx_list[1:]:
    #     symbols[row.code] = row.name
    symbols = {}
    for row in json_data:
        symbols[row["code"]] = row["name"]
    # {000140 : '회사이름'}

    if request.method == "GET":
        return render_template("krx_stock/index.html", **locals())  # html에 잘 넘겨줘야함


@bp_krx.route("/dashboard")
def dashboard():  # 컴퍼니 값을 받으면 심볼로 가져오는거겠지 ?
    symbol = request.args.get("company", "")  # 매개변수로부터 가져오는 것
    print("****", symbol)

    _, json_data = kospi_get_individual_stock_json_data(symbol)
    data = []
    for row in json_data:
        row["close"] = int(row["close"])
        data.append(row)

    # 반환하는거 : List
    # [row, row] row : dict
    return render_template("krx_stock/dashboard.html", **local())


@bp_krx.route("/test")
def test():  # 컴퍼니 값을 받으면 심볼로 가져오는거겠지 ?
    # symbol = request.args.get("company", "") # 매개변수로부터 가져오는 것
    symbol = "000140"
    print("****", symbol)

    _, json_data = kospi_get_individual_stock_json_data(symbol)
    data = []
    for row in json_data:
        row["close"] = int(row["close"])
        data.append(row)

    # 반환하는거 : List
    # [row, row] row : dict
    return render_template("krx_stock/dashboard_test.html", **locals())


# @app.route('/stock/<stock_name>')
def stock_detail(stock_name):
    # stock_name을 이용하여 해당 종목의 가격 정보를 조회하고 전달
    # 예를 들어, stock_name에 따라 DB에서 가격 정보를 가져오는 로직
    price_info = get_price_info(stock_name)
    return render_template(
        "stock_detail.html", stock_name=stock_name, price_info=price_info
    )
