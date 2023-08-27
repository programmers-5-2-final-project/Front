from connect_db import get_market_individual_data, get_simbol_company_list_dict

market = "nasdaq"
symbols = get_simbol_company_list_dict(market)
print(symbols)
