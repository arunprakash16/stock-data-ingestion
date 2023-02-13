# stock-data-ingestion

### Daily stock trading data ingestion in batch mode
Data per stock (history to till date) will be sent in a csv file.
1. Assumptions:
   1. data-format (header): Date, Open, High, Low, Close, Adj Close, Volume
   2. file name: stock name
2. db-scripts contains ddl and dql.
   1. ddl - contains sql script for table schema
   2. dql - contains sql script for query to calculate below information:
      1. Query 1 - Assumption is to provide below average based on current date.
      2. Query 2 - Assumption is to provide below running average. 
         1. Weekly average of High, Low and Volume 
         2. Monthly average of High, Low and Volume 
         3. Quarterly average of High, Low and Volume 
         4. Yearly average of High, Low and Volume
3. src/batch_process/\__init__.py - module requires file path to run the program to insert data in to mysql
   e.g. run command src/batch_process/\__init__.py -fp ../../data/MSFT.csv

### Daily stock trading data ingestion in stream mode
Stock trading data will be received in real time (streaming)
1. Assumptions:
   1. Record type: Json
   2. Json object specification:
      1. stock_id: string
      2. trade_date: timestamp
      3. open_price: number
      4. close_price: number
      5. trade_price: number
      6. volume: number
      7. high_52: number
      8. low_52: number
   3. SMA - Simple Moving Average of 20, 50 and 200 days are calculated based on close price.
   4. API - Input parms:
      1. stock_id
   5. API - Output: Json object specification
      1. stock_id: string
      2. last_trade_date: timestamp
      3. last_trade_price: number
      4. sma_20: number
      5. sma_50: number
      6. sma_200: number
      7. curr_price_above_sma_indicator: bool (specify whether price is its above moving average)
      8. curr_price_above: string (sets the maximum sma type e.g. sma_20)
2. Design:
   1. Had chosen snowflake as data lake due to below functionalities and this pipeline can be of type ELT.  
      1. Snowpipe can be leveraged to ingest data directly into snowflake.
      2. Even when smaller transformation is needed, we can load them into a temporary table and then have a batch job to perform the transformation and ingest into final table.
      3. Snowflake cluster cost depends on the usage. Since, heavy usage is between trading hours cost can be saved for rest of the off hours.   
   2. SMA of 20, 50 and 200 days based on close price can be calculated through batch job.

![alt text](https://github.com/arunprakash16/stock-data-ingestion/resource/images/stream_stock.png?raw=true)
      