import yfinance as yf
import psycopg2
from dotenv import dotenv_values
from datetime import datetime

"""
세계 지수 수집하기 위한 파이썬 파일
"""
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

db_config = {
    "dbname": "dev",
    "user": CONFIG["POSTGRES_USER"],
    "password": CONFIG["POSTGRES_PASSWORD"],
    "host": CONFIG["POSTGRES_HOST"],
    "port": CONFIG["POSTGRES_PORT"],
}


def get_index_data(symbol, start_date, end_date):
    index = yf.Ticker(symbol)
    print(f"index: {index}")
    data = index.history(start=start_date, end=end_date)
    print(data)
    return data


def insert_data_to_rds(data, table_name):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    drop_query = f"""DROP TABLE IF EXISTS {table_name};"""
    cursor.execute(drop_query)
    print(f"{table_name} drop")

    create_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
        date date,
        open float,
        high float,
        low float,
        close float,
        volume float
        );"""
    cursor.execute(create_query)
    print(f"{table_name} create")

    for index, row in data.iterrows():
        values = [
            index,
            row["Open"],
            row["High"],
            row["Low"],
            row["Close"],
            row["Volume"],
        ]
        # date_obj = values[0].strftime("%Y-%m-%d")
        # date_obj = datetime(date_obj)
        # # 주어진 타임스탬프 문자열
        # timestamp_string = "2003-01-02 00:00:00-0"

        # 타임스탬프 형식을 datetime 객체로 변환
        # timestamp_datetime = datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S-%f")

        # # 날짜 부분만 추출하여 문자열로 변환
        # formatted_date = timestamp_datetime.strftime("%Y-%m-%d")
        query = f"INSERT INTO {table_name} (date, open, high, low, close, volume) VALUES (to_timestamp('{values[0]}', 'YYYY-MM-DD'), {values[1]}, {values[2]}, {values[3]},{values[4]}, {values[5]});"

        cursor.execute(query, values)
        print(query)

    conn.commit()
    cursor.close()
    conn.close()


# if __name__ == "__main__":
#     start_date = "2003-01-01"
#     end_date = "2023-08-01"

#     index_symbols = ["^DJI", "^IXIC", "^GSPC"]  # 다우존스, 나스닥, S&P 500 지수
#     table_names = [
#         "raw_data.index_djia",
#         "raw_data.index_nasdaq",
#         "raw_data.index_snp",
#     ]  # 테이블 이름

#     for symbol, table_name in zip(index_symbols, table_names):
#         print(f"tabel:{table_name} symbol:{symbol}")

#         index_data = get_index_data(symbol, start_date, end_date)
#         print(f"sucess get {table_name} data")
#         insert_data_to_rds(index_data, table_name)
#         print(f"{symbol} data inserted to {table_name}")


# def insert_data_to_rds(data, table_name):
#     conn = psycopg2.connect(**db_config)
#     cursor = conn.cursor()

#     drop_query = f"""DROP TABLE IF EXISTS {table_name};"""
#     cursor.execute(drop_query)
#     print(f"{table_name} drop")

#     create_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
#         date date,
#         open float,
#         high float,
#         low float,
#         close float,
#         volume float
#         );"""
#     cursor.execute(create_query)
#     print(f"{table_name} create")

#     for index, row in data.iterrows():
#         values = [
#             index,
#             row["Open"],
#             row["High"],
#             row["Low"],
#             row["Close"],
#             row["Volume"],
#         ]
#         # date_obj = values[0].strftime("%Y-%m-%d")
#         # date_obj = datetime(date_obj)
#         # # 주어진 타임스탬프 문자열
#         # timestamp_string = "2003-01-02 00:00:00-0"

#         # 타임스탬프 형식을 datetime 객체로 변환
#         # timestamp_datetime = datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S-%f")

#         # # 날짜 부분만 추출하여 문자열로 변환
#         # formatted_date = timestamp_datetime.strftime("%Y-%m-%d")
#         query = f"INSERT INTO {table_name} (date, open, high, low, close, volume) VALUES (to_timestamp('{values[0]}', 'YYYY-MM-DD'), {values[1]}, {values[2]}, {values[3]},{values[4]}, {values[5]});"

#         cursor.execute(query, values)
#         print(query)

#     conn.commit()
#     cursor.close()
#     conn.close()


if __name__ == "__main__":
    start_date = "2003-01-01"
    end_date = "2023-08-01"

    index_symbols = ["^KS11", "KRW=X"]  # 코스피 지수, 원-달러 환율
    table_names = [
        "raw_data.index_kospi",
        "raw_data.index_usd_krw_exchange_rate",
    ]  # 테이블 이름

    for symbol, table_name in zip(index_symbols, table_names):
        print(f"tabel:{table_name} symbol:{symbol}")

        index_data = get_index_data(symbol, start_date, end_date)
        print(f"sucess get {table_name} data")
        type(index_data)
        insert_data_to_rds(index_data, table_name)
        print(f"{symbol} data inserted to {table_name}")
