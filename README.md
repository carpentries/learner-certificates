# Certificates for The Carpentries


There are two ways to build certificates from this repo, one depends on the python package cairosvg which in turn depends on cairo development libraries being installed. To use this method, use `bin/certificates.py` to build certificates.

The second, pure python method uses the python packages jinja2, jinja2-cli and svglib to build the certificates.

To build certificates this way, you can run:
```
jinja2 swc-instructor.svg -D name="Firstname Lastname" -D date="Nov. 6, 2017" -D instructor="Some Instructor Name" > lastname_firstname.svg
svg2pdf lastname_firstname.svg 
```

