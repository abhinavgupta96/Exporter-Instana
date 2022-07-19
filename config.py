import configparser
import re
from time import process_time_ns

def build_config():
    config_parser = configparser.ConfigParser()
    try:
        config_parser.read('config/config.ini')
        config_api = dict(config_parser["API CONFIG"])
        return config_api
    except:
        raise Exception('Improper configuation of config/config.ini, see sample configuration')
    

def build_auth():
    config_parser = configparser.ConfigParser()
    try:
        config_parser.read('config/config.ini')
        config_api = dict(config_parser["API AUTH"])
        return config_api
    except:
        raise Exception('Improper configuation of config/config.ini, see sample configuration')

    

