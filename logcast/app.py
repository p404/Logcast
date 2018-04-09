from time import sleep
from pathlib import Path
from scp import SCPClient
from progress import Status
from containers import Pipeline
from config import ConfigLoader
from templates import FilterTemplates
from paramiko import SSHClient, SSHConfig, ProxyCommand

HOME_PATH = str(Path.home())

class Logcast(object):

    def analyze(self, host, file, filter_type, file_location):
        if file_location == 'remote':
            file_destination_path = self.__remote_file(host, file, filter_type)
            FilterTemplates(filter_type)
            containers = Pipeline()
            containers.start()
            # Here we are going to analyze the log
            # file_destination_path  
            # Here we are going the send the elasticsearch queries
            sleep(20)
            containers.stop()
    
    def __local_file(self, path):
        file = open(path, 'r')
        return file.read()

    def __remote_file(self, host, remote_file, log_type):
        config = SSHConfig()
        config.parse(open('{}/.ssh/config'.format(HOME_PATH)))

        ssh = SSHClient()
        ssh.load_system_host_keys()

        if '.east' in host:
            user_config = config.lookup('*.east')
            proxy = ProxyCommand('ssh -q {}@bastion.ubiome.com nc {} 22'.format(user_config['user'], host))
            ssh.connect(host, 
                    username=user_config['user'], 
                    sock=proxy,
                    port=user_config['port']
        )
        # TODO 
        # Make this more generic
        else:
            user_config = config.lookup(host)
            ssh.connect(host, username=user_config['username'], port=user_config['port'])

        scp = SCPClient(ssh.get_transport())

        try:
            file_dest = "{}/input/{}.log".format(ConfigLoader.LOGSTASH_CONFIGS_PATH, log_type)
            scp.get(remote_file, file_dest)
            Status.show('File {}.log has been successfuly created'.format(log_type), True)
            scp.close()
            return file_dest
        except:
            Status.show('Something went wrong creating {}.log'.format(log_type), False)
