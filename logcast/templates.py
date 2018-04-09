from os import path
from progress import Status
from config import ConfigLoader 
from jinja2 import Environment, FileSystemLoader

TEMPLATES_FOLDER = path.dirname(path.abspath(__file__)) + '/templates'

class FilterTemplates(object):

    def __init__(self, filter_name):
        self.jinja = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER),trim_blocks=True)

        self._input_template(filter_name)
        self._filter_template(filter_name)
        self._output_template(filter_name)

    def _input_template(self, filter_name):
        input_file = '/etc/logstash/conf.d/input/' + filter_name + '.log'
        input_template_content = self._render('input.j2', type=filter_name, input_file=input_file )
        
        dest_file = ConfigLoader.LOGSTASH_CONFIGS_PATH + '/input.conf'
        self._create_file(input_template_content, dest_file)

    def _filter_template(self, filter_name):
        filter_template_content = self._render('filter.j2', type=filter_name )

        dest_file = ConfigLoader.LOGSTASH_CONFIGS_PATH + '/filter_' + filter_name + '.conf' 
        self._create_file(filter_template_content, dest_file)

    def _output_template(self, filter_name):
        output_template_content = self._render('output.j2', type=filter_name )

        dest_file = ConfigLoader.LOGSTASH_CONFIGS_PATH + '/output_' + filter_name + '.conf' 
        self._create_file(output_template_content, dest_file)

    def _render(self, template_file, **kwargs):
        return self.jinja.get_template(template_file).render(kwargs)
    
    def _create_file(self, content, path):
        with open(path, 'w') as file:
            file.write(content)
