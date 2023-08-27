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