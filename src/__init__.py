import os
import sys
import logging
from configparser import ConfigParser

sys.path.append('../../')

relative_config_path = '../../conf/config.cfg'
conf = ConfigParser()


def log_warning(warn_msg):
    logging.warning(warn_msg)


def log_error(error_msg):
    logging.error(error_msg)


def log_debug(debug_msg):
    logging.debug(debug_msg)


def log_info(info_msg):
    logging.info(info_msg)


def get_file_path(root_section, option):
    data_exist = False
    temp_file_path = ''
    if conf.has_option(root_section, option):
        data_exist = True
        temp_file_path = conf.get(root_section, option)
    return data_exist, temp_file_path


def check_file_existence(file_path, hard_stop=False, msg_prefix=''):
    file_exist = False
    if os.path.exists(file_path):
        file_exist = True
    elif hard_stop:
        log_error(msg_prefix + ' does not exist, hence skipping further process!')
        exit(777)
    return file_exist


def conf_file_read():
    if check_file_existence(relative_config_path, True, 'Configuration file'):
        conf.read(relative_config_path)


def get_env_var_data(key):
    return os.environ.get(key)


conf_file_read()
