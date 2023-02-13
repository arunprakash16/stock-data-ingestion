import argparse

from src import log_info, check_file_existence, log_debug
from src.batch_process.process_csv import process_csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSV file batch load Command Usage')
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-fp', '--filepath', required=True, action="store", dest="file_path",
                                help='CSV File path with file name')
    optional_named = parser.add_argument_group('optional named arguments')
    optional_named.add_argument('-cfs', '--config-float-section', required=False, action='store_true',
                                default='data_format', dest='conf_section',
                                help='Section name to look in config to identify numeric fields in the csv file.')
    optional_named.add_argument('-cfk', '--config-float-key', required=False, action='store_true',
                                default='float_col_pos', dest='conf_foat_key',
                                help='Key name to look in config to identify float fields in the csv file.')
    optional_named.add_argument('-cik', '--config-int-key', required=False, action='store_true',
                                default='int_col_pos', dest='conf_int_key',
                                help='Key name to look in config to identify int fields in the csv file.')

    args = parser.parse_args()
    log_info('Provided file path: {}, configuration section & key {} - {}, {}.'.format(args.file_path,
                                                                                       args.conf_section,
                                                                                       args.conf_foat_key,
                                                                                       args.conf_int_key))

    if check_file_existence(args.file_path):
        log_debug('Provided file path is valid.')
        process_csv(args.file_path, args.conf_section, args.conf_foat_key, args.conf_int_key)
