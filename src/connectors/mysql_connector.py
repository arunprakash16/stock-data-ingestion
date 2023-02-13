from mysql import connector as mysql_connect
from mysql.connector import errorcode
from src import log_error, log_info


class MysqlConnector:
    """
    MysqlConnector class handles connect and sql execution calls to mysql
    """
    __db_conn_keys = ['user', 'password', 'host', 'database']

    def __init__(self, mysql_config, chunk_size):
        """
        :param
        :param mysql_config: (dict) database connection details - user, password, host, database
        """
        MysqlConnector.__parm_validator(mysql_config)
        self.__chunk_size = chunk_size
        try:
            self.__conn = mysql_connect.connect(**mysql_config)
            log_info("Connected to MySql!")
            self.__cursor = self.__conn.cursor()
        except mysql_connect.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log_error("MySql credentials invalid.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                log_error("Database does not exist")
            else:
                log_error(err)

    @staticmethod
    def __parm_validator(config):
        parm_valid = True
        if not isinstance(config, dict):
            log_error('MySql configuration should be dictionary')
            exit(777)
        sql_parm = config.keys()
        for db_conn_key in MysqlConnector.__db_conn_keys:
            if parm_valid and db_conn_key not in sql_parm:
                parm_valid = False
                log_error('MySql configuration has to have {} information to connect.'.format(db_conn_key))
                exit(778)

    def commit_changes(self):
        self.__conn.commit()

    def insert_record(self, sql_query, sql_data):
        self.__cursor.execute(sql_query, sql_data)
        log_info('Data has been inserted: {}'.format(self.__cursor.lastrowid))
        self.commit_changes()

    def insert_records(self, sql_query, sql_data):
        sql_data_len = len(sql_data)
        start_pos = 0
        end_pos = self.__chunk_size
        if self.__chunk_size > sql_data_len:
            self.__cursor.executemany(sql_query, sql_data)
        else:
            loop_thru = True
            while loop_thru:
                self.__cursor.executemany(sql_query, sql_data[start_pos:end_pos])
                start_pos = end_pos

                if sql_data_len == end_pos:
                    loop_thru = False
                elif sql_data_len > (end_pos + self.__chunk_size):
                    end_pos += self.__chunk_size
                else:
                    end_pos = sql_data_len

        log_info('Data has been inserted: {}'.format(self.__cursor.lastrowid))
        self.commit_changes()

    def select_records(self, sql_query, sql_parm):
        return_code = 0
        query_out = list()
        if len(sql_parm) > 0 and not isinstance(sql_parm, tuple):
            log_error('Parameter for sql should be tuple, but received {}.'.format(type(sql_parm)))
            return_code = 1

        if return_code == 0:
            self.__cursor.execute(sql_query, sql_parm)
            query_out = self.__cursor.fetchall()
        return return_code, query_out

    def close_conn(self):
        self.__cursor.close()
        self.__conn.close()
