#!/usr/bin/env python3

'''
Generate a certificate from a template.

* Requires the python package 'cairosvg' to be installed.
  Please visit http://cairosvg.org/ for install instructions.
* Some systems may also need to have 'cairo' installed.
  Please visit http://cairographics.org/download/ for the same.

On a Mac, a typical command line is

python -m learner_certificates.certificates \
       -b swc-instructor
       -o $HOME/sc/certification/ \
       -u turing_alan
       -d 'January 24, 1924' \
       -i 'Ada Lovelace' \
       -n 'Alan Turing'

where:

    -b:         BADGE_TYPE
    -o:         the OUTPUT_DIRECTORY
    -u:         USER_ID
    -d:         the date
    -i:         the name of the instructor
    -n:         the name of the participant

The script then creates $(OUTPUT_DIRECTORY)/$(BADGE_TYPE)/$(USER_ID).pdf as
output.

This script will also take a CSV file as input.  The file must contain rows of:

    name[,badge][,instructor][,user_id][,date]

such as:
    badge,instructor,user_id,name,date
    swc-instructor,Grace Hopper,turing_alan,Alan Turing,2016-01-27

Any missing columns are filled in from the command line optiomns. The order of
the columns does not matter.
'''

import sys
import pandas
import tempfile
import string
import argparse
from pathlib import Path
from datetime import date
import cairosvg
from jinja2 import Environment, PackageLoader, select_autoescape


DATE_FORMAT = '%B %-d, %Y'


def main():
    args = parse_args()

    env = Environment(
        loader=PackageLoader("learner_certificates"),
        autoescape=select_autoescape())

    if args.csv_file:
        check(args.csv_file.exists(), f"no such file {args.csv_file}")
        process_csv(args, env)
    else:
        process_single(args, env)


def construct_user_name(name):
    '''construct a username from the name by only allowing
    alphanumeric characters and replacing spaces with _'''
    valid_characters = string.ascii_letters + string.digits + '_'
    user_id = ''.join(
        ch for ch in name.replace(' ', '_') if ch in valid_characters)
    user_id = user_id.lower()
    return user_id


def parse_args():
    '''Get command-line arguments.'''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--badge', help='Type of badge')
    parser.add_argument(
        '-o', '--output-dir', default=Path.cwd(), type=Path,
        help='Output directory (current by default)')
    parser.add_argument(
        '-d', '--date', default=date.isoformat(date.today()),
        help='Date of certificate, defaults to today')
    parser.add_argument(
        '-i', '--instructor', help='Name of instructor')
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument(
        '-c', '--csv', type=Path, dest='csv_file', help='CSV file')
    grp.add_argument(
        '-n', '--name', help='Name of the participant')
    parser.add_argument(
        '-u', '--userid', dest='user_id',
        help='User ID, default construct from name')
    args = parser.parse_args()

    return args


def process_csv(args, env):
    '''Process a CSV file.'''

    data = pandas.read_csv(args.csv_file)
    if 'instructor' not in data.columns:
        check(args.instructor is not None, "need to specify instructor")
        data['instructor'] = args.instructor
    if 'date' not in data.columns:
        data['date'] = args.date
    if 'user_id' not in data.columns:
        data['user_id'] = data['name'].apply(construct_user_name)
    if 'badge' not in data.columns:
        check(args.badge is not None, "need to specify badge type")
        data['badge'] = args.badge
    for _, row in data.iterrows():
        create_certificate(args.output_dir, env, row)


def process_single(args, env):
    '''Process a single entry.'''

    check(args.instructor is not None, "need to specify instructor")
    check(args.badge is not None, "need to specify badge type")

    if args.user_id is None:
        user_id = construct_user_name(args.name)
    else:
        user_id = args.user_id

    params = {}
    for k in ['badge', 'instructor', 'name', 'date']:
        params[k] = getattr(args, k)
    params['user_id'] = user_id

    create_certificate(args.output_dir, env, params)


def create_certificate(output, env, params):
    '''Create a single certificate.'''

    params['date'] = date.fromisoformat(params['date']).strftime(DATE_FORMAT)

    template = env.get_template(params['badge'] + ".svg")
    badge_path = output / Path(params['badge'])

    if not badge_path.exists():
        badge_path.mkdir()
    outputpdf = badge_path / Path(params['user_id']).with_suffix('.pdf')

    tmp = tempfile.NamedTemporaryFile(suffix='.svg', delete=False)
    tmp.write(bytes(template.render(**params), 'utf-8'))
    cairosvg.svg2pdf(url=tmp.name, write_to=str(outputpdf), dpi=90)

    Path(tmp.name).unlink()


def check(condition, message):
    '''Fail if condition not met.'''

    if not condition:
        print(message, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
