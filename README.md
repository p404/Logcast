# Logcast (WIP)
Logcast is a configuration filters generator for logstash, it takes a log and ingest them to create the logstash filters.


## Installation
```bash
1. git clone https://github.com/p404/logcast.git
2. cd logcast
3. make install 
```

## Configuration
Configuration path $HOME/.logcast/config.yml
```yaml
logcast:
  filters_configs_path: /tmp
  filters_deploy_folder: /etc/logstash/conf.d/
```

## Command line (CLI)
```bash
$ logcast -h
    usage: logcast [-h] [--debug] [--quiet] {ingest,remote-ingest} ...

    Logcast, is here to help you creating parsing configuration files for logstash

    optional arguments:
    -h, --help            show this help message and exit
    --debug               toggle debug output
    --quiet               suppress all output

    sub-commands:
    {ingest,remote-ingest}
        ingest              ingest log files to create templates
        remote-ingest       connect to a remote server and download log files to
                            ingest them
```