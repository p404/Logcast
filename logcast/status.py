from datetime import datetime

class StatusColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Status(object):
    @staticmethod
    def startup():
        print(StatusColors.OKBLUE + StatusColors.BOLD + 'Starting Logcast {}'.format(datetime.now()) + StatusColors.ENDC)    
    @staticmethod
    def show(message, success):
        if success is True:
            print(message + StatusColors.OKGREEN + ' ' + 'done' + StatusColors.ENDC)
        else:
            print(message + StatusColors.FAIL + ' ' + 'fail' + StatusColors.ENDC)


