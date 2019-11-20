import http.client, urllib
conn = http.client.HTTPConnection("14.207.58.207", 3128)
#conn = http.client.HTTPConnection("accounts.google.com", 80)
conn.set_tunnel("sites.lilu.ge")
#conn.set_tunnel("accounts.google.com")

#conn.request("GET","/signup/v2?flowName=GlifWebSignIn&amp;flowEntry=SignUp")
conn.request("GET","/tst.php")
r1 = conn.getresponse()
rdr = r1.read().decode("utf_8")
print(r1.headers)
print(rdr)


