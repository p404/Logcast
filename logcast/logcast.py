#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from pathlib import Path
from scp import SCPClient
from cli import LogcastCLI
from progress import Status
from config import ConfigLoader
from paramiko import SSHClient, SSHConfig, ProxyCommand

HOME_PATH = str(Path.home())

class Logcast(object):
    def file_handling(self, path):
        file = open(path, 'r')
        return file.read()

    def remote_file(self, host, remote_file, log_type):
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
        # Make this else more generic
        else:
            user_config = config.lookup(host)
            ssh.connect(host, username=user_config['username'], port=user_config['port'])

        scp = SCPClient(ssh.get_transport())

        scp.get(remote_file, "{}/input/{}.log".format(ConfigLoader.LOGSTASH_CONFIGS_PATH, log_type))
        Status.show('File {}.log has been successfuly created'.format(log_type), True)
        scp.close()

def main():
    Status.startup()
    log = Logcast()
    log.remote_file('dev1.east', '/home/pablo/test2.txt', 'ubiome-pepito')
    # with LogcastCLI() as app:
    #     app.run()

if __name__ == "__main__":
    main()