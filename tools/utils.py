import os
import logging
import re
import sys
import getpass

import exceptions


def execute_command(cmd, execute, echo=True):
    """Execute a command in shell or just print it if execute is False"""
    if execute:
        if echo:
            print "Executing: " + cmd
        return os.system(cmd)
    else:
        print cmd
        return 0

def set_log_level(level):
    """Sets the desired log level."""
    lLevel = level.lower()
    unrecognized = False
    if (lLevel == 'debug-all'):
        loglevel = logging.DEBUG
    elif (lLevel == 'debug'):
        loglevel = logging.DEBUG
    elif (lLevel == 'info'):
        loglevel = logging.INFO
    elif (lLevel == 'warning'):
        loglevel = logging.WARNING
    elif (lLevel == 'error'):
        loglevel = logging.ERROR
    elif (lLevel == 'critical'):
        loglevel = logging.CRITICAL
    else:
        loglevel = logging.DEBUG
        unrecognized = True
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d/%(funcName)s: %(message)s')
    console = logging.StreamHandler()
    console.setLevel(loglevel)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(loglevel)
    #logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d/%(funcName)s: %(message)s', level=loglevel)
    if lLevel != 'debug-all':
        # lower the loglevel for enumerated packages to avoid unwanted messages
        packagesWarning = ["requests.packages.urllib3", "urllib3", "requests_kerberos", "jenkinsapi"]
        for package in packagesWarning:
            logging.debug("Setting loglevel for %s to WARNING.", package)
            logger = logging.getLogger(package)
            logger.setLevel(logging.WARNING)

    if unrecognized:
        logging.warning('Unrecognized log level: %s  Log level set to debug', level)

    #TODO ref: use external log config
    fh = logging.FileHandler('builder.log')
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)
    logging.getLogger('').addHandler(fh)

def get_dir(f):
    return os.path.dirname(os.path.realpath(f))

def canonize_url(url):
    """Modify URL to a standardized format (e.g. add slash at the and if it is
    not there.)

    :return: canonized URL
    """

    # add slash at the and if it's not there
    if not re.match(".*/$", url):
        url = url + "/"

    return url

def canonize_path(path):
    """Modify path to a standardized format (e.g. add ./ at the beginning if
    it's a relative path and it's not there)

    :return: canonized path
    """

    # add ./ at the begining if relative url
    if not re.match("^\.?/", path):
        path = "./" + path

    return path

def parse_conf_args(argv):
    """Parse command line options into {section: (option, key)} which can be
    used for overlaying on top of config

    :param argv: list of argumets to be parsed
    :return: Dictionary in the following format: {section: (option, key)}"""

    args = {}
    for rarg in argv:
        if re.match("^--.*", rarg):
            arg = rarg.replace('--','', 1)

            fsplit = arg.split('=', 1)
            if len(fsplit) != 2:
                raise exceptions.InvalidOptionError(
                    "Command option '%s' not recognized." % rarg)

            rkey, value = fsplit
            ssplit = rkey.split('.', 1)
            if len(ssplit) != 2 or not ssplit[1]:
                raise exceptions.InvalidOptionError(
                    "Command option '%s' not recognized." % rarg)

            section, option = ssplit
            args[section] = (option, value)
        else:
            raise exceptions.InvalidOptionError(
                    "Command option '%s' not recognized." % rarg)

    return args

def get_user_creds():
    """Promt user for credentials.

    :return: Pair of username (first) and password (second).
    """
    print "Please provide your JIRA credentials"
    username = raw_input("Username: ")
    password = getpass.getpass()

    return (username, password)

def required(field):
    """Decorator that checks if return value is set, if not, raises exception.
    """

    def wrap(f):
        def wrappedf(*args):
            result = f(*args)
            if result is None or result == "":
                raise exceptions.InvalidConfigError(
                    "Config option '%s' is required." % field)
            else:
                return result
        return wrappedf
    return wrap

def is_dr(version):
    return re.match(".*(\.|-)dr\d(\.|-).*", version.lower())

# https://stackoverflow.com/questions/18092354/python-split-string-without-splitting-escaped-character
# http://www.sieswerda.net/2010/10/08/splitting-strings-while-not-ignoring-escape-characters/
def split_unescape(s, delim, escape='\\', unescape=True):
    """
        >>> split_unescape('foo,bar', ',')
        ['foo', 'bar']
        >>> split_unescape('foo$,bar', ',', '$')
        ['foo,bar']
        >>> split_unescape('foo$$,bar', ',', '$', unescape=True)
        ['foo$', 'bar']
        >>> split_unescape('foo$$,bar', ',', '$', unescape=False)
        ['foo$$', 'bar']
        >>> split_unescape('foo$', ',', '$', unescape=True)
        ['foo$']
        """
    ret = []
    current = []
    itr = iter(s)
    for ch in itr:
        if ch == escape:
            try:
                # skip the next character; it has been escaped!
                if not unescape:
                    current.append(escape)
                current.append(next(itr))
            except StopIteration:
                if unescape:
                    current.append(escape)
        elif ch == delim:
            # split! (add current to the list and reset it)
            ret.append(''.join(current))
            current = []
        else:
            current.append(ch)
    ret.append(''.join(current))
    return ret
