from flask import Flask, render_template, Blueprint

'''
krx_stock에 대해서 조회하는 페이지였으나 임시적으로 analytics.kospi_list로 확인
'''

# 블루프린트 사용한다면 

bp_kospi = Blueprint('kospi', __name__, url_prefix='/kospi')
# 인수로 별칭, main_views, 접두어 url 전달

@bp_kospi.route('/')
def index():
    return 'Welcome to Stock Dashboard'


def conn_test_db_get_json(table):
    '''rds 접속해서 -> de-5-2에 analytics스키마에 현재 있는 상황 
    컬럼 리스트, 데이터 (json형식) 가져오기
    
    - input : table - rds에 적재된 스키마.테이블 명 ex) raw_data.gold
    - output : column_names(list), json_data(list : [{}, {}])
    '''
    from dotenv import dotenv_values
    CONFIG = dotenv_values(".flaskenv")
    db_config = {
    'dbname': 'dev',
    'user': CONFIG["POSTGRES_USER"],
    'password': CONFIG["POSTGRES_PASSWORD"],
    'host': 'de-5-2.ch4xfyi6stod.ap-northeast-2.rds.amazonaws.com',
    'port' : CONFIG["POSTGRES_PORT"]
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
    query = f'SELECT * FROM {table}'
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

def get_table_names(): # 코드를 불러오기 위해 
    tables = db.session.execute(text("SELECT code FROM raw_data.krx_list;"))
    table_names = ["krx_stock_"+table[0] for table in tables]
    return table_names



# @bp.route('/<label>') # 어떻게 써야하지? 
@bp_kospi.route('/kospi_list') 
def kospi_list():
    from views import krx_stock
    label = 'kospi_list' # 종류 이름
    
    # 데이터 가져오기 
    column_names, json_data = krx_stock.conn_test_db_get_json(f'analytics.{label}')

    xlabels = []
    dataset = []
    # for row in json_data:
    #     xlabels.append(row['date'])
    #     dataset.append(row['usd_am'])    
    return render_template('metal/gold.html', **locals())

# @app.route('/stock/<stock_name>')
def stock_detail(stock_name):
    # stock_name을 이용하여 해당 종목의 가격 정보를 조회하고 전달
    # 예를 들어, stock_name에 따라 DB에서 가격 정보를 가져오는 로직
    price_info = get_price_info(stock_name)
    return render_template('stock_detail.html', stock_name=stock_name, price_info=price_info)
