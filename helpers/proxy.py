import http.client, sys, urllib.request, urllib.parse, random, time, json
from bs4 import BeautifulSoup




class SelfException(Exception):
	pass


class getProxy:

	proxyIP    = ""
	proxyPORT  = 0
	_saveProxy = 300 # 5 min
	_proxyFile = 'proxy.ip'
	_lastProxyTime = 0

	def __init__(self, force = False):
		if force:
			self.proxyToFile()
		self.getFreshProxy()

	def getFreshProxy(self):
		tm = int(time.time())
		obj = {}
		try:
			with open(self._proxyFile) as r:
				json_ = json.load(r)
				k = list(json_.keys())[0]
				if tm - int(k) > self._saveProxy:
					raise SelfException()
				obj = json_[k]

		except (SelfException, FileNotFoundError) as e:
			obj = self.proxyToFile()
		

		self.proxyIP 	= obj['ip']
		self.proxyPORT  = obj['port']
		

	def proxyToFile(self, getOnlyMin = True):
		print("get new proxy: ")
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
					ipList[k].append(v)
				except Exception as e:
					ipList[k] = [v]
		if not len(ipList):
			print('get recursive...')
			return self.proxyToFile(False)
		mn = min(ipList, key=int)
		self._lastProxyTime = int(time.time())
		returnValue = random.choice(ipList[mn])
		obj = {self._lastProxyTime: returnValue}
		with open(self._proxyFile, "w") as w:
			json.dump(obj, w)
		print(returnValue)
		return returnValue





if __name__ == '__main__':
	try:
		getProxy()
	except Exception as e:
		print(e)


