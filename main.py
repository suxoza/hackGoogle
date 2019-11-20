import http.client, urllib.parse, json, requests, socket
from proxy import getProxy



class Auth:

	_proxy 	 = {}
	_host 	 = "accounts.google.com"	
	_headers = {} 
	_params  = {}
	_cookie  = {}
	conn 	 = False
	_authUrl  = "/signup/v2?flowName=GlifWebSignIn&amp;flowEntry=SignUp"
	_authActionUrl = "/_/signup/accountdetails?hl=ka&_reqid=70475&rt=j"

	def __init__(self):
		self.headers()
		self.proxy()
		

		#auth page
		#self.getAuthPage()
		self.authAction()

	def __del__(self): 
		if self.conn:
			self.conn.close()

	def proxy(self, force = False):
		self._proxy = getProxy(force)
		self.initConnection()


	def initConnection(self):
		self.conn = http.client.HTTPSConnection(self._proxy.proxyIP, self._proxy.proxyPORT)
		self.conn.set_tunnel(self._host)

	def sendRequest(self, method, url):
		try:
			self.conn.request(method, url, urllib.parse.urlencode(self._params), self._headers)
		except (http.client.RemoteDisconnected, socket.error) as e:
			print("run to force...")
			self.proxy(True)
			return self.sendRequest(method, url)


	def authAction(self):
		print("---call method: authAction")
		#self._headers['Cookie'] = 'GAPS='+self._cookie['GAPS']
		self._headers['Referer'] = "https://{0}{1}".format(self._host, self._authUrl)

		with open('params.json') as r:
			self._params = json.load(r)



		self._headers['Cookie'] = 'GAPS=1:YSHVtaMjCSw7i43Yo_4tbAEL5F8yqw:5O7oHA9JWUyVxWNK'
		self.sendRequest("POST", self._authActionUrl)	
		r1 = self.conn.getresponse()
		print(r1.status, r1.reason)
		print(r1.read().decode("utf_8"))
		#r1 = self.conn.getCookie()



	def getAuthPage(self):
		print("---call method: getAuthPage")
		self.sendRequest("GET", self._authUrl)				
				
		r1 = self.conn.getresponse()
		rdr = r1.read().decode("utf_8")
		print(r1.status, r1.reason)
		print(r1.headers)
		self.getCookie(r1.headers)
		print(self._cookie)
		for key, value in self._headers.items():
			print(key, value)

		self.authAction()
		#print(self._headers)

	def getCookie(self, headers):
		for i,v in headers.items():
			if i == 'Set-Cookie':
				fKey = v.split(";")
				for itr in fKey:
					sKey = itr.split("=")
					try:
						self._cookie[sKey[0]] = sKey[1]
					except:
						self._cookie[sKey[0]] = ''
				break
		

	def connection(self):
		pass

	def headers(self):
		self._headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "X-Same-Domain": "1",
            "Google-Accounts-XSRF": "1",
            "TE": "Trailers",
            "Host": self._host,
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
        }




if __name__ == '__main__':
	Auth()