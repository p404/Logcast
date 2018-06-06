# -*- coding: UTF-8 -*-
import os
import sys
import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self):
        config_file = Path(os.path.join(Path.home(), '.logcast', 'config.yml'))
        if config_file.is_file():
            self.CFG = self._config_open(config_file)['logcast']
        else:
            self._config_init(config_file)

    def _ask_input(self, message):
        yes = {'yes','y', 'ye', ''}
        no = {'no','n'}

        choice = input(message).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'")
            sys.exit()

    def _config_init(self, config_file):
        example_config = {'logcast': {'filters_deploy_folder': 'ops-tools/roles/setup_logstash/files', 'filters_configs_path' : '/tmp' }}

        print('ERROR: There is no configuration file at {}'.format(config_file))
        if self._ask_input('INFO: Do you want generate a example config? y/n : '):
            if config_file.parent.is_dir():
                with open(config_file, 'w') as yaml_file:
                    yaml.dump(example_config, yaml_file, default_flow_style=False)
                sys.exit()
            else:
                os.makedirs(config_file.parent)
                if config_file.parent.is_dir():
                    with open(config_file, 'w') as yaml_file:
                        yaml.dump(example_config, yaml_file, default_flow_style=False)
                sys.exit()

    def _config_open(self, config_file):
        with open(config_file, 'r') as ymlfile:
            return yaml.load(ymlfile)

