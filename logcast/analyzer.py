from json import loads
from pprint import pprint
from progress import Status

class Audit(object):
    def __init__(self, log_file_path):
        self.load_data(log_file_path)

    def load_data(self, log_file_path):
        try:
            data = []
            with open(log_file_path) as file:
                for line in file:
                    data.append(loads(line))
            Status.show('The log file has valid JSON objects separated by lines, Number of items: {}'.format(len(data)), True)
            return data
        except:
            Status.show('Something went wrong parsing {}.log'.format(log_file_path), False)
