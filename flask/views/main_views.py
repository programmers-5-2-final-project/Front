from flask import Flask, render_template, Blueprint, request

"""
index 페이지 구성
"""


bp = Blueprint("main", __name__, url_prefix="/main")
# 인수로 별칭, main_views, 접두어 url 전달


@bp.route("/")
def index():
    return "주식 대시보드"


@bp.route("/home", methods=["GET", "POST"])
def home():
    # 1. 종목 목록 가져오기 -> 검색 구현
    # 1) 코스피, 2) 나스닥, 3) snp, 4) 원자재
    from .connect_db import get_simbol_company_list_dict, get_top_level_list

    kospi_simbol_company_dict = get_simbol_company_list_dict("kospi")
    nasdaq_simbol_company_dict = get_simbol_company_list_dict("nasdaq")
    snp_simbol_company_dict = get_simbol_company_list_dict("snp")
    material_simbol_company_dict = get_simbol_company_list_dict("material")

    # 2. 상위 리스트 구현 column_names, json_data
    # 1) market_capitalization 시가총액 상위 20
    _, kospi_top_market_capitalization_dict = get_top_level_list(
        "market_capitalization", "kospi"
    )
    _, nasdaq_top_market_capitalization_dict = get_top_level_list(
        "market_capitalization", "nasdaq"
    )
    _, snp_top_market_capitalization_dict = get_top_level_list(
        "market_capitalization", "snp"
    )

    # 2) fluctuation_rate 등락율 상위 20
    _, kospi_top_fluctuation_rate_dict = get_top_level_list("fluctuation_rate", "kospi")
    _, nasdaq_top_fluctuation_rate_dict = get_top_level_list(
        "fluctuation_rate", "nasdaq"
    )
    _, snp_top_fluctuation_rate_dict = get_top_level_list(
        "fluctuation_rate", "snp"
    )

    if request.method == "GET":
        return render_template("home.html", **locals())  # html에 잘 넘겨줘야함

    return render_template("home.html", **locals())


@bp.route("/detail_test")
def detail_test():
    market = request.args.get("market", "")
    symbol = request.args.get("symbol", "")
    return [market, symbol]


# 상세 페이지 라우트와 템플릿 예시
@bp.route("/detail")
def detail():
    market = request.args.get("market", "")
    symbol = request.args.get("symbol", "")

    from .connect_db import get_market_individual_data, get_simbol_company_list_dict

    symbols = get_simbol_company_list_dict(market)
    company_name = symbols[symbol]
    _, individual_stock_json_data = get_market_individual_data(market, symbol)

    if market in ["kospi", "nasdaq", "snp"]:
        dates = []
        values = []

        for row in individual_stock_json_data:
            # 날짜 리스트
            dates.append(
                "-".join(
                    [
                        str(row["date"].year),
                        str(row["date"].month),
                        str(row["date"].day),
                    ]
                )
            )
            # 종가 리스트
            values.append(row["close"])
    else:  # 원자재
        dates = []
        values = []

        from datetime import datetime

        unit_dict = {"silver": "usd", "orb": "value", "gold": "usd_pm", "cme": "open"}

        for row in individual_stock_json_data:
            # 날짜 리스트

            datetime_obj = row["date"]
            # datetime_obj = datetime.strptime(row["date"], "%Y-%m-%d")
            dates.append(
                "-".join(
                    [
                        str(datetime_obj.year),
                        str(datetime_obj.month),
                        str(datetime_obj.day),
                    ]
                )
            )
            # 종가 리스트
            unit_ = unit_dict[symbol]
            values.append(row[unit_])

    # 이후 render_template을 사용하여 상세 정보를 템플릿에 전달하여 표시
    return render_template("detail.html", **locals())


from .connect_db import conn_test_db_get_json_data


@bp.route("/dashboard")
def dashboard():  # 컴퍼니 값을 받으면 심볼로 가져오는거겠지 ?
    symbol = request.args.get("company", "")  # 매개변수로부터 가져오는 것
    print("****", symbol)

    _, json_data = conn_test_db_get_json_data(f"analytics.krx_stock_{symbol}")
    data = []
    for row in json_data:
        row["close"] = int(row["close"])
        data.append(row)

    # 반환하는거 : List
    # [row, row] row : dict
    return render_template("krx_stock/dashboard.html", data=data)


@bp.route("/test")
def test():  # 컴퍼니 값을 받으면 심볼로 가져오는거겠지 ?
    # symbol = request.args.get("company", "") # 매개변수로부터 가져오는 것
    symbol = "000140"
    print("****", symbol)

    _, json_data = conn_test_db_get_json_data(f"analytics.krx_stock_{symbol}")
    data = []
    for row in json_data:
        row["close"] = int(row["close"])
        data.append(row)

    # 반환하는거 : List
    # [row, row] row : dict
    return render_template("krx_stock/dashboard_test.html", **locals())
