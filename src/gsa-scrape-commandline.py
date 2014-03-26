import getpass
import json
import os
import requests
from bs4 import BeautifulSoup

import gsa_advantage

def actLikeACommandLineProgram():
  # A URL like this appears to retrieve a cart in a way in which details can be done:
  # https://www.gsaadvantage.gov/advantage/parkcart/addToCart.do?cartNum=2865618
  # Temporarily Get User Credentials, you'll probably want to pass these some other way
  if ('GSAAdvantage_userName' in os.environ):
    GSAAdvantage_userName = os.environ['GSAAdvantage_userName']
  else:
    GSAAdvantage_userName = raw_input("Enter GSA Advantage Username: ")

  if ('GSAAdvantage_password' in os.environ):
    GSAAdvantage_password = os.environ['GSAAdvantage_password']
  else:
    GSAAdvantage_password = getpass.getpass("Enter GSA Advantage Password: ")

  if ('GSAAdvantage_cartNumb' in os.environ):
    GSAAdvantage_cartNumb = os.environ['GSAAdvantage_cartNumb']
  else:
    GSAAdvantage_cartNumb = raw_input("Enter the Cart Number you wish to display: ")


# Give the user some peace of mind
  print "Looking for your record! (usually for about 4 seconds.)"

  cart = getCart(GSAAdvantage_userName,GSAAdvantage_password,GSAAdvantage_cartNumb)
  print json.dumps(cart,indent=4,sort_keys=True)

if __name__ == "__main__":
  actLikeACommandLineProgram()
