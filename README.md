# Certificates for The Carpentries

## Learner Certificates

This repo has templates for Carpentries workshop Instructors to issue certificates to their learners for completing a Data, Library, or Software Carpentry workshop.  This certificates can be issued directly by Carpentries workshop Instructors to their learners.

Certificates issued direclty by the Carpentries include thos for Instructors, Maintainers, Trainers, and more.  For information about these certifcates, please contact team@carpentries.org.

## Building Certificates

There are two ways to build certificates from this repo.  

### Using Cairo

This method depends on the python package `cairosvg` which in turn depends on `cairo` development libraries being installed. To use this method, use `bin/certificates.py` to build certificates. This python script can take parameters to generate a single certificate or take a csv file to generate certificates in bulk.

Read more information in the [comments at the beginning of the python file](https://github.com/carpentries/learner-certificates/blob/main/bin/certificates.py).

### Using Jinja

This pure python method uses the python packages `jinja2`, `jinja2-cli`, and `svglib` to build the certificates. Each certificate will need to be generated individually.

To build certificates this way, you can run the following from your bash terminal.

```
jinja2 swc-attendance.svg -D name="Firstname Lastname" -D date="Nov. 6, 2017" -D instructor="Some Instructor Name" > lastname_firstname.svg
svg2pdf lastname_firstname.svg 
```

