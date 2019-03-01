from sys import stdout
from time import sleep
from pathlib import Path
from scp import SCPClient
from deploy import FilterDeploy 
from analyzer import Audit
from elastic import Queries
from config import ConfigLoader
from containers import Pipeline
from templates import FilterTemplates
from status import Status, StatusColors
from paramiko import SSHClient, SSHConfig, ProxyCommand

HOME_PATH = str(Path.home())
OUTPUT_FILTERS_PATH = ConfigLoader().CFG['filters_configs_path']

class Logcast(object):
    def analyze(self, host, file, filter_type, file_location):
        if file_location == 'remote':
            file_destination_path = self.__remote_file(host, file, filter_type)            
            log_data, date_key = Audit().load_data(file_destination_path)
            FilterTemplates(filter_type, date_key)
            containers = Pipeline()
            containers.start()
            Queries(log_data, filter_type)
            containers.stop()
            FilterDeploy(filter_type)
    def __local_file(self, path):
        file = open(path, 'r')
        return file.read()

    def __remote_file(self, host, remote_file, log_type):
        def __remote_progress(filename, size, sent):
            stdout.write("%s\'s : %.2f%%   \r" % (filename, float(sent)/float(size)*100) )
        
        config = SSHConfig()
        config.parse(open('{}/.ssh/config'.format(HOME_PATH)))

        ssh = SSHClient()
        ssh.load_system_host_keys()

        user_config = config.lookup(host)
        ssh.connect(host, username=user_config['username'], port=user_config['port'])

        scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x, progress=__remote_progress)

        try:
            file_dest = "{}/input/{}.log".format(OUTPUT_FILTERS_PATH, log_type)
            scp.get(remote_file, file_dest)
            Status.show('File {}.log has been successfuly created'.format(log_type), True)
            scp.close()
            return file_dest
        except:
            Status.show('Something went wrong creating {}.log'.format(log_type), False)
