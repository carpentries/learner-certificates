# Certificates for The Carpentries

## Using the python program

The python program makes use of the `cairosvg` package and supports reading a csv file containing participants using the `pandas` package. You can either install the python package or run it directly from this repo.

```
python3 -m learner_certificates.certificates -h
```

## Using jinja2 directly

The second, pure python method uses the python packages jinja2, jinja2-cli and svglib to build the certificates.

To build certificates this way, you can run:
```
jinja2 learner_certificates/templates/swc-attendance.svg \
   -D name="Firstname Lastname" -D date="Nov. 6, 2017" \
   -D instructor="Some Instructor Name" > lastname_firstname.svg
svg2pdf lastname_firstname.svg 
```

