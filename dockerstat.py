import argparse
import json
import sys
import time

try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib


__author__ = 'Karthik Nadig'
__version__ = '1.0.0a'

DOCKER_STAT_OK = 0
DOCKER_STAT_API = 'https://hub.docker.com/v2/repositories/'


def _get_stat_url(repo):
    return '%s%s' % (DOCKER_STAT_API, repo)


def _parse_args():
    prog = sys.argv[0]
    usage = """
     %s [-h|--help] [-V|--version] [--file FILENAME] --repo REPO
    """ % prog
    parser = argparse.ArgumentParser(
        prog=prog,
        usage=usage
    )

    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--filename', type=str)
    parser.add_argument('-V', '--version', action='version')
    parser.version = __version__
    return vars(parser.parse_args(sys.argv[1:]))


def process_command():

    args = _parse_args()

    req = url_lib.urlopen(_get_stat_url(args['repo']))
    resp = req.read()
    if not isinstance(resp, str):
        resp = resp.decode('utf-8')
    data = json.loads(resp)
    msg = '%s, \"%s\", %s\n' % (str(time.time()),
                                time.asctime(),
                                str(data['pull_count']))

    try:
        filename = args['filename']
        if filename is None:
            print(msg)
        else:
            with open(filename, 'a') as fp:
                fp.write(msg)
    except KeyError:
        print(msg)

    return DOCKER_STAT_OK


if __name__ == '__main__':
    process_command()
