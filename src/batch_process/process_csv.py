import csv
import json

from src import conf, log_info, log_error, get_env_var_data
from src.connectors.mysql_connector import MysqlConnector


def convert_datatype(stock_id, row, float_pos, int_pos):
    try:
        for col_pos in float_pos:
            row[col_pos] = float(row[col_pos])
        for col_pos in int_pos:
            row[col_pos] = int(row[col_pos])
        return (stock_id, *row)
    except Exception as err:
        log_error('Has issue in type casting value - {}, hence will be skipped from loading.'.format(row))


def process_csv(file_name, numeric_col_sec, float_col_key, int_col_key):
    conversion_needed = True
    header = True
    processed_data = list()
    float_col_list = list()
    int_col_list = list()

    stock_id = file_name.split('/')[-1].split('.')[0]
    float_col_str = conf.get(numeric_col_sec, float_col_key, fallback='')
    int_col_str = conf.get(numeric_col_sec, int_col_key, fallback='')
    mysql_conn = json.loads(conf.get('mysql_conn', 'mysql_conn_str'))
    mysql_conn['user'] = get_env_var_data('mysql_username')
    mysql_conn['password'] = get_env_var_data('mysql_password')
    chunk_size = conf.getint('mysql_conn', 'chunk_size')
    insert_query = "insert into batch_stock_data (stock_id, trade_date, open_price, high_price, low_price, " \
                   "close_price, adj_close_price, volume) values (%s, %s, %s, %s, %s, %s, %s, %s)"
    print(insert_query)

    if len(float_col_str) == 0 and len(int_col_str) == 0:
        log_info('Numeric fields does not exist, hence no data type conversion will be applied.')
        conversion_needed = False

    if conversion_needed:
        float_col_str = float_col_str.split(',')
        int_col_str = int_col_str.split(',')
        float_col_list = [int(col) for col in float_col_str]
        int_col_list = [int(col) for col in int_col_str]

    with open(file_name, 'r') as in_file:
        csv_data = csv.reader(in_file)
        skip_rec = True
        for row_data in csv_data:
            if not skip_rec:
                tmp_data = convert_datatype(stock_id, row_data, float_col_list, int_col_list)
                if tmp_data is not None:
                    processed_data.append(tmp_data)
            skip_rec = False

    mysql_db = MysqlConnector(mysql_conn, chunk_size)
    try:
        mysql_db.insert_records(insert_query, processed_data)
    except Exception as e:
        log_error("Error occurred while inserting records - {}".format(e))
    finally:
        mysql_db.close_conn()









