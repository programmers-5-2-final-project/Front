
[update] gold 대시보드 추가

[update] 그래프 월별 데이터로 변경

[update] 홈 세계 지수 구현

[update] 홈 상위 거래량 살펴보기 혹은 그래프 추가 

[update] 로고 추가

[update] 세부 페이지 디자인 수정

---
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