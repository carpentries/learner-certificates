#!/bin/sh

if [[ $# -eq 0 ]]; 
then
	echo "makecert.sh <source.svg> <context> <outputfile.pdf>"
fi

# Check for jinja2 
command -v jinja2 >/dev/null 2>&1 || { echo >&2 "This scripts requires jinja2-cli but it's not installed. Install with `pip install jinja2-cli`.  Aborting."; exit 1; }
# Check for svg2pdf
command -v svg2pdf>/dev/null 2>&1 || { echo >&2 "This script requires svg2pdf, a part of svglib. Install with `pip install svgilib`. Aborting."; exit 1; }

source_svg=${1}
context=${2} 
certout_pdf=${3}
certout_svg=${certout_pdf/.pdf/.svg}

jinja2 ${source_svg} ${context} > ${certout_svg} # fill template

svg2pdf ${certout_svg} # convert to PDF


