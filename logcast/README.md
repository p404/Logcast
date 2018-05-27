Logcast
=======

Logcast is a configuration filters generator for logstash, it takes a log and ingest them to create the logstash filterss


Installation
------------

Configuration
-------------

Config file
~~~~~~~~~~~
Config file example:
.. code:: ini
    [LOGCAST]
    logstash_configs_path = /path/to/a/folder


Command line (CLI)
~~~~~~~~~~~~~~~~~~

The CLI arguments that can
be used are:

::

$ logcast -h
    usage: logcast [-h] [--debug] [--quiet] {ingest,remote-ingest} ...

    Logcast, is here to help you creating parsing configuration files for logstash

    optional arguments:
    -h, --help            show this help message and exit
    --debug               toggle debug output
    --quiet               suppress all output

    sub-commands:
    {ingest,remote-ingest}
        ingest              Ingest log files to create templates
        remote-ingest       Connect to a remote server and download log files to
                            ingest them