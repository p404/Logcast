import yaml
import os
import configparser

CONFIG_DEFAULT_PATH = os.getcwd() + '/config.ini'

class ConfigLoader(object):
    config = configparser.ConfigParser()
    config.read(CONFIG_DEFAULT_PATH)
    
    LOGSTASH_CONFIGS_PATH = config.get('LOGCAST', 'logstash_configs_path')    

