# GSA Advantage Cart Scrape

This is a really simple script to scrape a parked cart from GSA Advantage.

Thaks to Sean Herron (https://github.com/seanherron) for doing the breakthrough work.  I have just filled in details.

# Reason for Existence

To some extent this is experimental. If you aren't a Federal government user of GSA Advantage! 
or have to wish to server those users, this code is only valuable to use as an example, if that.

We are building a "spike" that re-utilizes GSA Advantage's excellent shopping cart building 
capabilities.  Our goal is to build a searchable database of shopping carts and to smooth 
the process of communication around carts.  This project could be considered a part of the project
here at github codenamed "mario" (https://github.com/18F/Mario), but I am making this repo stand-alone in hopes of greater
reuse.

We of course invite assistance, but this is not the best project to help on, due to its
very "spikey" nature, so I am not opening any issues at present---but improving my Python code
is generally easy to do!

## Requirements
- `requests`
- `beautifulsoup4`


## Installation

- `pip install -r requirements.txt`
- `python gsa-advantage.py`

## Other Usage

I am currently building this as a web-service.

To test, you can run "python gsa-advantage-py".

### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
