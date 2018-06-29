import argparse
import json
import os
import sys
import time

try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib


__author__ = 'Karthik Nadig'
__version__ = '1.0.0a'

DOCKER_STAT_OK = 0

def _parse_args():
    prog = sys.argv[0]
    usage = """
     %s [-h|--help] [-V|--version] --repo REPO --file FILENAME
    """ % prog
    parser = argparse.ArgumentParser(
        prog=prog,
        usage=usage
    )

    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument('-V', '--version', action='version')
    parser.version = __version__
    return vars(parser.parse_args(sys.argv[1:]))


def process_command():
    args = _parse_args()

    req = url_lib.urlopen('https://hub.docker.com/v2/repositories/%s' % args['repo'])
    data = json.loads(req.read())
    msg = '%s, \"%s\", %s\n' % (str(time.time()),
                              time.asctime(),
                              str(data['pull_count']))

    filename = args['filename']
    if filename == 'stdout':
        print(msg)
    else:
        with open(filename, 'a') as fp:
            fp.write(msg)

    return DOCKER_STAT_OK


if __name__ == '__main__':
    process_command()

