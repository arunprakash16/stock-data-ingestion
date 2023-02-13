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
