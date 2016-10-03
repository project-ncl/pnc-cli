from argh import arg
from ConfigParser import Error, NoSectionError
from tools.config_utils import ConfigReader
import logging
import os
from pprint import pprint

@arg('-c', '--config', help='Configuration file to use to drive the build')
def make_mead(config="builder.cfg"):
    """
    Create Make Mead configuration
    :param config: Make Mead config name
    :return:
    """    
    if not os.path.isfile(config):
        logging.error('Config file %s not found.', os.path.abspath(config))
        return 1

    try:
        config_reader = ConfigReader(config)
    except NoSectionError as e:
        logging.error('Missing config in %s (%r)', config, e)
        print '-c false'
        return 1
    except Error, err:
        logging.error(err)
        print '-c false'
        return 1

    tasks = config_reader.get_tasks()

    pprint (vars(config_reader))
    pprint (vars(tasks))

    print("All found targets are " + ','.join('%s' % key for key in tasks.get_all().keys()));
    print("Building all artifacts...")

    return config
