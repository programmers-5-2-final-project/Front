
[update] gold 대시보드 추가

[update] 그래프 월별 데이터로 변경

[update] 홈 상위 거래량 살펴보기 혹은 그래프 추가 

[update] 로고 추가

[update] 세부 페이지 디자인 수정

[update] 세부 페이지 정보 추가

[update] 버튼 선택해서 볼 수 있게 

[update] 세부 차트 단위 선택해서 볼 수 있게 하고 싶음

[update] 상단바 통일

[update] 모바일에서 안깨지게 수정

--- 
[update] 홈 세계 지수 구현, 가격 추가 

"raw_data.index_usd_krw_exchange_rate", 원-달러 환율
"raw_data.index_kospi", 코스피 지수
"raw_data.index_djia", 다우존스
"raw_data.index_nasdaq", 나스닥
"raw_data.index_snp", S&P 500 지수


[update] symbol 파라미터 수정 
-> 문제점 : 
    - symbol : 소문자로 바꿔야함
        - stock['symbol']
    - html



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