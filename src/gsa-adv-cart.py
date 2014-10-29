#!/usr/bin/python
import cgi
import cgitb
import json
import gsa_advantage

cgitb.enable()


form = cgi.FieldStorage() 

# Get data from fields
gsa_adv_p = form.getvalue('p')
gsa_adv_u = form.getvalue('u')
gsa_adv_cart_id = form.getvalue('cart_id')
callback = form.getvalue('callback')


print "Content-type: application/json"
print 
response = gsa_advantage.getCart(gsa_adv_u,gsa_adv_p,gsa_adv_cart_id)
d = json.JSONEncoder().encode((response))
if (callback):
    print callback+'(' + d + ');'
else:
    print d


