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

Many people prefer to install python modules with VirtualEnv.  If you
choose to do this, perform within the src directory:

```virtualenv gsascraper
pip install -r ../requirements.txt
```

If you don't care to use it, then  simply execute:

- `pip install -r requirements.txt`

In the main effect.

## Other Usage

To make this useful, we support both a command-line usage and a CGI
usage.

The command line usage is simple:

```
python gsa-scrape-commandline.py
```

However, we normally used this a web-service API, and therefore host
it with Apache.  Although there are many ways to do this, I prefer to
do it as a virtual host.  This requires two steps:  Adding an entry to
/etc/hosts file and adding a VirtualHost entry to your apche
configuration.

The example configuration looks like this:
```
<VirtualHost gsa-advantage-scraper:80>
    ServerName gsa-advantage-scraper
    ScriptAlias /cgi-bin/ /Users/robertread/projects/gsa-advantage-scrape/src/ \

      DocumentRoot /Users/robertread/projects/gsa-advantage-scrape/src
       <Directory "/Users/robertread/projects/gsa-advantage-scrape/src">
            Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
            Order allow,deny
            AllowOverride None
            Allow from all
            DirectoryIndex index.php
            AddHandler cgi-script .py .cgi
      </Directory>
</VirtualHost>
```

Depending on whether have used the "VirtualEnv" installation method
above or have installed your python packages where they can be reached
without VirtualEnv, you should access gsa-adv-cart-ve.py or
gsa-adv-cart.py.

### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
