from progress import Status
from docker import from_env
from config import ConfigLoader

class Pipeline(object):
    def __init__(self):
        self.docker_client = from_env()

    def start(self):
        try:
            self.network       =  self.__network()
            self.elasticsearch =  self.docker_client.containers.run('elasticsearch:5.4', network='logcast' , ports={'9200/tcp': 9200, '9300/tcp': 9300}, detach=True, name='elasticsearch')
            self.kibana        =  self.docker_client.containers.run('kibana:5.4', network='logcast', ports={'5601/tcp': 5601}, detach=True, name='kibana', links=[('elasticsearch', 'elasticsearch')])
            self.logstash      =  self.docker_client.containers.run('logstash:5', '--pipeline.unsafe_shutdown -f /etc/logstash/conf.d/', 
                volumes={
                    ConfigLoader.LOGSTASH_CONFIGS_PATH : {
                        'bind': '/etc/logstash/conf.d/', 'mode': 'ro'
                    }
                },
                ports={'5044/tcp': 5044}, 
                network='logcast',
                name='logstash',
                detach=True,
                links=[('elasticsearch', 'elasticsearch')]
            )
            Status.show('The containers has been created', True)
        except:
            Status.show('Something went wrong creating containers, please use the debug flag to troubleshoot the issue', False)

    def stop(self):
        try:
            self.elasticsearch.remove(force=True)
            self.logstash.remove(force=True)
            self.kibana.remove(force=True)
            self.network.remove()
            Status.show('The containers has been stopped/deleted', True)
        except:
            Status.show('Something went wrong stoping containers, please use the debug flag to troubleshoot the issue', False)            

    def __network(self):
        return self.docker_client.networks.create("logcast", driver="bridge")

    
# containers = Pipeline()
# containers.start()
# sleep(400)
# containers.stop()