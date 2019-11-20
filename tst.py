import http.client
conn = http.client.HTTPSConnection("50.246.4.13", 54325)
#conn = http.client.HTTPConnection("accounts.google.com", 80)
#conn.set_tunnel("sites.lilu.ge")
conn.set_tunnel("accounts.google.com")

conn.request("GET","/signup/v2?flowName=GlifWebSignIn&amp;flowEntry=SignUp")
#conn.request("GET","/tst.php")
r1 = conn.getresponse()
rdr = r1.read().decode("utf_8")
print(r1.headers)

with open("google.html", "w") as w:
	w.write(rdr)
cookie = {}
for i,v in r1.headers.items():
	if i == 'Set-Cookie':
		fKey = v.split(";")
		for itr in fKey:
			sKey = itr.split("=")
			try:
				cookie[sKey[0]] = sKey[1]
			except:
				cookie[sKey[0]] = ''
		break


print(cookie)