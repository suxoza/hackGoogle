import http.client,  sys, urllib.request, urllib.parse, random, time, json
from bs4 import BeautifulSoup

lastTime = 0


class SelfException(Exception):
	pass


class getGoogle:

	_host 	  = "accounts.google.com"		
	_proxyIP   = ""
	_proxyPORT = 0
	_saveProxy = 300 # 5 min
	_proxyFile = 'proxy.ip'

	def __init__(self):
		self.getFreshProxy()

	def getFreshProxy(self):
		tm = int(time.time())
		obj = {}
		try:
			with open(self._proxyFile) as r:
				json_ = json.load(r)
				k = list(json_.keys())[0]
				if tm - int(k) > self._saveProxy:
					raise SelfException("get new value")
				obj = json_[k]

		except (SelfException, FileNotFoundError) as e:
			print(e)
			obj = self.proxyToFile()
		

		self._proxyIP 	= obj['ip']
		self._proxyPORT  = obj['port']
		print(obj)

	def proxyToFile(self, getOnlyMin = True):
		ipList = {}
		conn = urllib.request.Request("https://free-proxy-list.net/", headers={'User-Agent': 'Mozilla/5.0'})
		r = urllib.request.urlopen(conn)
		html = r.read()
		headers = r.headers
		soup = BeautifulSoup(html, "html.parser")
		tr = soup.find("table", {'id': "proxylisttable"}).find("tbody").findAll("tr")
		for item in tr:
			td = item.findAll('td')
			if getOnlyMin and 'hour' not in td[7].text:continue
			if  td[6].text == 'yes':
				k = int(td[7].text.split(" ")[0])
				v = {"ip": td[0].text, "port": td[1].text}
				try:
					ipList[k].append({"ip": td[0].text, "port": td[1].text})
				except Exception as e:
					ipList[k] = [v]
		if not len(ipList):
			print('get to recursive...')
			return self.proxyToFile(False)
		mn = min(ipList, key=int)
		lastTime = int(time.time())
		returnValue = random.choice(ipList[mn])
		obj = {lastTime: returnValue}
		with open(self._proxyFile, "w") as w:
			json.dump(obj, w)
		return returnValue





if __name__ == '__main__':
	try:
		getGoogle()
	except Exception as e:
		print(e)
	sys.exit()



conn = http.client.HTTPSConnection(proxyIP, proxyPORT)



conn.set_tunnel(host)

headers_ = {
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": host,
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
		}


conn.request("GET","/_/signup/accountdetails?hl=ka&_reqid=51281&rt=j",urllib.parse.urlencode(self.params_))




r1 = conn.getresponse()
rdr = r1.read().decode("utf_8").strip("\n")

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