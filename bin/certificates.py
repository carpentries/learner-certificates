#!/usr/bin/env python3

'''
Generate a certificate from a template.

* Requires the python package 'cairosvg' to be installed.
  Please visit http://cairosvg.org/ for install instructions.
* Some systems may also need to have 'cairo' installed.
  Please visit http://cairographics.org/download/ for the same.

On a Mac, a typical command line is

python bin/certificates.py \
       -b swc-instructor
       -r $HOME/sc/certification/ \
       -u turing_alan
       date='January 24, 1924' \
       instructor='Ada Lovelace' \
       name='Alan Turing'

where:

    -b:         BADGE_TYPE
    -r:         ROOT_DIRECTORY
    -u:         USER_ID
    name=value: fill-ins for the template

The script then looks for $(ROOT_DIRECTORY)/$(BADGE_TYPE).svg as a template
file, and creates $(ROOT_DIRECTORY)/$(BADGE_TYPE)/$(USER_ID).pdf as output.

This script will also take a CSV file as input.  The file must contain rows of:

    badge,trainer,user_id,new_instructor,email,date

such as:

    swc-instructor,Grace Hopper,turing_alan,Alan Turing,alan@turing.org,2016-01-27

In this case, the command line invocation is:

python bin/certificates.py \
       -r $HOME/sc/certification/ \
       -c input.csv
'''

import sys
import os
import re
import csv
import tempfile
import subprocess
import unicodedata
from optparse import OptionParser
import time
from datetime import date
import cairosvg


DATE_FORMAT = '%B %-d, %Y'


def main():
    args = parse_args()
    if args.csv_file:
        process_csv(args)
    else:
        process_single(args)


def parse_args():
    '''Get command-line arguments.'''

    parser = OptionParser()
    # -i argument retained for backward incompatibility,
    #  not used anymore
    parser.add_option('-i', '--ink',
                      default='/Applications/Inkscape.app/Contents/Resources/bin/inkscape',
                      dest='inkscape',
                      help='[deprecated] Path to Inkscape')
    parser.add_option('-b', '--badge',
                      default=None, dest='badge_type', help='Type of badge')
    parser.add_option('-r', '--root',
                      default=os.getcwd(), dest='root_dir', help='Root directory (current by default)')
    parser.add_option('-u', '--userid',
                      default=None, dest='user_id', help='User ID')
    parser.add_option('-c', '--csv',
                      default=None, dest='csv_file', help='CSV file')

    args, extras = parser.parse_args()
    check(args.root_dir is not None, 'Must specify root directory')
    msg = 'Must specify either CSV file or both root directory and user ID'
    if args.csv_file is not None:
        check((args.badge_type is None) and (args.user_id is None), msg)
    elif args.badge_type and args.user_id:
        check(args.csv_file is None, msg)
    else:
        check(False, msg)

    args.params = extract_parameters(extras)
    if 'date' not in args.params:
        args.params['date'] = date.strftime(date.today(), DATE_FORMAT)

    return args


def extract_parameters(args):
    '''Extract key-value pairs from command line (checking for uniqueness).'''

    result = {}
    for a in args:
        fields = a.split('=')
        assert len(fields) == 2, 'Badly formatted key-value pair "{0}"'.format(a)
        key, value = fields
        assert key not in result, 'Duplicate key "{0}"'.format(key)
        result[key] = value
    return result


def process_csv(args):
    '''Process a CSV file.'''

    with open(args.csv_file, 'r') as raw:
        reader = csv.reader(raw)
        for row in reader:
            check(len(row) == 6, 'Badly-formatted row in CSV: {0}'.format(row))
            badge_type, args.params['instructor'], user_id, args.params['name'], email, args.params['date'] = row
            if '-' in args.params['date']:
                d = time.strptime(args.params['date'], '%Y-%m-%d')
                d = date(*d[:3])
                args.params['date'] = date.strftime(d, DATE_FORMAT)
            template_path = construct_template_path(args.root_dir, badge_type)
            output_path = construct_output_path(args.root_dir, badge_type, user_id)
            create_certificate(template_path, output_path, args.params)

def process_single(args):
    '''Process a single entry.'''

    template_path = construct_template_path(args.root_dir, args.badge_type)
    output_path = construct_output_path(args.root_dir, args.badge_type, args.user_id)
    create_certificate(template_path, output_path, args.params)


def construct_template_path(root_dir, badge_type):
    '''Create path for template file.'''

    return os.path.join(root_dir, badge_type + '.svg')


def construct_output_path(root_dir, badge_type, user_id):
    '''Create path for generated PDF certificate.'''

    badge_path = os.path.join(root_dir, badge_type)
    path_exists = os.path.exists(badge_path)

    if not path_exists:
        os.mkdir(badge_path)

    return os.path.join(badge_path, user_id + '.pdf')


def create_certificate(template_path, output_path, params):
    '''Create a single certificate.'''

    with open(template_path, 'r') as reader:
        template = reader.read()
    check_template(template, params)

    for key, value in params.items():
        pattern = '{{' + key + '}}'
        template = template.replace(pattern, value)

    tmp = tempfile.NamedTemporaryFile(suffix='.svg', delete=False)
    tmp.write(bytes(template, 'utf-8'))

    cairosvg.svg2pdf(url=tmp.name, write_to=output_path, dpi=90)


def check_template(template, params):
    '''Check that all values required by template are present.'''

    expected = re.findall(r'\{\{([^}]*)\}\}', template)
    missing = set(expected) - set(params.keys())
    check(not missing,
          'Missing parameters required by template: {0}'.format(' '.join(missing)))


def check(condition, message):
    '''Fail if condition not met.'''

    if not condition:
        print(message, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
