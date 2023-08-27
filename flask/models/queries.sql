-- 쿼리 0: krx 상위 시가총액 불러오기
SELECT
	RANK() OVER (ORDER BY marcap DESC) rank, name, code, changesratio,
	TO_CHAR(close, 'FM999,999,999,999') AS price
FROM raw_data.krx_list

WHERE market like 'KOSPI'
ORDER BY marcap DESC
LIMIT 50;


-- 쿼리 1: nasdaq 상위 시가총액 불러오기

SELECT
	RANK() OVER (ORDER BY marcap DESC) rank,  *, LOWER(symbol) low_symbol
FROM raw_data.nas_co_info
ORDER BY marcap DESC
LIMIT 50;


-- 쿼리 2: snp 상위 시가총액 불러오기

SELECT
	RANK() OVER (ORDER BY marcap DESC) rank,  *, LOWER(symbol) low_symbol
FROM raw_data.snp_co_info
ORDER BY marcap DESC
LIMIT 50;




-- 쿼리 3: krx 상위 등락률 불러오기
select
	RANK() OVER (ORDER BY changesratio DESC) rank,  *,
	TO_CHAR(close, 'FM999,999,999,999') AS price
from raw_data.krx_list
WHERE market like 'KOSPI'
order by changesratio desc
limit 50;


-- 쿼리 4: nasdaq 상위 등락률 불러오기
SELECT
	RANK() OVER (ORDER BY changesratio DESC) rank,  *, LOWER(symbol) low_symbol
FROM raw_data.nas_co_info
ORDER BY changesratio desc
LIMIT 50;

-- 쿼리 5: snp 상위 등락률 불러오기
SELECT
	RANK() OVER (ORDER BY changesratio DESC) rank,  *, LOWER(symbol) low_symbol
FROM raw_data.snp_co_info
ORDER BY changesratio desc
LIMIT 50;

-- 쿼리 6: 거래량 상위 50 불러오기 

with gold as(
select date, usd_pm as gold
from raw_data.gold_price
ORDER BY date DESC
LIMIT 1),

silver as(select date, usd as silver
from raw_data.silver_price
ORDER BY date DESC
LIMIT 1),

cme as (select date, last as cme
from raw_data.cme_price
ORDER BY date DESC
LIMIT 1),

orb as (select date, value as orb
from raw_data.orb_price
ORDER BY date DESC
LIMIT 1)

select *
from gold join silver  ON 1 = 1
join cme on 1=1
join orb on 1=1 ;


-- 7 상위 거래량 50
select
	RANK() OVER (ORDER BY volume DESC) rank,  *,
	TO_CHAR(close, 'FM999,999,999,999') AS price
from raw_data.krx_list
WHERE market like 'KOSPI'
order by volume desc
limit 50;