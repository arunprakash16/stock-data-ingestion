# Query 1
WITH one_yr_data AS(select stock_id, trade_date, low_price, high_price, volume from batch_stock_data order by trade_date desc limit 365),
quarterly_data AS(select stock_id, trade_date, low_price, high_price, volume from one_yr_data order by trade_date desc limit 90),
monthly_data AS(select stock_id, trade_date, low_price, high_price, volume from quarterly_data order by trade_date desc limit 30),
weekly_data AS(select stock_id, trade_date, low_price, high_price, volume from quarterly_data order by trade_date desc limit 7)
select stock_id, 'Yearly' as avg_type, avg(low_price) as avg_low, avg(high_price) as avg_high, avg(volume) as avg_volume
from one_yr_data
union
select stock_id, 'Quarterly' as avg_type, avg(low_price) as avg_low, avg(high_price) as avg_high, avg(volume) as avg_volume
from quarterly_data
union
select stock_id, 'Monthly' as avg_type, avg(low_price) as avg_low, avg(high_price) as avg_high, avg(volume) as avg_volume
from monthly_data
union
select stock_id, 'Weekly' as avg_type, avg(low_price) as avg_low, avg(high_price) as avg_high, avg(volume) as avg_volume
from weekly_data;

# Query 2
WITH trade_data AS (
  SELECT trade_date, high_price, low_price, volume
  FROM batch_stock_data
  ORDER BY trade_date desc
)
SELECT
  trade_date,
  high_price,
  low_price,
  volume,
  AVG(high_price) OVER (ROWS 7 PRECEDING) AS weekly_high_avg,
  AVG(low_price) OVER (ROWS 7 PRECEDING) AS weekly_low_avg,
  AVG(volume) OVER (ROWS 7 PRECEDING) AS weekly_volume_avg,
  AVG(high_price) OVER (ROWS 30 PRECEDING) AS monthly_high_avg,
  AVG(low_price) OVER (ROWS 30 PRECEDING) AS monthly_low_avg,
  AVG(volume) OVER (ROWS 30 PRECEDING) AS monthly_volume_avg,
  AVG(high_price) OVER (ROWS 90 PRECEDING) AS quarterly_high_avg,
  AVG(low_price) OVER (ROWS 90 PRECEDING) AS quarterly_low_avg,
  AVG(volume) OVER (ROWS 90 PRECEDING) AS quarterly_volume_avg,
  AVG(high_price) OVER (ROWS 365 PRECEDING) AS yearly_high_avg,
  AVG(low_price) OVER (ROWS 365 PRECEDING) AS yearly_low_avg,
  AVG(volume) OVER (ROWS 365 PRECEDING) AS yearly_volume_avg
FROM trade_data
;