import getpass
import json
import os
import requests
from bs4 import BeautifulSoup
import logging
import re
logging.basicConfig(filename='scraper.log',level=logging.ERROR)


# Set some other things, like the login url for GSA Advantage
root_url = "https://www.gsaadvantage.gov"
login_url = "%s/advantage/main/login.do" % root_url
login_post_url = "%s/advantage/main/login_in.do" % root_url
retrieve_cart_url = "%s/advantage/parkcart/retrieve_parkcart.do" % root_url
# cartNum=XXX must be added to this
retrieve_cart_details_url = "%s/advantage/parkcart/addToCart.do" % root_url


def parse_detail_rows(detail_rows):
  parsed_rows = []
  i = 0
  for row in detail_rows:
    cart_item = {}
    columns = row.find_all('td')
# 'notes' is untested
    cart_item['notes'] = columns[1].getText().strip()
    cart_item['partNumber'] = columns[3].getText().strip()
    cart_item['description'] = columns[5].b.getText()
    cart_item['vendor'] = columns[7].string.strip()

# details is ugly, I have little choice but to do some sort 
# of whitespace cleansing...
    cart_item['details'] = ' '.join(columns[8].getText().split())

# Let's hope this is really an integer, but I'm going to 
# let the consumer worry about that.
    cart_item['qty'] = columns[9].input['value']

# this needs some error-checking...but they put a weird link
# into this which we need to cut out...
    cart_item['price'] = columns[11].getText().strip().split()[0]

    parsed_rows.append(cart_item)
    i = i + 1
  return parsed_rows

def add_url_from_product_table(analyzed_rows,product_rows):
  i = 0

  for row in analyzed_rows:
    prow = product_rows[i]
    product_url = prow.find('a')['href']

    # We'll just print out some info here
    row['url'] = product_url
    i = i + 1
  return analyzed_rows

# Quick script to get the token of the session so that we can login
def token_get(s):
  page = s.get(login_url).text
  soup = BeautifulSoup(page)
  #print soup.title
  token_tag = soup.find('input', attrs={'name':'org.apache.struts.taglib.html.TOKEN', 'type':'hidden'})
  return token_tag['value']

def find_checked_row(items):
# This is a little tricky...we need to figure out how to find the one checked value.
  i = 0
  for item in items:
    checked = item.find('input', attrs={'checked':'checked'})
    if (checked is not None):
      return item
    i = i + 1

  print "Whoops, didn't find a checked value, probably a giant problem!"
  raise Error("Couldn't find the checked Item!");

def map_features(features):
  map_f = []
  pattern = r'.*/(\w+).gif'
  for f in features:
    m = re.match(pattern, repr(f))
    if (m):
      map_f.append(m.groups()[0])
  return map_f


def addIndividualItem(s,row):
  item_page = s.get(root_url+row['url']).text
  soup = BeautifulSoup(item_page)
  item_table = soup.find('table', attrs={'class':'greybox'}).find_all('tr')
  checked_row = find_checked_row(item_table)

  tds = checked_row.find_all('td')
  i = 0
  for itd in tds:
    i = i+1

  features = tds[6].find_all('img')
  abstract_features = map_features(features)

  socio = tds[10]
  anchors = socio.find_all("a")
  j = 0
  socio_agg = ""
  for ans in anchors:
    socio_agg = ans.getText() + socio_agg
    j = j + 1

  green = tds[13].getText()

  if (green == u'\xa0'):
    green = ""

  row['green'] = green
  row['socio'] = socio_agg
  row['features'] = repr(abstract_features)


# Return the cart as an array of dictionaries
def getCart(GSAAdvantage_userName,GSAAdvantage_password,GSAAdvantage_cartNumb):
  logging.debug('username '+GSAAdvantage_userName)
  logging.debug('password '+GSAAdvantage_password)
  logging.debug('cartNumb '+GSAAdvantage_cartNumb)
  
  # We'll use requests to login and get to the cart page
  s = requests.Session()

  # Setting the payload for the login
  login_payload = {
    "userName": GSAAdvantage_userName,
    "password": GSAAdvantage_password,
    "mapName": "",
    "map": "forgotPassword",
    "addressMap": "false",
    "productOID": "",
    "org.apache.struts.taglib.html.TOKEN": token_get(s),
  }
  
  # We'll login now
  s.post(login_post_url, data=login_payload)
  
  # We'll now get the content of the cart
  cart_payload = {
    'cartNumber': GSAAdvantage_cartNumb,
    'cartPassword': "",
    'retrieveCart': "true"
  }
  
  cart_page = s.post(retrieve_cart_url, data=cart_payload).text
  soup = BeautifulSoup(cart_page)
  product_table = soup.find('table', attrs={'class':'sectionpanel4'}).find('table', attrs={'class':'greybox'}).find_all('tr')

  retrieve_cart_details_url_with_num = retrieve_cart_details_url+"?cartNum=%s" % GSAAdvantage_cartNumb

  cart_detail_page = s.get(retrieve_cart_details_url_with_num)
  
  # Surprisingly, this partially works, not sure what that means...
  # cart_detail_page = requests.get(retrieve_cart_details_url_with_num)
  soup = BeautifulSoup(cart_detail_page.text)
  
  form = soup.find_all('form')[2]
  first_table = form.find_all('table')[0]
  detail_table = first_table.find_all('table')[2]
  data_rows = detail_table.find_all('tr')[1:-2]
  detail_rows = data_rows[:-1]
  
  analyzed_rows = parse_detail_rows(detail_rows)
  product_rows = product_table[1:]
  analyzed_rows = add_url_from_product_table(analyzed_rows,product_rows)

  for row in analyzed_rows:
    addIndividualItem(s,row)
    
  return analyzed_rows
