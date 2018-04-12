import time
from progress import Status
from elasticsearch import Elasticsearch

class Queries(object):
    def __init__(self, log_data, filter_type):
        time.sleep(55)
        self.es_client = Elasticsearch()        
        self.__all_documents_count(log_data, filter_type)

    def __all_documents_count(self, log_data, filter_type):
        filter_wildcard = filter_type + '-*'
        result = self.es_client.count(index=filter_wildcard)

        if result['count'] == len(log_data):
            Status.show('The created Elasticserach index {} has the same amount of items {} as the {}.log'.format(filter_type, result['count'], filter_type), True)   
        else:
            Status.show('The {} index data count {} differs from the ingested log, please check the filters'.format(filter_type, result['count']), False)

    def __document_time(self):
        pass
