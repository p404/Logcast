from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose

class BaseController(ArgparseController):
    class Meta:
        label = 'base'
        description = "Logcast, is here to help you creating parsing configuration files for logstash"
        ignore_unknown_arguments = True

    def default(self):
        self.app.args.print_help()

class IngestController(ArgparseController):
    class Meta:
        label = 'else'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose(arguments=[
                (['--file_path', '-f'], {'help': 'Log file path to be ingested', 'action':'store'}),
                (['--name', '-n'], {'help': 'Name type for the templates', 'action': 'store'})
            ],
            help="Ingest log files to create templates"
    )
    def ingest(self):
        if self.app.pargs.file_path and self.app.pargs.name:
            self.app.log.info(self.app.pargs.file_path)
        else:
            self.app.log.error('Please fill the arguments')

    @expose(arguments=[
                (['--remote_server', '-r'], {'help': 'Remote server', 'action':'store'}),
                (['--file_path', '-f'], {'help': 'Log file path to be ingested', 'action':'store'}),
                (['--name', '-n'], {'help': 'Name type for the templates', 'action': 'store'})
            ],
            help="Connect to a remote server and download log files to ingest them"
    )
    def remote_ingest(self):
        if self.app.pargs.file_path and self.app.pargs.name:
            self.app.log.info(self.app.pargs.file_path)
        else:
            self.app.log.error('Please fill the arguments')

class LogcastCLI(CementApp):
    class Meta:
        label = 'logcast'
        handlers = [BaseController, IngestController]
