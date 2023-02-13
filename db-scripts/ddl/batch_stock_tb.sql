create database stock;

use stock;

create table batch_stock_data(
	stock_id varchar(50) Not Null,
	trade_date date,
	open_price decimal(10, 2),
	high_price decimal(10, 2),
	low_price decimal(10, 2),
	close_price decimal(10, 2),
	adj_close_price decimal(10, 2),
	volume int)
partition by range (year(trade_date))
subpartition by key (stock_id)
subpartitions 2 (
	partition p0 values less than (2010),
    partition p1 values less than (2020),
    partition p2 values less than maxvalue
);