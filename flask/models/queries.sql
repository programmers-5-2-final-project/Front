-- 쿼리 1: krx 상위 시가총액 불러오기
SELECT
	RANK() OVER (ORDER BY marcap DESC) 시가총액_순위,  *
FROM raw_data.krx_list
ORDER BY marcap DESC
LIMIT 20;


-- 쿼리 2: nasdaq, snp 상위 시가총액 불러오기
SELECT * FROM users WHERE id = :user_id;

-- 쿼리 3: krx 상위 등락율 불러오기
select
	RANK() OVER (ORDER BY changesratio DESC) 등락율,  *
from raw_data.krx_list
order by changesratio desc
limit 20;


-- 쿼리 4: 특정 제품 조회
SELECT * FROM products WHERE id = :product_id;
