# -*- coding: UTF-8 -*-
import os
import sys
import pick
from status import Status
from subprocess import run
from config import ConfigLoader

OUTPUT_FILTERS_PATH = ConfigLoader().CFG['filters_configs_path']
FILTERS_DEPLOY_PATH = ConfigLoader().CFG['filters_deploy_folder']

class FilterDeploy(object):
    def __init__(self, filter_type):
        if self._ask_input('Do you want to deploy this filter? y/n : '):
            try:
                deploy_script          =  os.path.dirname(os.path.realpath(__file__)) + '/contrib/deploy.sh'
                hub_binary             =  os.path.dirname(os.path.realpath(__file__)) + '/contrib/hub'
                filter_folders         =  self.__list_folders(FILTERS_DEPLOY_PATH)
                title_environment      =  'Please choose environment : '
                ENVIRONMENT, index_env =  pick.pick(filter_folders, title_environment)
                
                script = run([deploy_script, ENVIRONMENT, filter_type, FILTERS_DEPLOY_PATH, OUTPUT_FILTERS_PATH, hub_binary])
                if script.returncode == 0:
                    Status.show('The execution deployment of the {} script has been successful'.format(filter_type), True)
                else:
                    Status.show('Something went wrong with the execution of the deployment script {}'.format(filter_type), False)
                    sys.exit()
            
                Status.show('The deployment of the {} has been successful'.format(filter_type), True)   
            except:
                Status.show('Something went wrong with the deployment of the filter {}'.format(filter_type), False)


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

    def __list_folders(self, path):
        ignored = {".DS_Store", "etc"}
        return [x for x in os.listdir(path) if x not in ignored]
