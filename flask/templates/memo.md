[update] 상위 리스트 추가 

- krx 시가총액 등락율

rank, name, close, changesratio, marcap, volume
순위, 회사 이름, 가격, 등락율, 시가총액, 거래량

'''
select
	RANK() OVER (ORDER BY marcap DESC) rank,  *
from raw_data.krx_list
WHERE market like 'KOSPI'
order by marcap desc
limit 50;
'''