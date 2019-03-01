from status import Status
from app import Logcast
from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose

class BaseController(ArgparseController):
    class Meta:
        label = 'base'
        description = "Logcast, Tool for generating configuration files for logstash"
        ignore_unknown_arguments = True


    def default(self):
        self.app.args.print_help()

class IngestController(ArgparseController):
    class Meta:
        label = 'ingest'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose(arguments=[
                (['--file_path', '-f'], {'help': 'log file path to be ingested', 'action':'store'}),
                (['--name', '-n'], {'help': 'name type for the templates', 'action': 'store'})
            ],
            help="ingest log files to create templates"
    )
    def ingest(self):
        if self.app.pargs.file_path and self.app.pargs.name:
            self.app.log.info(self.app.pargs.file_path)
        else:
            self.app.log.error('please fill the arguments')

    @expose(arguments=[
                (['--remote_server', '-r'], {'help': 'remote server', 'action': 'store'}),
                (['--file_path', '-f'], {'help': 'remote Log file path to be ingested', 'action': 'store'}),
                (['--type', '-t'], {'help': 'filter type name', 'action': 'store'})
            ],
            help="connect to a remote server and download log files to ingest them"
    )
    def remote_ingest(self):
        if self.app.pargs.file_path and self.app.pargs.type and self.app.pargs.remote_server:
            Status.startup()
            Logcast().analyze(self.app.pargs.remote_server, self.app.pargs.file_path, self.app.pargs.type, 'remote')
        else:
            self.app.log.error('please fill the arguments')

class LogcastCLI(CementApp):
    class Meta:
        label = 'logcast'
        handlers = [BaseController, IngestController]
