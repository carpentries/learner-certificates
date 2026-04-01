#!/bin/sh


if [ $# -le 2 ]; then
    echo "makecert.sh <source.svg> <outputfile.pdf> <jinja2 args>..."
    exit 1;
fi

# Check for jinja2
command -v jinja2 >/dev/null 2>&1 || { echo >&2 "This scripts requires jinja2-cli but it's not installed. Install with \`pip install jinja2-cli\`.  Aborting."; exit 1; }
# Check for svg2pdf
command -v svg2pdf>/dev/null 2>&1 || { echo >&2 "This script requires svg2pdf, a part of svglib. Install with \`pip install svglib\`. Aborting."; exit 1; }

source_svg="$1"

certout_pdf="$2"
certout_svg=${certout_pdf/.pdf/.svg}

shift 2


jinja2 "${source_svg}" "$@" > "${certout_svg}" # fill template

svg2pdf "${certout_svg}" # convert to PDF
