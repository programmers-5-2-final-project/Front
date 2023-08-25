"""_summary_
- get_market_individual_data(market, symbol)
    - market, symbol 넣으면 
    - 컬럼명, json_data 형식으로 
    - 개별 종목에 대한 가격 리스트를 가져오는 함수 

- get_simbol_company_list_dict(market)
    - market 넣으면 
    - 그 마켓에 해당하는 종목 리스트가 
    - {종목코드 : '회사이름'} 형식으로 반환됨

- conn_test_db_get_json_data
- conn_db_get_json_data
    - table 명 적으면 select 문으로 조회해서, 
    컬럼명, josn_data 형식으로 가져오는 함수 


"""


def get_market_individual_data(market, symbol):
    """
    - get_market_individual_data(market, symbol)
        - market, symbol 넣으면
        - 컬럼명, json_data 형식으로
        - 개별 종목에 대한 가격 리스트를 가져오는 함수
    """

    if market == "kospi":
        column_names, json_data = conn_db_get_json_data(f"analytics.krx_stock_{symbol}")
    elif market == "nasdaq":
        column_names, json_data = conn_db_get_json_data(f"analytics.nas_stock_{symbol}")
    elif market == "snp":
        column_names, json_data = conn_db_get_json_data(f"analytics.snp_stock_{symbol}")
    elif market == "material":
        column_names, json_data = conn_db_get_json_data(f"row_data.{symbol}")
    else:
        return None  # 처리하지 않는 시장에 대한 처리

    return column_names, json_data


def get_simbol_company_list_dict(market):
    """
    전체 리스트 목록으로 보여주기 받아오기

    - input : x
        - label = "kospi_list"
        - column_names, json_data = kospi_conn_test_db_get_json_data(f"analytics.{label}")
    - output : dict = {종목코드 : '회사이름'}

    테이블 이름 analyics.kospi_list (현재 test db에 위치)
    """

    if market == "kospi":
        label = "krx_list"
        column_names, json_data = conn_db_get_json_data(f"raw_data.{label}")

        symbols = {}
        for row in json_data:
            symbols[row["code"]] = row["name"]
        # {000140 : '회사이름'}

        return symbols

    elif market == "nasdaq":
        label = "nas_list"
        column_names, json_data = conn_db_get_json_data(f"raw_data.{label}")

        symbols = {}
        for row in json_data:
            symbols[row["symbol"].lower()] = row["name"]
        # {000140 : '회사이름'}

        return symbols
    elif market == "snp":
        label = "snp_stock_list"

        # column_names, json_data = conn_db_get_json_data(f"raw_data.{label}")

        # symbols = {}
        # for row in json_data:
        #     symbols[row["symbol"].lower()] = row["name"]
        # # {000140 : '회사이름'}

        return {}
        # return symbols

    elif market == "material":
        return {"gold": "금", "silver": "은", "cme": "구리", "orb": "원유"}

    else:
        return None  # 처리하지 않는 시장에 대한 처리


## 회사 정보 가지고 오는 함수도 만들기


def get_kospi_data(symbol):
    """코스피 종목 코드 입력하면
        1) 컬럼 리스트,
        2) 가격 데이터 (json형식) 가져오기

    input:
        simbol (str): 종목 코드 입력
    output: column_names, json_data

    """
    column_names, json_data = conn_test_db_get_json_data(
        f"analytics.krx_stock_{symbol}"
    )

    return column_names, json_data


def get_nasdaq_data(symbol):
    # 나스닥 시장의 회사 데이터 가져오는 코드
    pass


def get_snp_data(symbol):
    # S&P 시장의 회사 데이터 가져오는 코드
    pass


def get_material_data(symbol):
    # 원자재 시장의 회사 데이터 가져오는 코드
    pass


### db 연결 함수
def conn_db_get_json_data(table):
    """rds 접속해서 de-5-2-db
    컬럼 리스트, 데이터 (json형식) 가져오기

    - input : table - rds에 적재된 스키마.테이블 명 ex) raw_data.gold
    - output : column_names(list), json_data(list : [{}, {}])
    """
    from dotenv import dotenv_values

    CONFIG = dotenv_values(".flaskenv")
    db_config = {
        "dbname": "dev",
        "user": CONFIG["POSTGRES_USER"],
        "password": CONFIG["POSTGRES_PASSWORD"],
        "host": CONFIG["POSTGRES_HOST"],
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


def conn_test_db_get_json_data(table):
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
