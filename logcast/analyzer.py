import re
from json import loads
from random import choice
from pprint import pprint
from progress import Status
from dateutil.parser import parse

class Audit(object):
    def load_data(self, log_file_path):
        try:
            data = []
            with open(log_file_path) as file:
                for line in file:
                    data.append(loads(line))
            Status.show('The log file has valid JSON objects separated by lines, Number of items: {}'.format(len(data)), True)
            date = self.__parse(data)            
            return data
        except:
            Status.show('Something went wrong parsing {}.log'.format(log_file_path), False)

    def __parse(self, data):
        log_line = choice(data)

        for item in log_line:
            if self.__date_checker(log_line[item]):
                Status.show('A date value has been found: {}'.format(item), True)
                return self.__date_checker(log_line[item])

    def __date_checker(self, date_text):
        try:
            date_parsed = re.match("(\d{4})-(\d{2})-(\d{2})[\s](\d{2}):(\d{2}):(\d{2})[,](\d{3}$)", date_text)
            date_parsed.groups()
            return date_parsed
        except ValueError:
            raise ValueError("Incorrect data format, should be yyyy-MM-dd HH:mm:ss,SSS")