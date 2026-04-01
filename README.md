# Certificates for The Carpentries

## Centrally-Organised Workshops

If you would like to give certificates of attendance to learners at your Centrally-Organised Workshop, please contact team@carpentries.org so we can assist you.

## Self-Organised Workshops 

If you are hosting a Self-Organised Workshop, you may generate certificates for your learners based on the templates in this repo.

There are two ways to build certificates from this repo.

One uses the `cairosvg` Python package. To use this method, use `bin/certificates.py` to build certificates.  Usage instructions are in the `certificates.py` Python script.

The second method uses the Python packages `jinja2`, `jinja2-cli` and `svglib` to build the certificates.

To build certificates this way, you can run these two bash commands. The first creates an svg file and the second converts it into a pdf.

```
$ jinja2 swc-attendance.svg -D name="Firstname Lastname" -D date="Nov. 6, 2017" -D instructor="Some Instructor Name" > "lastname_firstname.svg"
$ svg2pdf lastname_firstname.svg lastname_firstname.pdf
```

## Certificate Templates

We offer certificate templates for standard Data Carpentry, Library Carpentry, and Software Carpentry workshops.  We do not offer templates for non-standard workshops, such as mix-and-match, Incubator, or Lab workshops.  
