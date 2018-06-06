from status import Status
from docker import from_env
from config import ConfigLoader

OUTPUT_FILTERS_PATH = ConfigLoader().CFG['filters_configs_path']

class Pipeline(object):
    def __init__(self):
        self.docker_client = from_env()

    def clean(self):
        container_list = ['elasticsearch', 'kibana', 'logstash']
        for container in container_list:
            container_object = self.docker_client.containers.get(container)
            print(container_object)
                #container_object.remove(force=True)

    def start(self):
            self.network       =  self.__network()
            self.elasticsearch =  self.docker_client.containers.run('elasticsearch:5.4', network='logcast' , ports={'9200/tcp': 9200, '9300/tcp': 9300}, detach=True, name='elasticsearch', auto_remove=True)
            self.kibana        =  self.docker_client.containers.run('kibana:5.4', network='logcast', ports={'5601/tcp': 5601}, detach=True, name='kibana', links=[('elasticsearch', 'elasticsearch')], auto_remove=True)
            self.logstash      =  self.docker_client.containers.run('logstash:5', '--pipeline.unsafe_shutdown -f /etc/logstash/conf.d/', 
                volumes={
                    OUTPUT_FILTERS_PATH : {
                        'bind': '/etc/logstash/conf.d/', 'mode': 'ro'
                    }
                },
                ports={'5044/tcp': 5044}, 
                network='logcast',
                name='logstash',
                detach=True,
                auto_remove=True,
                links=[('elasticsearch', 'elasticsearch')]
            )
            Status.show('The containers has been created', True)

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