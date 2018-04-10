from elasticsearch import Elasticsearch
from pprint import pprint

class Queries(object):
    def __init__(self, log_data, filter_type):
        self.es_client = Elasticsearch()
        pprint(self.__all_documents_count(filter_type))

    def __all_documents_count(self, filter_type):
        filter_wildcard = filter_type + '-*'
        result = self.es_client.count(index=filter_wildcard)
        return result['count']

    def __document_time(self):
        pass

data = ['one', 'two', 'tree']

Queries(data, 'ubiome-collections')